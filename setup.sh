#!/bin/bash
set -e

echo "=== AIBOからLINEへ写真送信 セットアップ ==="

# Python確認
if ! command -v python3 &>/dev/null; then
    echo "エラー: Python3 が見つかりません。インストールしてください。"
    exit 1
fi

# 仮想環境作成
if [ ! -d ".venv" ]; then
    echo "仮想環境を作成中..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "依存ライブラリをインストール中..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# .env確認
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "===================================================="
    echo ".env ファイルを作成しました。"
    echo "以下の値を設定してから再度起動してください:"
    echo ""
    echo "  LINE_CHANNEL_ACCESS_TOKEN  ... LINE Developersで取得"
    echo "  LINE_CHANNEL_SECRET        ... LINE Developersで取得"
    echo "  LINE_TARGET_USER_ID        ... 橋本香織さんのUser ID"
    echo "                               (起動後、ボットにメッセージを送ると取得できます)"
    echo "===================================================="
    exit 0
fi

echo ""
echo "サーバーを起動中... (Ctrl+C で停止)"
echo ""
python3 aibo_line_sender.py
