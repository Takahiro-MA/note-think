# CHANGES.md — note_poster 変更記録

## 2026-07-07 月次レビュー反映（1ヶ月連続投稿の振り返り）

分析: `notes/2026-07-07-monthly-review.md`（実データ: PVの主因は露出ゼロ、スキ率は高い）

- `client.py` / `cli.py`: **`stats` コマンド新設**（定点観測用。全期間合計＋直近N日の記事別PV/スキ/スキ率。
  非公開統計API `/api/v1/stats/pv` を使用）。E2E動作確認済み
- `.claude/commands/title.md`: **検索語の必須化**節を追加（候補10本中5本は検索語入り・
  採点に第4観点「検索語」追加・流入記事では検索語△を落とす）
- `style_guide.md`: **§2.5「エッジの規律」新設**（1行要約テスト・敵の名指し・具体の毒・
  反転1回・断定着地の5規律）＋品質チェックリストに4項目追加
- `.claude/commands/article.md`: ステップ2に**エッジ検査（出力前必須）**を追加

---

# 以下: 再設計（redesign-2026-07）の変更記録

計画: `/home/takahiroma/REDESIGN_PLAN.md` §5.1（Phase 2）。ブランチ: `redesign-2026-07`。

## 2026-07-07 Phase 2 実施内容

### 変更
- `CLAUDE.md` 全面改訂: 「実行環境」節を新設し実行パスの矛盾を解消（ホスト=`python3 -m note_poster`／コンテナ=`/workspace/.venv/bin/python`、判定コマンド付き）。文体の優先順位（style_guide v2 ＜ `_self-inventory.md`）と article-status 更新ルールを明文化。適用前にホストで `python3 -m note_poster check` の動作確認済み（`[OK] セッション有効`）
- `style_guide.md` → v2 に書き換え（旧版は `archive/style_guide_v1.md` に保存）
- `article-status.md`: 凡例に「Published(下書きストック)」追加、更新ルール明文化、Last Updated更新
- `knowledge/03_workflow_framework.md`: 冒頭に「歴史的経緯文書。現行仕様は04が正」の注記追加
- `knowledge/01_paid_note_playbook.md`: Web検索痕跡トークン（U+E200区切りの `cite...` 63個・2,297文字）を機械除去。本文は無変更（diffで確認済み）
- `.claude/commands/publish.md`: 実行パスの正典をCLAUDE.md「実行環境」節に統一（1行）
- `README.md`: 実行パスを2環境併記に修正、ディレクトリ構成図を現行（articles/ ideas/ knowledge/ .claude/）に更新、テーマ選定を4柱に更新

### 削除（理由つき）
- `style_guide.md` v1 の「§1 ペルソナ」（一人称「僕」・敬体と常体を混ぜる）: 現行の人物像 `ideas/_self-inventory.md`（常体固定・効率を疑う実験者）と直接矛盾するため。v2では _self-inventory への参照に置換。**原文は archive/style_guide_v1.md に完全保存**
- `style_guide.md` v1 の「§8 テーマローテーション（曜日別）」: 形骸化済み。現行は `ideas/_netacho.md` の4柱運用。※同節内のアフィリエイト比較記事ノウハウ（3点構成・リンクコメント形式・構成テンプレ・テーマ候補）は**v2 §7 に全量継承**
- `article-status.md` の「アイデア／ドラフト」節の個別項目: 記載内容（断酒サイゼ＝仕上げ待ち）が投稿済み(#8)と矛盾。ネタの現況は `_netacho.md` が単一真実源のため参照に置換
- `README.md` の曜日ローテーション表: 同上

### 変更していないもの
- `.claude/commands/` の article / title / check-compliance / review（現行運用と一致・完成度が高い）
- `knowledge/02` / `knowledge/04`、`ideas/` 配下すべて、`articles/`・`drafts/` の記事本文、Pythonソース、`cookies.json`

### 未解決（ユーザー判断待ち）
- **★印の捏造本文記事4本**（article-status #2 AI外注14倍 / #3 Technics / #4 3週間 / #5 PC故障）が下書きのまま残存。「公開は本文の正直化が前提」ルールとの整合が宙づり。→ 正直化して公開 or 破棄 の判断が必要
- #28 / #30 の「試合事実要確認」も未処理
