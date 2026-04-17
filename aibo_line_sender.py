import base64
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from linebot.v3 import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    ImageMessage,
    MessagingApi,
    PushMessageRequest,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent

load_dotenv()

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
LINE_TARGET_USER_ID = os.environ.get("LINE_TARGET_USER_ID", "")
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

TEMP_IMAGE_DIR = Path("/tmp/aibo_photos")
TEMP_IMAGE_DIR.mkdir(exist_ok=True)


def _push_image(url: str) -> None:
    with ApiClient(configuration) as api_client:
        MessagingApi(api_client).push_message(
            PushMessageRequest(
                to=LINE_TARGET_USER_ID,
                messages=[ImageMessage(original_content_url=url, preview_image_url=url)],
            )
        )


def _save_binary_and_push(image_data: bytes) -> None:
    if not PUBLIC_BASE_URL:
        raise ValueError(
            ".env に PUBLIC_BASE_URL を設定してください。"
            " このサーバー自身のURL例: PUBLIC_BASE_URL=https://your-domain.com"
        )
    filename = f"{uuid.uuid4().hex}.jpg"
    (TEMP_IMAGE_DIR / filename).write_bytes(image_data)
    _push_image(f"{PUBLIC_BASE_URL}/aibo_photos/{filename}")


@app.route("/aibo_photos/<filename>")
def serve_image(filename: str):
    """保存した画像をLINEサーバーに公開するエンドポイント"""
    return send_from_directory(TEMP_IMAGE_DIR, filename)


@app.route("/webhook/aibo", methods=["POST"])
def aibo_webhook():
    """
    AIBOからの写真撮影イベントを受け取るエンドポイント。

    対応フォーマット:
      1. JSON {"photo_url": "https://..."}       ← AIBOが画像URLを送る場合
      2. JSON {"photo_base64": "<base64文字列>"}  ← Base64エンコード画像
      3. multipart/form-data (フィールド名: photo)
      4. 生バイナリ (Content-Type: image/jpeg など)
    """
    if not LINE_TARGET_USER_ID:
        return jsonify({"error": ".env に LINE_TARGET_USER_ID が設定されていません"}), 500

    content_type = request.content_type or ""
    try:
        if "application/json" in content_type:
            payload = request.get_json(force=True) or {}
            if "photo_url" in payload:
                _push_image(payload["photo_url"])
            elif "photo_base64" in payload:
                _save_binary_and_push(base64.b64decode(payload["photo_base64"]))
            else:
                return jsonify({"error": "photo_url または photo_base64 が必要です"}), 400
        elif "multipart/form-data" in content_type:
            if "photo" not in request.files:
                return jsonify({"error": "フィールド 'photo' が見つかりません"}), 400
            _save_binary_and_push(request.files["photo"].read())
        else:
            data = request.get_data()
            if not data:
                return jsonify({"error": "画像データが空です"}), 400
            _save_binary_and_push(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.error("送信エラー: %s", e)
        return jsonify({"error": "送信に失敗しました"}), 500

    return jsonify({"status": "ok", "message": "橋本香織に写真を送信しました"}), 200


@app.route("/webhook/line", methods=["POST"])
def line_webhook():
    """
    LINEからのWebhookを受け取るエンドポイント。
    ボットにメッセージを送ってきたユーザーのUser IDをログに出力する。
    橋本香織さんにボットを友達追加・メッセージ送信してもらうとUser IDが確認できる。
    """
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return jsonify({"error": "署名が不正です"}), 400

    for event in events:
        user_id = event.source.user_id if event.source else "不明"
        app.logger.info("LINE User ID: %s", user_id)
        print(f"\n[LINE User ID] {user_id}\n→ .env の LINE_TARGET_USER_ID に設定してください\n")

        if isinstance(event, MessageEvent):
            with ApiClient(configuration) as api_client:
                MessagingApi(api_client).reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"あなたのUser ID: {user_id}")],
                    )
                )

    return jsonify({"status": "ok"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "target_user_set": bool(LINE_TARGET_USER_ID)}), 200


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(host="0.0.0.0", port=port)
