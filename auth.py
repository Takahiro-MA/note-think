"""
note.com 認証管理

セッションCookie (_note_session_v5) の管理と有効性チェック。
Cookieが切れた場合は通知して手動更新を促す。
"""
import json
import time
from pathlib import Path

from .config import COOKIES_FILE, NOTE_API_BASE, DEFAULT_HEADERS

SESSION_COOKIE_NAME = "_note_session_v5"


def check_session_valid() -> dict:
    """
    現在のセッションが有効か確認する。

    Returns:
        {"valid": bool, "message": str}
    """
    import requests

    cookies = _load_raw_cookies()
    session_cookie = cookies.get(SESSION_COOKIE_NAME)

    if not session_cookie:
        return {"valid": False, "message": f"{SESSION_COOKIE_NAME} が cookies.json にありません"}

    resp = requests.get(
        f"{NOTE_API_BASE.replace('/v1', '/v2')}/note_list/contents",
        params={"limit": 1, "page": 1, "status": "draft"},
        cookies={SESSION_COOKIE_NAME: session_cookie},
        headers=DEFAULT_HEADERS,
    )

    if resp.status_code == 200:
        return {"valid": True, "message": "セッション有効"}

    return {
        "valid": False,
        "message": f"セッション無効 (status={resp.status_code})。Cookie を再取得してください。",
    }


def update_session_cookie(new_value: str) -> None:
    """セッションCookieを更新する"""
    cookies = _load_raw_cookies()
    cookies[SESSION_COOKIE_NAME] = new_value
    COOKIES_FILE.write_text(json.dumps(cookies, indent=2, ensure_ascii=False))


def get_session_cookie() -> str:
    """有効なセッションCookieを返す。無効なら例外"""
    result = check_session_valid()
    if not result["valid"]:
        raise SessionExpiredError(result["message"])
    cookies = _load_raw_cookies()
    return cookies[SESSION_COOKIE_NAME]


def _load_raw_cookies() -> dict:
    if not COOKIES_FILE.exists():
        return {}
    return json.loads(COOKIES_FILE.read_text())


class SessionExpiredError(Exception):
    """セッション期限切れ"""
    pass
