# ナレッジグラフ・オントロジー学習ノート

知識の表現・整理・意味を基礎から学び、AIエージェントによる実装やテスト作成への応用を考える日本語の学習資料です。まず理論と方法を学び、その後に技術比較と小さな実証へ進みます。

## 読み始める

[序章](docs/chapters/00-introduction.md)から章番号の順に読み進めてください。各章には到達点、具体例、復習、演習と解答例があります。図の表示にはMermaid対応のMarkdownビューアが必要です。

構成は[合意済み目次](OUTLINE.md)に従います。序章・5部17章の本文と[付録](docs/appendices/README.md)を用意しました。

| 章 | 本文 | 学べること |
|---|---|---|
| 序章 | [この資料の目的と読み方](docs/chapters/00-introduction.md) | 学習ルート、開発への応用題材、事実と仮説 |
| 1 | [知識を表現するとは](docs/chapters/01-knowledge-representation.md) | データ・情報・知識、対象・名前・ID、事実と規則 |
| 2 | [知識を整理するさまざまな方法](docs/chapters/02-knowledge-organization.md) | 語彙・分類・モデル、関係図・条件表・手順 |
| 3 | [ナレッジグラフの基礎](docs/chapters/03-knowledge-graphs.md) | 関係探索、同一性、PG/RDF、表や文書検索との比較 |
| 4 | [オントロジーの基礎](docs/chapters/04-ontologies.md) | クラス・個体・プロパティ、公理、定義と個別の記録 |
| 5 | [推論・制約・不確実性](docs/chapters/05-reasoning-and-constraints.md) | 探索・推論・検証・計画、不明・否定・矛盾、日時と適用条件 |
| 6 | [問いからモデルを設計する](docs/chapters/06-model-design.md) | 問い・粒度・条件・外部参照・語彙の再利用 |
| 7 | [文書・データ・コードから知識を構築する](docs/chapters/07-knowledge-construction.md) | 原文の構造・条件を保ち、抽出候補を照合・確認する |
| 8 | [知識の品質とライフサイクル](docs/chapters/08-quality-and-lifecycle.md) | 根拠・確認状態・改訂・撤回を管理する |
| 9 | [データモデル・標準・問い合わせ言語](docs/chapters/09-models-and-languages.md) | RDFの構文・問い合わせ・推論・制約を小例で確かめる |
| 10 | [保存・問い合わせ基盤](docs/chapters/10-storage-and-query.md) | 保存・索引・問い合わせ・推論と、基盤・運用の分担 |
| 11 | [編集・構築・推論・検証のツール](docs/chapters/11-editing-and-validation-tools.md) | 編集・構築・推論・検証ツールの入出力と組合せ |
| 12 | [AI・AIエージェント向けの知識活用技術](docs/chapters/12-ai-knowledge-use.md) | 検索方式・根拠付き回答・記憶・MCPの役割 |
| 13 | [開発知識のモデル化](docs/chapters/13-development-model.md) | 開発資産の根拠付き対応、仕様と実装、値の受け渡し |
| 14 | [AIによる設計・コード生成への適用](docs/chapters/14-design-and-code-generation.md) | 作業に必要な根拠の提供と生成物の検証 |
| 15 | [結合・システムテストへの適用](docs/chapters/15-integration-testing.md) | 複数設計の条件から入力と準備レコードを求める |
| 16 | [効果を評価する](docs/chapters/16-evaluation.md) | 同じ問い・原本による品質と総工数の比較 |
| 17 | [小さく始めて発展させる](docs/chapters/17-incremental-practice.md) | 原本から構築・問い合わせ・根拠検査・更新・JSON出力を一巡する |

本文はMarkdownを正本とします。章別レビューに加え、独立エージェントが全18章を順に読み、[指摘への対応と再確認](reviews/2026-10-11-book-review.md)を終えました。各改稿の確認範囲と未確認事項は[レビュー一覧](reviews/README.md)から確認してください。レビュー済みであることは、読者理解や実製品での効果を実証したことを意味しません。

## 資料の置き場所

| 場所 | 内容 |
|---|---|
| [docs/chapters/](docs/chapters/) | 章番号順に読む本文 |
| [docs/appendices/](docs/appendices/README.md) | 用語集、一次資料、ツール比較、実習補足、追加演習 |
| [OUTLINE.md](OUTLINE.md) | 合意済み目次と編集方針 |
| [docs/EDITORIAL_PLAN.md](docs/EDITORIAL_PLAN.md) | 全章の執筆状況、旧草稿との対応、文章上の注意 |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | 執筆・改稿の更新履歴 |
| [examples/](examples/) | 実行できる小例と応用題材の整理案 |
| [templates/](templates/) | 設計知識・技術調査・比較評価のひな形 |
| [drafts/](drafts/README.md) | 再編前の旧草稿 |
| [reviews/](reviews/README.md) | セルフレビュー・独立レビュー・公開前点検の記録 |
| [reviews/assets/](reviews/assets/) | 図の描画結果と検査の証跡 |
| [scripts/](scripts/README.md) | Markdown検査と過去の成果物生成スクリプト |
| [output/](output/) | 保存済みの派生成果物。PDFの更新は停止中 |

本文で使う例は、特記がなければ架空の教材です。[権限と画面をまたぐ条件分岐](examples/conditional-screen-flow.md)は、複数の設計書からテストの前提を集める応用題材です。未定義の仕様は確定事項と分けて記録しています。

付録とひな形の確認範囲も[レビュー一覧](reviews/README.md)に記録しています。旧草稿・補助題材全体を確認済みとするものではありません。保存済みPDFは過去のスナップショットであり、現在の本文を読む入口には使いません。

## 執筆を続ける

全章の初稿をそろえました。改稿の再開時は[作業引き継ぎ](HANDOFF.md)、[編集計画](docs/EDITORIAL_PLAN.md)、[レビュー方針](REVIEW_POLICY.md)を確認してください。[図の追加候補](docs/DIAGRAM_PROPOSALS.md)には理由と採否をまとめています。

mainを共有の基準とし、一章ごとにブランチを作って執筆します。本文・演習・必要な確認・独立レビュー・指摘対応を終えたらmainへマージします。具体的な手順は[CONTRIBUTING.md](CONTRIBUTING.md)にまとめています。

RDFの問い合わせ・逆関係の推論・SHACL検証、画面フローの条件計算、原本からの構築と更新をローカルで確認しました。手順は[実習一覧](docs/appendices/practice-and-formalization.md)にあります。実製品・外部AIへの接続と効果測定、復習用スライドは今後の作業です。PDFの再生成はユーザーの希望があるまで停止します。
