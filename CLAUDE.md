# note_poster — note.com 自動投稿ツール

## What this is

note.com（非公式API）を使った記事の自動生成・下書き投稿ツール。
スケジューラ経由で毎朝記事を生成し、note.com に下書きとして保存する。

## Current state

- ソース実装: 完了（`auth.py` / `client.py` / `cli.py` / `config.py`）
- 既存下書き: `drafts/` に5本（AI技術 / ガジェット / 働き方 / ライフハック / アフィリエイト比較）
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
- 状態管理: `article-status.md` / 記事本体: `articles/<slug>/article.md`
- ★ホストでは `python3 -m note_poster ...`（`/workspace/.venv/bin/python` はコンテナ用）

## Read first when working here

| 目的 | ファイル |
|------|---------|
| 全体像・CLI使い方 | `README.md` |
| 記事制作パイプライン設計 | `knowledge/04_integrated_design.md` |
| 記事の文体・構成・トーン | `style_guide.md` |
| 認証Cookie | `cookies.json`（編集前に有効性チェック） |
| 過去下書き | `drafts/01_ai_tech.md` 〜 `05_affiliate_comparison.md` |

## Conventions

- Python 環境: `/workspace/.venv/bin/python`
- 依存: `requests`, `markdown`
- 新しい記事を生成する前に、必ず `style_guide.md` を読む
- Cookie 期限切れ時は `cli.py` の `check` コマンドで判定→ユーザに更新依頼

## Commands

```bash
# セッション有効性チェック
/workspace/.venv/bin/python -m note_poster check

# 下書き一覧
/workspace/.venv/bin/python -m note_poster list

# Markdownから下書き作成
/workspace/.venv/bin/python -m note_poster draft "タイトル" article.md
```
