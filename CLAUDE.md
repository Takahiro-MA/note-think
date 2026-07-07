# note_poster — note記事の企画・執筆・投稿基盤

## What this is

note記事の企画・執筆・下書き投稿の基盤。制作は下記の半自動パイプライン（5コマンド）で行い、
note.com（非公式API）に下書きとして保存する。**公開操作・有料ライン・価格設定はnote編集画面で人間が行う。**

## 実行環境（正典）

- このリポジトリはホスト（`/home/takahiroma`）とNoahコンテナの両方から使われる。
- **ホストでの実行**: `cd /home/takahiroma/noah-workspace && python3 -m note_poster <cmd>`
- **Noahコンテナ内での実行**: `/workspace/.venv/bin/python -m note_poster <cmd>`
- どちらの環境かは `test -d /workspace && echo container || echo host` で判定する。
- 依存: `requests`, `markdown`

```bash
# 例（ホスト）。必ず noah-workspace から実行する（note_poster直下からでは -m が解決しない）
cd /home/takahiroma/noah-workspace
python3 -m note_poster check                          # セッション有効性チェック
python3 -m note_poster list                           # 下書き一覧
python3 -m note_poster draft "タイトル" article.md    # 下書き作成
python3 -m note_poster stats 30                       # アクセス統計（直近30日・定点観測）
```

## Current state

- ソース実装: 完了（`auth.py` / `client.py` / `cli.py` / `config.py`）
- 記事本体: `articles/<slug>/article.md`（一覧と状態は `article-status.md`）
- `drafts/` は旧v1時代の下書き置き場（参考資料。現行の記事は `articles/` に置く）
- 認証: `cookies.json` に Cookie を保存（手動更新）★秘密情報

## 記事制作パイプライン（半自動・2026-06-13〜）

note有料コンテンツの半自動量産が目標。記事の"格"でプロセスの重さを変える軽量フロー。

```
/article <ネタ>          # ネタ採点→5行設計→初稿執筆（①の売れる形を内蔵）
/title <file or テーマ>  # タイトル磨き：候補10本→好奇/共感で採点→本文が回収できるか検証→上位提示
/check-compliance <file> # 規約/不当表示の自動チェック（人手ゼロ・必須）
/review <file>           # 任意・多視点レビュー（有料主力のみ）
/publish <file>          # 公開前チェック→人間承認→note下書き投稿
```

- 設計の全体像: `knowledge/04_integrated_design.md`
- 売れる形のノウハウ: `knowledge/01_paid_note_playbook.md` / `02_note_monetization_book_notes.md`
- ネタのストック: `ideas/`（使い方=`ideas/README.md`、全ネタの地図=`ideas/_netacho.md`、人物像=`ideas/_self-inventory.md`）
- 状態管理: `article-status.md` — **`/publish` 実行時に必ず更新し、`Last Updated` を書き換える**

## 文体の正典

- 文体・構成の正典は `style_guide.md`（v2）。人物像・声・テーマの正典は `ideas/_self-inventory.md` と `ideas/_netacho.md`。
- **両者が矛盾する場合は `_self-inventory.md` が勝つ。**
- 新しい記事を生成する前に、必ず `style_guide.md` を読む。

## Read first when working here

| 目的 | ファイル |
|------|---------|
| 全体像・CLI使い方・API仕様 | `README.md` |
| 記事制作パイプライン設計 | `knowledge/04_integrated_design.md` |
| 記事の文体・構成・トーン | `style_guide.md`（v2） |
| ネタと人物像 | `ideas/_netacho.md` / `ideas/_self-inventory.md` |
| 認証Cookie | `cookies.json`（編集前に有効性チェック） |

## Conventions

- 上位規約: `~/.claude/CLAUDE.md`（グローバル原則）に従う。
- Cookie 期限切れ時は `check` コマンドで判定→ユーザに更新依頼（勝手に更新しない）。
- 実行パスは本ファイル「実行環境」節が正典。他ファイルでパスを再定義しない。
