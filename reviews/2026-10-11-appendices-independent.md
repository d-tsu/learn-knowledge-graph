# 付録・ひな形の独立レビュー

実施日：2026-10-11。基準は `OUTLINE.md` と `REVIEW_POLICY.md`（更新日2026-10-01、ユーザー確認済み）。対象読者はソフトウェア開発経験のある、ナレッジグラフ・オントロジーの初学者。

執筆者：親エージェント `/root`。独立レビュアー：執筆に参加していない別エージェント `/root/appendices_independent`。会話履歴を引き継がない新しい文脈で依頼を受け、セルフレビューの結果や期待する結論を受け取らずに確認した。本文・付録・ひな形は編集していない。

初回結果：高0件、中0件、低1件。指定範囲の独立レビューを完了した。低指摘AP-01の採否と理由は執筆者の対応欄へ追記する。以下の確認は読者理解・製品効果・ライセンス適合の実証を意味しない。

## 対象と固定確認

対象は `tmp/appendices-review-manifest.json` に列挙された全9ファイル。manifestのSHA-256は `79a274ab161f829e0700cd8739e0ee203acc6c6abc57272a91d6d51f2a87c783`。開始時と終了時にmanifestと全9ファイルを再計算し、すべて依頼時の値に一致した。

| ファイル | SHA-256（開始・終了で同一） |
|---|---|
| docs/appendices/glossary.md | `58919090ca17f4ce2ece6630a464e88507431007c2fb6394ce2493a398eff3cb` |
| docs/appendices/practice-and-formalization.md | `99c244b3abddd11fab52081939765099c592a461332ce9f3e88c22632cec26a4` |
| docs/appendices/README.md | `d99a712f53334a28fdf54b05f47366f22f2a5f67bf84e05511924b6b37d41f12` |
| docs/appendices/sources.md | `6a074594afbd4d2508692d26f71409dd5b0c11f26b0b5340552890e7708583fa` |
| docs/appendices/templates-and-exercises.md | `469e6b9968f00e4bfaa9cf9e26a6ac1c17ac8745ec4f67bd71a8967267ba736c` |
| docs/appendices/tool-comparison.md | `f2c7254c8b11d8834117ff2492be51cbd49e08bc9ec850191b4d76720af803e3` |
| templates/evaluation-record.md | `1348242bd138ad8893619dc9afe3b0d632a7b117735ea586ac7a519852a20fe7` |
| templates/knowledge-record.md | `114d6b0f7bd0a05ebcb829616e963dd819351f8468f5aff6ab94d2924efa7cbb` |
| templates/tool-review.md | `348ebbb2b09bf37654183c208dfafc1c2355d65a3312a46b0dd8c84b01434201` |

9ファイルは全文を確認した。本文0〜17章は用語・題材・説明の担当箇所を検索し、定義と関連段落を照合した。特に2・4・5章の分類・公理・未知、6〜8章の主張・来歴・承認・撤回、9〜12章の技術とツール、13〜17章の開発対応・条件計算・比較評価・実習を参照した。全18章を今回あらためて全面レビューしたという意味ではない。

## 方針の観点ごとの結果

| 観点 | 結果 | 確認した内容 |
|---|---|---|
| 初出の用語 | 問題なし | 用語集は短い意味と本文参照を提供する。付録のEL・QL・RLはプロファイルの説明と用途表を伴う。英語の列挙だけで理解を要求していない |
| 前提と学習順序 | 問題なし | 本文を読み進め、必要時に参照する付録という位置付けが明確。実習は各READMEに入口がある |
| 説明の十分さ | 問題なし | ツールの役割・入出力・導入前の確認をそろえている。ひな形の全項目を必須にせず、根拠・版・状態を保つ説明がある |
| 正確性 | 問題なし | 一種と一部、存在の公理と記載検査、探索と制約充足、明記・導出・推測と承認を区別している |
| 根拠と断定 | 指摘あり（低） | AP-01は原典の節案内のずれ。製品の公式説明、教材の計算、実運用の実測は区別されている |
| 具体例・図・表 | 問題なし／図の描画は対象外 | 分類、原本撤回、仕様と実装の境界、総工数の例が本文と一致。対象9ファイルにMermaid図・画像はない |
| 復習・演習 | 問題なし | 四つの追加演習は状況・問い・理由付き解答を持つ。演習3は同額と1円超で設計と実装の境界差を調べられる |
| 構成と範囲 | 問題なし | OUTLINEの用語集・原典・役割別比較・対象版付き実習・形式化補足・ひな形・追加演習を扱う。後続スライドとPDF停止も明記 |
| 章間の整合 | 問題なし（対象との関係） | 用語集の参照先は存在し、本文の定義と大きな矛盾がない。3ひな形は6〜8・10〜12・16章の記録方法と整合 |
| 読みやすさ | 問題なし | 短い案内と比較表が中心で、不要な説明の追加を要求する箇所は認めなかった |
| 技術的な体裁 | 確認範囲で問題なし | ローカルリンク54件は参照先が存在。コードフェンスはknowledge-recordのYAML一組のみで閉じている。3実習の実行結果は下記のとおり |

