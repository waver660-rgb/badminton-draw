import base64
import os
import tempfile
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    ImageMessage,
    MessagingApi,
    PushMessageRequest,
)

load_dotenv()

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_TARGET_USER_ID = os.environ["LINE_TARGET_USER_ID"]
# 公開URLのベース（バイナリ受信時に使用。外部からアクセス可能なURLを設定）
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

TEMP_IMAGE_DIR = Path(tempfile.gettempdir()) / "aibo_photos"
TEMP_IMAGE_DIR.mkdir(exist_ok=True)


def _push_image_url(original_url: str, preview_url: str | None = None) -> None:
    with ApiClient(configuration) as api_client:
        MessagingApi(api_client).push_message(
            PushMessageRequest(
                to=LINE_TARGET_USER_ID,
                messages=[
                    ImageMessage(
                        original_content_url=original_url,
                        preview_image_url=preview_url or original_url,
                    )
                ],
            )
        )


def _save_and_push_binary(image_data: bytes) -> None:
    """
    バイナリ画像を一時ファイルに保存し、PUBLIC_BASE_URL 経由でLINEに送信する。
    PUBLIC_BASE_URL が未設定の場合は ValueError を送出する。
    """
    if not PUBLIC_BASE_URL:
        raise ValueError(
            "バイナリ画像を送るには .env に PUBLIC_BASE_URL を設定してください。"
            " (例: PUBLIC_BASE_URL=https://your-server.example.com)"
        )
    import uuid
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = TEMP_IMAGE_DIR / filename
    filepath.write_bytes(image_data)
    image_url = f"{PUBLIC_BASE_URL}/aibo_photos/{filename}"
    _push_image_url(image_url)


@app.route("/webhook/aibo", methods=["POST"])
def aibo_webhook():
    """
    AIBOからの写真撮影イベントを受け取るエンドポイント。

    対応フォーマット:
      1. JSON {"photo_url": "https://..."}
      2. JSON {"photo_base64": "<base64文字列>"}
      3. multipart/form-data  (フィールド名: photo)
      4. 生バイナリ (Content-Type: image/jpeg など)
    """
    content_type = request.content_type or ""

    try:
        if "application/json" in content_type:
            payload = request.get_json(force=True) or {}
            if "photo_url" in payload:
                _push_image_url(payload["photo_url"])
            elif "photo_base64" in payload:
                image_data = base64.b64decode(payload["photo_base64"])
                _save_and_push_binary(image_data)
            else:
                return jsonify({"error": "photo_url または photo_base64 が必要です"}), 400

        elif "multipart/form-data" in content_type:
            if "photo" not in request.files:
                return jsonify({"error": "フィールド 'photo' が見つかりません"}), 400
            _save_and_push_binary(request.files["photo"].read())

        else:
            image_data = request.get_data()
            if not image_data:
                return jsonify({"error": "画像データが空です"}), 400
            _save_and_push_binary(image_data)

    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error("送信エラー: %s", e)
        return jsonify({"error": "送信に失敗しました"}), 500

    return jsonify({"status": "ok", "message": "橋本香織に写真を送信しました"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(host="0.0.0.0", port=port)
