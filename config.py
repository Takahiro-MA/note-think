"""
note.com 投稿ツール設定

Cookieはブラウザから手動取得して cookies.json に保存する。
"""
import json
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
COOKIES_FILE = CONFIG_DIR / "cookies.json"

NOTE_BASE_URL = "https://note.com"
NOTE_API_BASE = f"{NOTE_BASE_URL}/api/v1"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": NOTE_BASE_URL,
    "Referer": "https://note.com/akausa28",
    "x-requested-with": "XMLHttpRequest",
}


def load_cookies() -> dict[str, str]:
    """cookies.json から Cookie を読み込む"""
    if not COOKIES_FILE.exists():
        raise FileNotFoundError(
            f"Cookie ファイルが見つかりません: {COOKIES_FILE}\n"
            "ブラウザの DevTools から Cookie を取得して cookies.json に保存してください。"
        )
    data = json.loads(COOKIES_FILE.read_text())
    if isinstance(data, list):
        # [{name: ..., value: ...}, ...] 形式の場合
        return {c["name"]: c["value"] for c in data}
    # {name: value, ...} 形式の場合
    return data
