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

    # アクセス統計（定点観測。引数=直近N日、デフォルト30）
    python -m note_poster.cli stats [days]

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


def cmd_update(note_id: str, title: str, md_file: str):
    """既存の下書き（note_id）を上書き更新"""
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"エラー: ファイルが見つかりません: {md_file}")
        sys.exit(1)

    body = md_path.read_text(encoding="utf-8")
    client = NoteClient()
    result = client.update_draft(int(note_id), title, body)
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


def cmd_stats(days: int = 30):
    """アクセス統計（定点観測用）: 全期間合計＋直近N日の記事別PV/スキ/スキ率"""
    from datetime import datetime, timedelta, timezone

    client = NoteClient()
    stats = client.get_stats(filter="all")
    articles = stats["articles"]
    print(f"全期間: {len(articles)}記事 / PV {stats['total_pv']:,} / スキ {stats['total_like']:,} "
          f"/ スキ率 {stats['total_like'] / max(stats['total_pv'], 1) * 100:.1f}%")

    cut = datetime.now(timezone(timedelta(hours=9))) - timedelta(days=days)
    recent = []
    for a in articles:
        try:
            d = datetime.fromisoformat(a["publish_at"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            continue
        if d >= cut:
            recent.append({**a, "date": d})
    recent.sort(key=lambda a: a["date"])

    if not recent:
        print(f"直近{days}日の公開記事はありません")
        return
    reads = sorted(a["read"] for a in recent)
    median = reads[len(reads) // 2]
    total_read = sum(a["read"] for a in recent)
    total_like = sum(a["like"] for a in recent)
    print(f"直近{days}日: {len(recent)}記事 / PV {total_read:,}（中央値 {median}） / スキ {total_like} "
          f"/ スキ率 {total_like / max(total_read, 1) * 100:.1f}%")
    print(f"\n{'公開':5} {'PV':>6} {'スキ':>4} {'率%':>6}  タイトル")
    for a in recent:
        rate = a["like"] / a["read"] * 100 if a["read"] else 0
        print(f"{a['date'].strftime('%m/%d'):5} {a['read']:>6} {a['like']:>4} {rate:>6.1f}  {a['title'][:42]}")


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
        case "update":
            if len(sys.argv) < 5:
                print("使い方: cli.py update <note_id> <タイトル> <markdownファイル>")
                sys.exit(1)
            cmd_update(sys.argv[2], sys.argv[3], sys.argv[4])
        case "list":
            cmd_list()
        case "stats":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            cmd_stats(days)
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
