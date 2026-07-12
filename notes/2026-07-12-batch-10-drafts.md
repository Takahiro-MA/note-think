# 2026-07-12 下書きストック補充：10本一括執筆・投稿

## やったこと
ストック枯渇のため、📝ネタ帳から10本を一括で執筆→note下書き投稿（全て `type: free / status: draft`）。
並列サブエージェント10体で執筆し、`style_guide.md`（v2・エッジ規律§2.5）＋`_self-inventory.md`＋各ネタを読ませて生成。
投稿は frontmatter＋H1を除去し本文のみを `create_draft`（H1をタイトルに）。

## 投稿した10本（note_id）
| slug | note_id | 柱 | 備考 |
|------|---------|----|------|
| health-checkup-interpretation | 169679847 | 柱2 flagship | ⚠️医療最センシティブ・コクランは紹介止め・免責付 |
| irrationality-value | 169679848 | 柱2 最上位 | 非合理の価値・錨=ギター/釣り/真空管 |
| oshi-attachment-margin | 169679849 | 柱2 余白 | 推し=愛着・★娘描写は公開前に本人確認 |
| mct-fat-burn-myth | 169679850 | 柱2 脂質 | ⚠️薬機法特に厳格・ANTI-hype・免責付 |
| coffee-bean-discomfort | 169679851 | 柱2 違和感 | サイゼと地続き |
| deadlift-hip-hinge-feel | 169679853 | 柱2 身体観察 | #19と芯を書き分け（見た目≠身体感覚） |
| yen-weak-travel | 169679854 | 柱3 旅/お金 | 山形コスパで差別化・国名フラット |
| ai-engineer-value | 169679856 | 柱4 本職 | ML/DNN切り分けが差別化 |
| value-beyond-productivity | 169679857 | 柱4 横断 | 生産性でない・AI時代の人間の価値クラスタ |
| stoicism-misused | 169679858 | 柱2 規律の罠 | #35(楽しみ側)と芯を書き分け |

## 品質・コンプラ
- 全10本 文字化けなし／です・ます混入なし（免責文除く）を grep 確認。
- 健康系3本（健診・MCT・デッドリフト）は n=1＋一般知見・効能断定回避・末尾免責を徹底。
- 公開前に `/check-compliance`（特に health-checkup・mct）を通すのが安全。公開・価格設定・有料ラインは note 画面で人間が実施。

## 状態反映
- `article-status.md` に #37〜46 追記・Last Updated=2026-07-12。
- 各ネタ frontmatter を `status: done`（note_id付）に。
- `_netacho.md` の該当 📝/💡 を ✅（note_id・articlesパス）に更新。柱2「効率が奪う余白」クラスタと柱4「AI時代の人間の価値」ミニクラスタが揃い、マガジン化/内部リンク導線の候補に。

## 保留・次アクション
- **Zettelkasten化の相談は保留中**（テーマ(クラスタ)をノード化して双方向リンク＝案2を推奨。ユーザー回答待ち）。
- oshi記事の「双子の娘」描写の出し方は公開前に本人確認。
- 欧州サッカー（`euro-football-oshi-club.md`）は⚠️要ファクト確認のため今回の10本から除外（書く前に順位/監督/移籍を裏取り）。
