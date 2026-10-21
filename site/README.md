# Web版の管理

本文の正本は既存のMarkdown、Web表示はmdBook、配信先は[GitHub Pages](https://d-tsu.github.io/learn-knowledge-graph/)である。PDFの生成・更新は行わない。

## 構成

| ファイル | 役割 |
|---|---|
| [`../book.toml`](../book.toml) | 日本語タイトル、テーマ、図、検索の設定 |
| [`SUMMARY.md`](SUMMARY.md) | OUTLINEに沿った章・付録・実習・ひな形の並び |
| [`reader.css`](reader.css) | 日本語本文、表、図、スマホ幅の表示 |
| [`mermaid-init.js`](mermaid-init.js) | 図の描画とテーマ切替。大きな図は横スクロールで読む |
| [`reader-search.js`](reader-search.js) | 日本語の部分一致検索。空白で区切った語はすべて含む箇所を探す |
| [`../scripts/build-book.py`](../scripts/build-book.py) | 正本から公開用ソースを用意し、サイトと検索データを生成する |
| [`../scripts/check-book.py`](../scripts/check-book.py) | 生成HTMLと検索結果の内部リンクを検査する |
| [`../.github/workflows/book.yml`](../.github/workflows/book.yml) | mainの更新時にビルド・検査・公開する。PRではビルドと検査のみ行う |

本文・付録の全Markdownが目次に含まれることを生成時に検査する。章を増やす場合はSUMMARYも更新する。実習・ひな形は読み物として選んだファイルを列挙する。

公開用の一時ソースは `tmp/book-src/`、HTMLは `tmp/book/` に作る。これらのフォルダーは生成ごとに作り直す。SUMMARYで指定したファイルだけを取り込み、旧草稿、レビュー証跡、PDF、ローカル環境をサイトへコピーしない。目次にない文書や実習コードへのリンクは、生成時にGitHubのmainへのリンクに変換する。元のMarkdownは書き換えない。

READMEの公開先はmdBookの仕様に合わせて `index.html` とする。本文内のREADMEへのリンクも生成時に合わせる。検索索引は生成HTMLの本文と見出しIDから作り、ブラウザー内で検索する。検索に外部APIは使わない。

## ローカルで生成・確認する

Python 3.11以上と、次の公式リリースの実行ファイルを用意する。

- [mdBook 0.5.4](https://github.com/rust-lang/mdBook/releases/tag/v0.5.4)
- [mdbook-mermaid 0.17.1](https://github.com/badboy/mdbook-mermaid/releases/tag/v0.17.1)

実行ファイルはPATHに置くか、リポジトリの `tmp/mdbook-tools/` に展開する。リポジトリのルートで次を実行する。

```sh
python scripts/build-book.py
python scripts/check-book.py
python -m http.server 8000 --bind 127.0.0.1 --directory tmp/book
```

ブラウザーで `http://127.0.0.1:8000/` を開く。終了はCtrl+C。ファイルを編集した場合は生成・検査を再実行してブラウザーを更新する。`mdbook build` だけでは一時ソースと日本語検索索引が更新されないため、通常は `build-book.py` を使う。

ブラウザーによる自動確認にはNode.js、PlaywrightパッケージとMicrosoft Edgeも必要である。

```sh
node scripts/check-book-browser.cjs
```

結果とスクリーンショットは `tmp/book-browser/` に保存する。この検査は実機のスマートフォンを使うものではなく、デスクトップのEdgeで390×844の表示領域を再現する。`BOOK_BASE_URL` に末尾 `/` 付きの公開URLを設定すると、同じ検査を公開サイトに対して実行できる。

mdbook-mermaidはビルド対象のmdBook 0.5.0と使用版0.5.4の差を警告する。この組合せで実際の生成・図の描画を確認した。版を更新する場合は図と検索も再確認する。

## GitHub Pagesへの公開

GitHubのリポジトリ設定で、PagesのSourceをGitHub Actionsにする。`main` へのpushで、固定版のツールを取得し、生成と内部リンク検査に成功したHTMLを公開する。生成したHTMLをGitにコミットする必要はない。

公開先は `https://d-tsu.github.io/learn-knowledge-graph/`。リポジトリ名や公開先を変える場合は `book.toml` の `site-url`、READMEのURL、`check-book.py` と `check-book-browser.cjs` のパス接頭辞も更新する。

ローカルの作業ブランチとPRでは公開せず、本文の執筆・合流は引き続き[CONTRIBUTING](../CONTRIBUTING.md)に従う。公開後はActionsの完了状態と実際の公開ページを確認する。
