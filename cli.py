#!/usr/bin/env python3
"""
note.com 投稿 CLI

使い方:
    # セッション確認
    python -m note_poster.cli check

    # Markdownファイルから下書き作成
    python -m note_poster.cli draft "タイトル" article.md

    # 下書き一覧
    python -m note_poster.cli list

    # セッションCookie更新
    python -m note_poster.cli update-cookie "新しいCookie値"
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from note_poster.auth import check_session_valid, update_session_cookie, SessionExpiredError
from note_poster.client import NoteClient


def cmd_check():
    """セッション状態を確認"""
    result = check_session_valid()
    status = "OK" if result["valid"] else "NG"
    print(f"[{status}] {result['message']}")


def cmd_draft(title: str, md_file: str):
    """Markdownファイルから下書き作成"""
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"エラー: ファイルが見つかりません: {md_file}")
        sys.exit(1)

    body = md_path.read_text(encoding="utf-8")
    client = NoteClient()
    result = client.create_draft(title, body)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list():
    """下書き一覧"""
    client = NoteClient()
    drafts = client.list_drafts()
    if not drafts:
        print("下書きはありません")
        return
    for d in drafts:
        print(f"  [{d['id']}] {d['title']}")


def cmd_update_cookie(value: str):
    """セッションCookie更新"""
    update_session_cookie(value)
    result = check_session_valid()
    status = "OK" if result["valid"] else "NG"
    print(f"Cookie更新完了 [{status}] {result['message']}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    match cmd:
        case "check":
            cmd_check()
        case "draft":
            if len(sys.argv) < 4:
                print("使い方: cli.py draft <タイトル> <markdownファイル>")
                sys.exit(1)
            cmd_draft(sys.argv[2], sys.argv[3])
        case "list":
            cmd_list()
        case "update-cookie":
            if len(sys.argv) < 3:
                print("使い方: cli.py update-cookie <cookie値>")
                sys.exit(1)
            cmd_update_cookie(sys.argv[2])
        case _:
            print(f"不明なコマンド: {cmd}")
            print(__doc__)
            sys.exit(1)


if __name__ == "__main__":
    main()
