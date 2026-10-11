# 用語集

短い意味を調べるための一覧である。細かな条件や例は各章を参照する。

| 用語 | この資料での意味 | 説明 |
|---|---|---|
| 文脈 | 値や記述を理解するための対象・意味・日時などの情報 | [1章](../chapters/01-knowledge-representation.md) |
| 対象・識別子 | 個別に扱うものや出来事と、それを区別するための値 | [1章](../chapters/01-knowledge-representation.md) |
| 属性・関係 | 対象の特徴を値で表す方法と、対象どうしのつながりを表す方法 | [1章](../chapters/01-knowledge-representation.md) |
| 統制語彙 | 登録・検索に使う名称と別名を管理する仕組み | [2章](../chapters/02-knowledge-organization.md) |
| タクソノミー・シソーラス | 階層的な分類と、検索用の階層・関連関係の整理 | [2章](../chapters/02-knowledge-organization.md) |
| 概念モデル | 扱う対象や出来事の種類、関係、その意味を整理したモデル | [2章](../chapters/02-knowledge-organization.md) |
| オントロジー | 共有する概念と関係、それらについての定義を明示したもの | [2章](../chapters/02-knowledge-organization.md)、[4章](../chapters/04-ontologies.md) |
| ナレッジグラフ | 対象と意味付きの関係によって知識を表すもの | [3章](../chapters/03-knowledge-graphs.md) |
| PG | プロパティグラフ。ノードや関係に属性を持たせる表現 | [3章](../chapters/03-knowledge-graphs.md)、[9章](../chapters/09-models-and-languages.md) |
| RDF・トリプル | 主語・述語・目的語の三項から知識を表すモデルと、その一組 | [9章](../chapters/09-models-and-languages.md) |
| クラス・個体 | 対象を分類する区分と、その区分に属する特定の対象 | [4章](../chapters/04-ontologies.md) |
| 公理・推論 | 意味の前提となる記述と、その記述・事実から帰結を導く処理 | [4章](../chapters/04-ontologies.md)、[5章](../chapters/05-reasoning-and-constraints.md) |
| 開世界仮定 | 記録されていないことを、直ちに偽とはしない考え方 | [5章](../chapters/05-reasoning-and-constraints.md) |
| 閉世界仮定 | 指定した範囲の記録を完全とみなし、未記録のものをないものとして扱う考え方 | [5章](../chapters/05-reasoning-and-constraints.md) |
| 制約検証 | データが指定した必要項目や値の条件を満たすか調べる処理 | [5章](../chapters/05-reasoning-and-constraints.md)、[9章](../chapters/09-models-and-languages.md) |
| コンピテンシー・クエスチョン | モデルで答えたい具体的な問い | [6章](../chapters/06-model-design.md) |
| 粒度 | 何を一つの対象・出来事として区切るか | [6章](../chapters/06-model-design.md) |
| 来歴 | 原本、抽出、判断、更新など、その記録ができるまでの経緯 | [8章](../chapters/08-quality-and-lifecycle.md) |
| IRI・リテラル・空白ノード | RDFで使う識別子、文字列や数値、グラフ内で名を持たない対象の表現 | [9章](../chapters/09-models-and-languages.md) |
| Turtle・JSON-LD | RDFをファイルなどへ記述する構文 | [9章](../chapters/09-models-and-languages.md) |
| RDFS・OWL・SKOS・SHACL | 語彙定義、オントロジー記述、検索用概念の整理、制約検証を担う語彙・言語 | [9章](../chapters/09-models-and-languages.md) |
| SPARQL・Cypher・Gremlin | RDFやPGに対する問い合わせ・グラフ操作の言語 | [9章](../chapters/09-models-and-languages.md) |
| プロファイル | 推論の目的に合わせて使う表現を限定した言語の範囲 | [9章](../chapters/09-models-and-languages.md) |
| RDFストア | RDFの保存と問い合わせを提供する基盤 | [10章](../chapters/10-storage-and-query.md) |
| RAG・GraphRAG | 検索した根拠を生成へ渡す方法と、そこにグラフを使う方法群 | [12章](../chapters/12-ai-knowledge-use.md) |
| 埋め込み | 文や対象を数値の並びへ変換した表現 | [12章](../chapters/12-ai-knowledge-use.md) |
| 作業用の文脈 | 特定の作業に必要な仕様・制約・根拠・不足情報のまとまり | [14章](../chapters/14-design-and-code-generation.md) |
| トレーサビリティ | 要件・設計・実装・テストなどの対応を追跡できること | [13章](../chapters/13-development-model.md) |
| 計画・制約充足 | 操作の前提・結果から順序を求める処理と、複数条件を満たす値を求める処理 | [15章](../chapters/15-integration-testing.md) |
| テストオラクル | 実行結果の正しさを判定する根拠や仕組み | [15章](../chapters/15-integration-testing.md) |
| 適合率・再現率 | 取得した候補のうち正しい割合と、正解全体のうち取得できた割合 | [16章](../chapters/16-evaluation.md) |

[付録一覧へ](README.md)
