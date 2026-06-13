# note.com 自動投稿ツール

note.com（非公式API）を使った記事の自動生成・下書き投稿ツール。
スケジューラー（scheduler-state.json）と連携して毎朝8時に記事を自動生成する。

## ディレクトリ構成

```
/workspace/note_poster/
├── README.md              ← このファイル
├── style_guide.md         ← 記事生成のスタイルガイド（文体・構成・トーン）
├── config.py              ← API設定、ヘッダー、Cookie読み込み
├── auth.py                ← セッション管理、有効性チェック
├── client.py              ← note.com APIクライアント（作成・保存・一覧）
├── cli.py                 ← CLIツール
├── __init__.py
├── __main__.py
├── cookies.json           ← 認証Cookie（手動更新）★秘密情報
├── drafts/                ← 生成した記事のMarkdownファイル
└── test_connection.py     ← 接続テスト
```

## 環境

- Python 3.11 (venv: `/workspace/.venv`)
- 依存: `requests`, `markdown`（`/workspace/.venv/bin/pip`で管理）

## CLI使い方

```bash
# セッション有効性チェック
/workspace/.venv/bin/python -m note_poster check

# 下書き一覧
/workspace/.venv/bin/python -m note_poster list

# Markdownファイルから下書き作成
/workspace/.venv/bin/python -m note_poster draft "タイトル" article.md

# Cookie更新（期限切れ時）
/workspace/.venv/bin/python -m note_poster update-cookie "新しいCookie値"
```

## 認証

- **認証方式**: `_note_session_v5` Cookie（セッションベース）
- **auth_tokenは不要**: セッションCookieだけで全API操作可能
- **有効期限**: 数日〜数週間（サーバー側設定依存）
- **期限切れ時**: ブラウザDevToolsから `_note_session_v5` をコピーして `update-cookie` で更新

### Cookie更新手順
1. ブラウザで https://note.com にログイン
2. DevTools (F12) → Application → Cookies → `https://note.com`
3. `_note_session_v5` の値をコピー
4. `python -m note_poster update-cookie "値"` を実行

## API仕様（非公式）

| 操作 | エンドポイント | メソッド |
|------|--------------|---------|
| 記事作成 | `/api/v1/text_notes` | POST |
| 下書き保存 | `/api/v1/text_notes/draft_save?id={id}` | POST |
| 下書き一覧 | `/api/v2/note_list/contents?status=draft` | GET |
| 公開記事一覧 | `/api/v2/note_list/contents?status=published` | GET |
| 記事本文取得 | `/api/v3/notes/{key}` | GET |

- ヘッダーに `x-requested-with: XMLHttpRequest` が必要
- 本文はHTML形式（Markdownをmarkdownライブラリで変換）

## 記事生成フロー

### スケジューラー経由（自動）
1. scheduler-state.json の `note-daily-post` ジョブが毎朝8時(JST)に発火
2. agentTurnが起動し、以下を実行:
   a. `/workspace/note_poster/style_guide.md` を読む
   b. 曜日に応じたテーマを選択（ローテーション表参照）
   c. 記事を生成
   d. note APIで下書き投稿
   e. Slackで通知（タイトルとedit URL）

### 手動
1. `python -m note_poster check` でセッション確認
2. Markdownファイルを作成
3. `python -m note_poster draft "タイトル" file.md` で下書き投稿

## テーマローテーション

| 曜日 | テーマ |
|------|--------|
| 月・木 | AI・テック考察 |
| 火・金 | ガジェット・プロダクト論 |
| 水・土 | 働き方・思考法 |
| 日 | ツール・ライフハック |
| 週1回（金 or 土） | アフィリエイト比較記事（ガジェット枠と兼用） |

詳細は `style_guide.md` を参照。

## アフィリエイト比較記事

- Amazonリンク挿入ポイントは `<!-- 🔗 商品リンク: 製品名 -->` で明示
- リンクはTakahiroが下書きを確認後、手動で貼り付け
- 比較記事のトーンは通常記事より具体的・実用的（style_guide.md参照）

## 注意事項

- **非公式API**: 仕様変更・BANリスクあり。低頻度利用を推奨
- **Cookie管理**: cookies.jsonに秘密情報が含まれる。gitに入れないこと
- **公開API**: 現状は下書き保存まで。公開は手動（公開APIは未検証）
- **ユーザー名**: ta_ka_mi_ya (たかみや)
- **noteのReferer**: `https://note.com/akausa28`（config.pyで設定）
