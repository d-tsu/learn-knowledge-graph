# 文書の検査・生成スクリプト

## 本文のMarkdown検査

`check-chapter-markdown.cjs` は `docs/chapters/` のローカルリンク、コードフェンス、強調の解釈を検査し、各ファイルのSHA-256も出力する。Node.jsと `marked` パッケージが必要である。利用する環境で `marked` を解決できる状態にして実行する。

```sh
node scripts/check-chapter-markdown.cjs
```

引数にJSONの保存先を渡せる。保存先の親フォルダは事前に作成する。章の内容の正しさ、Mermaidの描画、コード例の実行を確認するスクリプトではない。

## 更新停止中のPDF関連

| スクリプト | 用途 |
|---|---|
| `render-mobile-diagrams.cjs` | 過去の読書用PDFに収録する図の描画 |
| `export-mobile-pdf.py` | 読書用PDFの生成 |
| `check-mobile-pdf.py` | 生成したPDFの検査 |

ユーザーの指定により、PDFの生成・更新は停止している。これらは過去の生成手順を残すためのスクリプトであり、通常の章執筆では実行しない。保存済み成果物の確認範囲は[過去の生成記録](../output/pdf/README.md)を参照する。
