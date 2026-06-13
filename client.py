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
