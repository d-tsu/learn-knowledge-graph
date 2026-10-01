# スマホ読書版

生成日：2026-10-01。正本は `docs/chapters/` のMarkdown。PDFはこの時点の内容を確認するための派生資料です。

| 資料 | ページ数 |
|---|---:|
| [序章](00-introduction-mobile.pdf) | 12 |
| [第1章](01-knowledge-representation-mobile.pdf) | 14 |
| [第2章](02-knowledge-organization-mobile.pdf) | 15 |
| [目次付きまとめ版](knowledge-graph-chapters-00-02-mobile.pdf) | 42 |

ページは108×180mm。日本語フォントを埋め込み、本文は10.7pt。本文・表の項目・復習・演習・解答例は省略していません。表の各行はカード形式へ、Mermaidの関係図は関係を保って縦向きの画像へ変換しました。まとめ版にはクリックできる目次と章・節のしおりがあります。

## 確認範囲

- まとめ版を全42ページ画像へ変換し、文字・図・表・改ページを目視確認。
- 章別PDFとまとめ版について、元本文の文章・表のセルをPDFの抽出文字と照合。各章74・92・94項目、まとめ版260項目の欠落なし。図の文字は画像のため文字照合の対象外で、描画結果を目視確認。
- ページ外へはみ出す文字なし。しおり・リンク注釈の生成を確認。スマホ実機でのタップ操作・表示は未確認。
- 元本文のハッシュと生成ファイル情報は `mobile-export-manifest.json`、文字照合結果は `mobile-export-qa.json` に保存。
- 本文自体の独立レビューは `reviews/2026-10-01-foundations.md` を参照。今回のPDFレイアウトは作成エージェントが確認しており、別エージェントのレイアウトレビューは未実施。

## 再生成

WindowsのMeiryoフォントとEdgeを使用します。PythonにはReportLab、Pillow、pypdf、pdfplumber、Node.jsにはPlaywrightが必要です。Mermaid 11.12.0のUMD形式JavaScriptをローカルに用意します。実行環境によりPython・Node.js・Popplerのコマンド名は調整してください。

リポジトリのルートから、次の順に実行します。Playwrightが通常の検索パスにない場合は、その配置場所を `NODE_PATH` に指定します。

```powershell
node scripts/render-mobile-diagrams.cjs 'C:/path/to/mermaid-11.12.0.min.js'
python scripts/export-mobile-pdf.py
pdftoppm -r 110 -png output/pdf/knowledge-graph-chapters-00-02-mobile.pdf tmp/pdfs/page
python scripts/check-mobile-pdf.py
```

`tmp/pdfs/` の全ページ画像・コンタクトシートを確認し、必要な修正後に再生成してください。確認済みの結果だけを `mobile-export-qa.json` に保存し、一時ファイルは作業後に削除します。本文を更新した場合は、PDF・生成日・ハッシュ・ページ数・確認記録も更新してください。日付とまとめ版の説明は現在の版に合わせてスクリプト内に設定されています。
