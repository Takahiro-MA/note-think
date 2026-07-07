"""
note.com API クライアント（非公式API）
"""
import markdown
import requests

from .auth import get_session_cookie, check_session_valid, SESSION_COOKIE_NAME
from .config import NOTE_API_BASE, DEFAULT_HEADERS


class NoteClient:
    """note.com の非公式APIを叩くクライアント"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        session_cookie = get_session_cookie()
        self.session.cookies.set(SESSION_COOKIE_NAME, session_cookie)

    def test_connection(self) -> dict:
        """認証が有効か確認"""
        return check_session_valid()

    def create_draft(self, title: str, body_markdown: str) -> dict:
        """
        新規記事を下書きとして作成する。

        Args:
            title: 記事タイトル
            body_markdown: 本文（Markdown）

        Returns:
            {"success": bool, "note_id": int, ...}
        """
        body_html = markdown.markdown(
            body_markdown,
            extensions=["extra", "codehilite", "nl2br"],
        )

        # 記事作成
        create_resp = self.session.post(
            f"{NOTE_API_BASE}/text_notes",
            json={"name": title, "body": ""},
        )

        if create_resp.status_code not in (200, 201):
            return {
                "success": False,
                "status_code": create_resp.status_code,
                "error": create_resp.text,
                "step": "create",
            }

        create_data = create_resp.json()
        note_id = create_data.get("data", {}).get("id")

        if not note_id:
            return {
                "success": False,
                "error": "記事IDが取得できませんでした",
                "response": create_data,
                "step": "parse_id",
            }

        # 下書き保存
        save_resp = self.session.post(
            f"{NOTE_API_BASE}/text_notes/draft_save",
            params={"id": note_id, "is_temp_saved": "true"},
            json={
                "name": title,
                "body": body_html,
                "body_length": len(body_markdown),
            },
        )

        if save_resp.status_code not in (200, 201):
            return {
                "success": False,
                "status_code": save_resp.status_code,
                "error": save_resp.text,
                "note_id": note_id,
                "step": "draft_save",
            }

        return {
            "success": True,
            "note_id": note_id,
            "title": title,
            "url": f"https://note.com/notes/{create_data['data']['key']}/edit",
            "message": "下書き保存しました",
        }

    def update_draft(self, note_id: int, title: str, body_markdown: str) -> dict:
        """
        既存の下書き（note_id）を上書き更新する。

        ※注意: これは下書き(draft)にのみ有効。公開済み記事には反映されない
        （編集が下書きバッファに溜まるだけでライブに出ない）。公開記事を直すには
        note画面でいったん下書きに戻してから update する。

        Args:
            note_id: 既存記事のID（list_drafts や create_draft の戻り値で取得）
            title: 記事タイトル
            body_markdown: 本文（Markdown）

        Returns:
            {"success": bool, "note_id": int, ...}
        """
        body_html = markdown.markdown(
            body_markdown,
            extensions=["extra", "codehilite", "nl2br"],
        )

        save_resp = self.session.post(
            f"{NOTE_API_BASE}/text_notes/draft_save",
            params={"id": note_id, "is_temp_saved": "true"},
            json={
                "name": title,
                "body": body_html,
                "body_length": len(body_markdown),
            },
        )

        if save_resp.status_code not in (200, 201):
            return {
                "success": False,
                "status_code": save_resp.status_code,
                "error": save_resp.text,
                "note_id": note_id,
                "step": "draft_save",
            }

        return {
            "success": True,
            "note_id": note_id,
            "title": title,
            "message": "下書きを更新しました",
        }

    def list_drafts(self, limit: int = 10) -> list[dict]:
        """下書き一覧を取得"""
        resp = self.session.get(
            f"{NOTE_API_BASE.replace('/v1', '/v2')}/note_list/contents",
            params={"limit": limit, "page": 1, "status": "draft", "without_magazines": "true"},
        )
        if resp.status_code != 200:
            return []
        data = resp.json()
        return [
            {
                "id": n["id"],
                "title": n.get("name") or "(無題)",
                "created_at": n.get("publishAt") or n.get("created_at", ""),
            }
            for n in data.get("data", {}).get("notes", [])
        ]

    def get_stats(self, filter: str = "all") -> dict:
        """ダッシュボードのアクセス統計を取得（全ページ集約）

        Args:
            filter: "all" | "week" | "month"

        Returns:
            {"total_pv": int, "total_like": int, "total_comment": int,
             "articles": [{"key", "title", "read", "like", "comment", "publish_at"}, ...]}
        """
        import time

        articles: list[dict] = []
        totals = {"total_pv": 0, "total_like": 0, "total_comment": 0}
        page = 1
        while True:
            resp = self.session.get(
                f"{NOTE_API_BASE}/stats/pv",
                params={"filter": filter, "page": page, "sort": "pv"},
            )
            if resp.status_code != 200:
                break
            data = resp.json().get("data", {})
            totals = {
                "total_pv": data.get("total_pv", 0),
                "total_like": data.get("total_like", 0),
                "total_comment": data.get("total_comment", 0),
            }
            articles += [
                {
                    "key": s.get("key"),
                    "title": s.get("name"),
                    "read": s.get("read_count", 0),
                    "like": s.get("like_count", 0),
                    "comment": s.get("comment_count", 0),
                }
                for s in data.get("note_stats", [])
            ]
            if data.get("last_page") or page >= 20:
                break
            page += 1
            time.sleep(0.4)

        # 公開日を published 一覧から結合
        publish_at: dict[str, str] = {}
        page = 1
        while True:
            resp = self.session.get(
                f"{NOTE_API_BASE.replace('/v1', '/v2')}/note_list/contents",
                params={"status": "published", "page": page},
            )
            if resp.status_code != 200:
                break
            data = resp.json().get("data", {})
            notes = data.get("notes", [])
            if not notes:
                break
            for n in notes:
                publish_at[n.get("key")] = n.get("publish_at") or n.get("publishAt") or ""
            if data.get("is_last_page") or data.get("isLastPage") or page >= 20:
                break
            page += 1
            time.sleep(0.4)
        for a in articles:
            a["publish_at"] = publish_at.get(a["key"], "")
        return {**totals, "articles": articles}
