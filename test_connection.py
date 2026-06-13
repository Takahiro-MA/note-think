#!/usr/bin/env python3
"""
note.com 接続テスト

使い方:
1. cookies.json を用意する
2. python -m note_poster.test_connection
"""
import json
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from note_poster.client import NoteClient


def main():
    print("=== note.com 接続テスト ===\n")

    try:
        client = NoteClient()
        print("✓ Cookie 読み込み成功")
    except FileNotFoundError as e:
        print(f"✗ {e}")
        return

    print("→ API 接続テスト中...")
    result = client.test_connection()
    print(f"  ステータスコード: {result['status_code']}")
    print(f"  認証状態: {'✓ 有効' if result['authenticated'] else '✗ 無効'}")

    if result["response_preview"]:
        print(f"  レスポンス: {result['response_preview'][:100]}...")

    if not result["authenticated"]:
        print("\n→ Cookie が無効または期限切れです。ブラウザから再取得してください。")
        return

    # 認証OKなら下書きテスト
    print("\n→ テスト下書き作成中...")
    draft_result = client.create_draft(
        title="[テスト] 自動投稿テスト（削除OK）",
        body_markdown="# テスト\n\nこれは自動投稿のテストです。削除して問題ありません。",
    )
    print(f"  結果: {json.dumps(draft_result, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    main()
