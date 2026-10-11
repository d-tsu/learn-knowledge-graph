# 文書の検査・生成スクリプト

## 本文のMarkdown検査

`check-chapter-markdown.cjs` は `docs/chapters/` のローカルリンク、コードフェンス、強調の解釈を検査し、各ファイルのSHA-256も出力する。Node.jsと `marked` パッケージが必要である。利用する環境で `marked` を解決できる状態にして実行する。

```sh
node scripts/check-chapter-markdown.cjs
```

引数にJSONの保存先を渡せる。保存先の親フォルダは事前に作成する。章の内容の正しさ、Mermaidの描画、コード例の実行を確認するスクリプトではない。

## 案内・付録も含めたリンク検査

`check-document-links.cjs` はREADME・引き継ぎ・目次・編集計画・本文・付録・ひな形・実習READMEのリンク先とコードフェンスを検査する。Node.jsと`marked`が必要である。

```sh
node scripts/check-document-links.cjs
```

引数にJSONの保存先を渡せる。外部サイトの到達性と、ページ内の見出しへのリンクは検査しない。

## 本文の図の描画

`render-chapter-diagrams.cjs` は選択した本文のMermaid図を描画する。引数はローカルのMermaid 11.12.0、証跡の保存先、本文ファイルの順。PlaywrightとEdgeが必要である。

```sh
node scripts/render-chapter-diagrams.cjs path/to/mermaid.min.js reviews/assets/check docs/chapters/06-model-design.md
```

PNG・SVGとハッシュを保存し、PDFは生成しない。描画の成功とは別に、生成された図を目視して文字・矢印・本文との対応を確認する。

## 更新停止中のPDF関連

| スクリプト | 用途 |
|---|---|
| `render-mobile-diagrams.cjs` | 過去の読書用PDFに収録する図の描画 |
| `export-mobile-pdf.py` | 読書用PDFの生成 |
| `check-mobile-pdf.py` | 生成したPDFの検査 |

ユーザーの指定により、PDFの生成・更新は停止している。これらは過去の生成手順を残すためのスクリプトであり、通常の章執筆では実行しない。保存済み成果物の確認範囲は[過去の生成記録](../output/pdf/README.md)を参照する。
