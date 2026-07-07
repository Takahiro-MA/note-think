# note.com 自動投稿ツール

note.com（非公式API）を使った記事の自動生成・下書き投稿ツール。
スケジューラー（scheduler-state.json）と連携して毎朝8時に記事を自動生成する。

## ディレクトリ構成

パスはホストでは `/home/takahiroma/noah-workspace/note_poster/`、Noahコンテナ内では `/workspace/note_poster/`（同一実体）。

```
note_poster/
├── README.md              ← このファイル
├── CLAUDE.md              ← プロジェクト憲章（実行環境の正典・パイプライン）
├── style_guide.md         ← 記事生成のスタイルガイド v2（文体・構成・トーン）
├── article-status.md      ← 全記事の状態管理台帳
├── articles/              ← 記事本体（articles/<slug>/article.md）
├── ideas/                 ← ネタ帳（_netacho.md=地図 / _self-inventory.md=人物像）
├── knowledge/             ← 売れる形・設計ドキュメント
├── .claude/commands/      ← /article /title /check-compliance /review /publish
├── config.py / auth.py / client.py / cli.py  ← CLI実装
├── cookies.json           ← 認証Cookie（手動更新）★秘密情報
├── drafts/                ← 旧v1時代の下書き（参考資料）
└── test_connection.py     ← 接続テスト
```

## 環境

実行パスの正典は `CLAUDE.md`「実行環境」節。

- **ホスト**: `cd /home/takahiroma/noah-workspace && python3 -m note_poster <cmd>`
- **Noahコンテナ**: `/workspace/.venv/bin/python -m note_poster <cmd>`（Python 3.11 venv）
- 依存: `requests`, `markdown`

## CLI使い方

```bash
# 以下はホスト表記（コンテナ内は python3 → /workspace/.venv/bin/python に読み替え）

# セッション有効性チェック
python3 -m note_poster check

# 下書き一覧
python3 -m note_poster list

# Markdownファイルから下書き作成
python3 -m note_poster draft "タイトル" article.md

# Cookie更新（期限切れ時）
python3 -m note_poster update-cookie "新しいCookie値"
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
   a. `style_guide.md`（v2）と `ideas/_netacho.md` を読む
   b. テーマを `ideas/_netacho.md` の4柱（断酒／身体と暮らし／会社員／AI）＋雑多から選択
   c. 記事を生成
   d. note APIで下書き投稿
   e. Slackで通知（タイトルとedit URL）

### 手動（推奨: `.claude/commands/` のパイプライン）
1. `/article <ネタ>` → `/check-compliance` → `/publish`（詳細は `CLAUDE.md`）
2. CLI直接なら: `check` でセッション確認 → Markdown作成 → `draft` で下書き投稿

## テーマ選定

テーマの正典は `ideas/_netacho.md` の4柱＋雑多コラム（曜日ローテーションは廃止済み・2026-06）。

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