## 指摘

### AP-01：原典の節案内に基本的な公理の説明箇所が含まれない

- 重要度：低。
- 観点：根拠と断定、技術的な体裁。
- 箇所：`docs/appendices/practice-and-formalization.md`、見出し「OWLの表現を増やす前に」、28行。該当箇所：「詳細はOWL 2 Primer §5–8で確認する」。影響範囲は直前の表（23〜26行）。
- 問題：表の分類の引継ぎ・排他性・関係の相手のクラスは、それぞれPrimer §4.2・§4.3・§4.6で基本を説明している。§5–8だけを探す読者には、直前の説明に対応する節が見つけにくい。公理の読み方自体に誤りは認めないため低とした。
- 根拠：[OWL 2 Primer §4.2 Class Hierarchies](https://www.w3.org/TR/owl2-primer/#Class_Hierarchies)、[§4.3 Class Disjointness](https://www.w3.org/TR/owl2-primer/#Class_Disjointness)、[§4.6 Domain and Range Restrictions](https://www.w3.org/TR/owl2-primer/#Domain_and_Range_Restrictions)。存在の関係制限は[§5.2 Property Restrictions](https://www.w3.org/TR/owl2-primer/#Property_Restrictions)で説明される。2026-10-11に原典の目次と対応する説明を確認した。
- 修正方向：「§4–8」に直すか、表に対応する「§4.2・4.3・4.6・5.2」へ案内を限定する。本文を増やす必要はない。
- 執筆者の対応：採否・理由の追記待ち。
- 再確認：未実施。高・中の再確認必須指摘はない。

## 一次資料の確認

`sources.md` と `tool-comparison.md` の外部リンク先はブラウジングで取得し、資料・配布元の対応を確認した。これはリンク先の全文精査や、全機能の実機確認を意味しない。主な意味判断は次の範囲で行った。

| 判断 | 一次資料と確認範囲 |
|---|---|
| RDFの三項・識別子・値・空白ノード | [RDF 1.1 Concepts §3](https://www.w3.org/TR/rdf11-concepts/#section-rdf-graph)、[RDF 1.1 Primer §3](https://www.w3.org/TR/rdf11-primer/#section-data-model)。用語集と第9章の対応 |
| 公理と記載検査の違い | [OWL 2 Primer §2・4・5](https://www.w3.org/TR/owl2-primer/)、[SHACL §4.2](https://www.w3.org/TR/shacl/#core-components-count)。存在の記述がID記載の検査にならないこと |
| EL・QL・RLの用途と非包含 | [OWL 2 Profiles §1](https://www.w3.org/TR/owl2-profiles/#Introduction)。各用途と、どのプロファイルも他のものの部分集合でない説明 |
| 保存基盤のモデル・言語 | 比較表の公式入口を取得。[NeptuneのモデルとAPI](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html)、[JanusGraphのPG・Gremlin](https://docs.janusgraph.org/)、[JenaのTDB2・Fuseki等の部品](https://jena.apache.org/documentation/)、[RDF4JのRepository API・SPARQL](https://rdf4j.org/documentation/)を照合。認証・復旧・ライセンスの適合性は未評価 |
| 推論・検証ライブラリ | [RDFLib](https://github.com/RDFLib/rdflib)、[OWL-RL](https://github.com/RDFLib/OWL-RL)、[pySHACL](https://github.com/RDFLib/pySHACL)の役割を照合し、指定版の小例は実行した。ELKは[公式Wiki](https://github.com/liveontologies/elk-reasoner/wiki/Introduction)の対応範囲の説明を参照したが、全公理の試験はしていない |
| Graphifyの対象 | [指定サイトの案内](https://graphify.net/skills/graphify/)が[Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)を指すことを確認。配布元ではコードのAST解析と文書等の処理を説明しており、対象の短い役割紹介と矛盾しない |
| AI検索・更新する記憶 | [Microsoft GraphRAG](https://microsoft.github.io/graphrag/)、[Neo4j GraphRAG](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html)、[Graphiti](https://github.com/getzep/graphiti)の入出力と用途の説明を照合。回答品質や設計知識の承認を自動保証するとは判定していない |

その他の原典入口（Turtle、JSON-LD、SPARQL、Cypher、Gremlin、RDFS、SKOS、PROV-O、Ontology Development 101、OpenAPI、CodeQL、LlamaIndex、MCP）も取得できた。比較表のNeo4j、Memgraph、GraphDB、Stardog、Protégé、HermiT、LLM Graph Builder、Graphviz、NetworkXの入口も取得した。採用順位・普及順位・性能の優位を推測で付けていない。

## 実行と機械的な確認

実行環境はWindows、Python 3.12.14、RDFLib 7.1.4、pySHACL 0.30.1、OWL-RL 7.1.4。`PYTHONUTF8=1` とし、既存の `tmp/practice-env/Scripts/python.exe` を使った。新しい仮想環境の作成とネットワークからの再インストールは行っていない。実習README・依存版のファイル・プログラム・入力・期待結果を照合し、次を実行した。

```powershell
$env:PYTHONUTF8='1'
& tmp/practice-env/Scripts/python.exe examples/rdf-practice/verify.py
& tmp/practice-env/Scripts/python.exe examples/screen-flow-constraints/verify.py
& tmp/practice-env/Scripts/python.exe examples/development-practice/practice.py
```

| 実習 | 実際に確認した結果 |
|---|---|
| RDF | `status: passed`。Turtle/JSON-LDの同型と4トリプル、A017と日本語書名1行、正常データ適合、借りた人削除で不適合、書名削除で0行、OWLの逆関係を導出 |
| 画面フロー | `status: passed`。選択P-01/P-02、利用可能額70、通常70/71・特別50/51の四境界、Cエラー候補80件、特別のままCは0件、P-02変更後の利用可能額50 |
| 開発対応 | `status: passed`。v1でT-01、v2でT-03、根拠削除で不適合、不正原本2例を拒否、v2から旧テスト除去、JSONの原文位置と`execution_status: not executed` |

これらの実行は画面・API・DB・AIへの接続を含まない。開発実習は所定の `output/context-v2.json` を再生成するが、付録・ひな形・本文は書き換えない。

ローカルリンクはPythonで全54件の参照先存在を検査した。コードフェンスの開始・終了とYAML例の字下げ・構造は確認した。ルートのNode.jsからは `marked` を解決できず、MarkdownのHTML変換は今回実行していない。指定Python環境にPyYAMLがないため、YAMLパーサによる読込みも未実施である。YAMLは説明用ひな形であり、実行プログラムの入力ではない。対象には描画を要する図がなく、Mermaid描画は対象外。PDFは生成していない。

## 確認事項と限界

- README・HANDOFF・EDITORIAL_PLANは公開進捗の統合時に更新する必要がある。レビュー時点では「第14章まで」「15〜17章と付録は未完成」等の記載が残る。作業中の進捗更新として親エージェント側で扱い、対象9ファイルへの指摘には数えていない。
- macOS/Linuxの実行、新規環境での導入、全製品の投入・更新・削除・認証・復旧、ライセンス適合と料金見積り、LLMの呼出し・精度・費用は未確認。対象文書もその確認を主張していない。
- GitHub・スマホ実機での表示と、実読者が理解できるかは未確認。全18章・全製品・全仕様の再レビューではない。
- 外部ページは変わり得る。今回確認した役割紹介を、そのまま将来の導入版の機能保証には使わない。

指定された付録・ひな形について、高・中の未解決指摘や重要な実行確認の不足は認めなかった。低1件の採否記録後も、上記の未確認事項は未確認のまま保持する。

## 執筆者の対応記録

2026-10-11、執筆者 `/root` がAP-01を採用した。広い節範囲の案内を、表の四項目に対応する§4.2・4.3・4.6・5.2への直接リンクに置き換えた。公理の例や実習内容は変更していない。修正後の `practice-and-formalization.md` のSHA-256は `48a34b34a19f83519adc7430ff5bbf9e76c03c22e4a60b5845acc518a60bb85c`。低指摘への参照先修正としてセルフレビューを行い、独立した再確認は要求していない。初回の報告と未確認事項は上に保持する。
