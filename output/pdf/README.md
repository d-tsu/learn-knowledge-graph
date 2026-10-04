# スマホ読書版

生成日：2026-10-04。正本は `docs/chapters/` のMarkdown。PDFはこの時点の内容を確認するための派生資料です。

ユーザーの希望により更新を停止しています。保存済みPDFは、第2章に概念モデルとオントロジーの図を追加する前のスナップショットです。最新のMarkdownとは一致しません。以下の生成・確認記録は保存済みPDFに対する過去の記録であり、後続の本文修正を確認したものではありません。

| 資料 | ページ数 |
|---|---:|
| [序章](00-introduction-mobile.pdf) | 16 |
| [第1章](01-knowledge-representation-mobile.pdf) | 19 |
| [第2章](02-knowledge-organization-mobile.pdf) | 26 |
| [目次付きまとめ版](knowledge-graph-chapters-00-02-mobile.pdf) | 62 |

ページは108×180mm。日本語フォントを埋め込み、本文は10.7pt。本文・表の項目・復習・演習・解答例は省略していません。表の各行はカード形式へ、Mermaidの図は画像へ変換しました。横向きの関係図は関係を保って縦向きに配置しています。2026-10-02に追加・更新した図は維持し、今回は第2章のモデル比較・整理方法の一覧と、序章のデータの出所をたどる説明を反映しました。まとめ版にはクリックできる目次と章・節のしおりがあります。

## 確認範囲

- 章別3本とまとめ版の全123ページを画像へ変換し、コンタクトシートで文字・図・表・改ページを目視確認。
- 章別PDFとまとめ版について、元本文の文章・表のセルをPDFの抽出文字と照合。各章104・124・164項目、まとめ版392項目の欠落なし。図の文字は画像のため文字照合の対象外で、描画結果を目視確認。
- ページ外へはみ出す文字なし。しおり・リンク注釈の生成を確認。スマホ実機でのタップ操作・表示は未確認。
- 元本文のハッシュと生成ファイル情報は `mobile-export-manifest.json`、文字照合結果は `mobile-export-qa.json` に保存。
- 本文自体の独立レビューは[最新のレビュー記録](../../reviews/2026-10-04-organization.md)、[第1章の追加修正](../../reviews/2026-10-03-context-information.md)、[3章の全面改稿](../../reviews/2026-10-02-readability.md)を参照。今回のPDFレイアウトは作成エージェントが確認しており、別エージェントのレイアウトレビューは未実施。

## 再生成

WindowsのMeiryoフォントとEdgeを使用します。PythonにはReportLab、Pillow、pypdf、pdfplumber、Node.jsにはPlaywrightが必要です。Mermaid 11.12.0のUMD形式JavaScriptをローカルに用意します。実行環境によりPython・Node.js・Popplerのコマンド名は調整してください。

リポジトリのルートから、次の順に実行します。Playwrightが通常の検索パスにない場合は、その配置場所を `NODE_PATH` に指定します。

```powershell
node scripts/render-mobile-diagrams.cjs 'C:/path/to/mermaid-11.12.0.min.js' reviews/assets/YYYY-MM-DD
python scripts/export-mobile-pdf.py
pdftoppm -r 110 -png output/pdf/knowledge-graph-chapters-00-02-mobile.pdf tmp/pdfs/page
python scripts/check-mobile-pdf.py
```

`render-mobile-diagrams.cjs`の第2引数は、元の向きのSVG/PNGを保存する証跡フォルダです。省略もできます。Markdownのリンク・フェンス・強調は `node scripts/check-chapter-markdown.cjs` で確認できます。この確認にはmarkedも必要です。

PDFの更新を再開する場合は、章別PDFも `pdftoppm` で全ページ画像へ変換し、まとめ版と合わせて確認してください。`tmp/pdfs/` の全ページ画像・コンタクトシートを確認し、必要な修正後に再生成します。確認済みの結果だけを `mobile-export-qa.json` に保存し、一時ファイルは作業後に削除します。再生成時は、PDF・生成日・ハッシュ・ページ数・確認記録も更新してください。生成日はスクリプトの `EXPORT_DATE` で設定します。現在は本文を更新してもPDFを再生成しません。
