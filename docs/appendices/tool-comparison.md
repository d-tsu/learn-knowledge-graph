# 技術・ツール比較

確認日：2026-10-11。代表例を役割ごとに比べる。各公式資料で役割を確認した一覧であり、性能・費用・実運用の優劣を実測した表ではない。リンク先の対象版と、導入する配布物・エディションの利用条件は導入時に固定する。

## 保存・問い合わせ基盤

| 候補・公式資料 | モデルと接続 | 構成上の注意 | 利用条件で確認する点 |
|---|---|---|---|
| [Neo4j](https://neo4j.com/docs/getting-started/) | PG・Cypher、ドライバから問い合わせ | 使用する索引・制約・権限を試す | Community・Enterprise・Auraでの機能と契約の違い |
| [Memgraph](https://memgraph.com/docs/) | PG・Cypher | 必要なCypher構文と他製品からの移行を試す | 配布版・追加機能ごとのライセンスと提供条件 |
| [JanusGraph](https://docs.janusgraph.org/) | PG・Gremlin | 保存・索引用のバックエンドも運用対象 | 本体に加え、各バックエンドの条件 |
| [GraphDB](https://graphdb.ontotext.com/documentation/11.5/) | RDF・SPARQL | 推論の設定、投入・更新・削除を試す | エディション別の機能・容量・利用条件 |
| [Stardog](https://docs.stardog.com/) | RDF・SPARQLを中心とする基盤 | 推論・検査・外部データ接続の構成を確認 | 配置方式と契約、利用する機能の条件 |
| [Apache Jena](https://jena.apache.org/documentation/) | RDF・SPARQL。TDB2で保存、FusekiでHTTP提供 | 部品の構成、認証・復旧を利用側で設計 | 対象配布物と同梱依存物のライセンス |
| [Eclipse RDF4J](https://rdf4j.org/documentation/) | JavaのRDF処理、Repository API・SPARQL | 組込みかサーバー利用かを選ぶ | 対象配布物と拡張ストアのライセンス |
| [Amazon Neptune](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html) | PGのGremlin・openCypher、RDFのSPARQL | 選択したモデル・APIとサービス制限を確認 | クラウドの課金・リージョン・接続条件 |

DBを選ぶ前に、第10章の問い・更新・復旧の小さな検証を行う。ライセンス条文の適合判定や料金の見積りは、この資料では実施していない。

## 編集・構築・検査・AI接続

| 候補・公式資料 | 入出力と役割 | 連携・限界と確認する点 |
|---|---|---|
| [Protégé](https://protege.stanford.edu/) | クラス・関係の編集 → OWLファイル | Desktop／Webの配置・共同編集・承認方法 |
| [RDFLib](https://github.com/RDFLib/rdflib) | RDFの読書き・SPARQL | 第9・17章で7.1.4を実行。公開APIや権限は別途設計 |
| [OWL-RL](https://github.com/RDFLib/OWL-RL) | RDFと規則 → 帰結の追加 | 第9章で7.1.4の逆関係を実行。他のOWL公理も同じ範囲で扱えるとは限らない |
| [pySHACL](https://github.com/RDFLib/pySHACL) | データとshape → 適合・違反報告 | 0.30.1で実習。推論の有無と検査対象を固定 |
| [HermiT](https://github.com/phillord/hermit-reasoner)／[ELK](https://github.com/liveontologies/elk-reasoner) | 公理・事実 → 推論結果 | 対応公理・処理を照合。ELKはOWL 2 ELの一部に対応 |
| [LLM Graph Builder](https://github.com/neo4j-labs/llm-graph-builder) | 文書 → グラフの候補 | モデルとの対応、原文位置、モデル提供元への送信と費用を確認 |
| [Graphviz](https://graphviz.org/documentation/)／[NetworkX](https://networkx.org/documentation/stable/) | グラフ → 描画／分析結果 | 図の分かりやすさや業務上の重要性は別に評価 |
| [Microsoft GraphRAG](https://microsoft.github.io/graphrag/)／[Neo4j GraphRAG](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html) | 文書・グラフ → 検索と生成の材料 | 名称が同じでも処理は異なる。原本・基準方式と比較 |
| [Graphify](https://github.com/Graphify-Labs/graphify) | コード・文書 → 関係を調べる材料 | 指定サイトとの対応を確認。コードの関係を承認済み仕様へ置き換えない |
| [Graphiti](https://github.com/getzep/graphiti) | エピソードなど → 更新する知識・記憶 | 取得日時・適用日時と、設計知識の承認状態を分ける |

実習の三ライブラリ以外は、この資料で製品の導入・性能試験をしていない。外部サービスへ送る内容、APIキーの管理、商用利用・再配布・依存物の条件を、[技術調査ひな形](../../templates/tool-review.md)へ記録する。

[付録一覧へ](README.md)
