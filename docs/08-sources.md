# 参照資料・調査台帳

確認日：2026-09-26。原則として標準仕様、提供元の文書、プロジェクトのリポジトリを参照した。製品の実機検証は行っていない。リンク先の最新版は更新されるため、実証時には使用バージョン・タグ・設定を固定する。

## 基礎・標準

| 資料 | 読む目的 |
|---|---|
| [W3C RDF 1.1 Primer](https://www.w3.org/TR/rdf11-primer/) | トリプル、IRI、RDFSの基礎 |
| [W3C OWL 2 Primer](https://www.w3.org/TR/owl2-primer/) | クラス、公理、開世界の意味 |
| [W3C SHACL](https://www.w3.org/TR/shacl/) | データ品質制約 |
| [W3C SPARQL 1.1](https://www.w3.org/TR/sparql11-query/) | パターン問い合わせ |
| [W3C PROV-O](https://www.w3.org/TR/prov-o/) | 根拠・由来のモデル |
| [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture) | AIアプリへの接続 |

ここでは基礎学習に使う版を明示している。各標準の最新動向を網羅した一覧ではない。

## 保存・編集・検証

| 資料 | 確認した範囲 |
|---|---|
| [Neo4j Graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) | プロパティグラフの構成 |
| [GraphDB 11.0 documentation](https://graphdb.ontotext.com/documentation/11.0/) | 製品の位置付け。11.0を参照したのであり最新版との断定ではない |
| [Apache Jena](https://jena.apache.org/) | RDF API、TDB、Fuseki、推論 |
| [Eclipse RDF4J](https://rdf4j.org/) | Java RDFフレームワーク |
| [Stardog Inference](https://docs.stardog.com/inference-engine/) | 問い合わせ時推論 |
| [Amazon Neptune user guide](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html) | モデル、対応言語、DatabaseとAnalyticsの区別 |
| [JanusGraph documentation](https://docs.janusgraph.org/) | 分散グラフの位置付け |
| [Memgraph documentation](https://memgraph.com/docs) | 製品と問い合わせの入口 |
| [Protégé](https://protege.stanford.edu/) | OWL編集と共同編集 |
| [RDFLib](https://rdflib.readthedocs.io/en/stable/) | Python RDF処理 |
| [pySHACL](https://github.com/RDFLib/pySHACL) | SHACL検証 |
| [Apache TinkerPop](https://tinkerpop.apache.org/) | グラフ処理、Gremlin |
| [NetworkX](https://networkx.org/documentation/stable/) | Pythonグラフ処理 |

## 構築・AI利用

| 資料 | 確認した範囲 |
|---|---|
| [Neo4j LLM Graph Builder](https://github.com/neo4j-labs/llm-graph-builder) | 非構造化データのグラフ構築 |
| [Neo4j GraphRAG Python](https://neo4j.com/docs/neo4j-graphrag-python/current/) | 検索・生成ライブラリ |
| [Microsoft GraphRAG](https://microsoft.github.io/graphrag/) | プロジェクトの概要 |
| [LlamaIndex Property Graph Index](https://developers.llamaindex.ai/python/framework/module_guides/indexing/lpg_index_guide/) | 抽出・保存・検索の構成 |
| [Graphiti](https://github.com/getzep/graphiti) | 時間を扱うエージェント向け知識グラフ |
| [Graphify指定サイト](https://graphify.net/) | 紹介機能と導入記述の不一致。配布物との対応は未確定 |

## 未確認事項と次の調査

- 製品間の性能・抽出品質・維持費の比較。サイトの宣伝値から順位は付けない。
- エディション別の機能、利用条件、配置環境、更新頻度、運用上の制約。
- Graphifyのサイト・リポジトリ・パッケージ・リリースの対応と実際の入出力。
- 日本語の業務設計書からの否定・例外・表の条件の抽出品質。
- 静的解析で取得した関係と、業務オントロジーの関係を結ぶ方法。

TrikeDBは今回の対象外。普及度に関する定量調査は未実施。本資料の分類は学習と比較の入口である。
