# 第9章 独立レビュー

実施日：2026-10-11。初回判定：**要修正**（高0件・中2件・低1件）。

## 対象・独立性・基準

- 執筆者：親タスク `/root`。
- 独立レビュアー：`/root/chapter_09_independent`。執筆に参加せず、執筆時の会話履歴・セルフレビュー・過去のレビュー報告書を受け取らずに評価した。
- 主対象：[第9章](../docs/chapters/09-models-and-languages.md)の全133行と、本文が参照する `examples/rdf-practice/` の7ファイル。
- 基準：`AGENTS.md`、`OUTLINE.md`、`REVIEW_POLICY.md`。レビュー方針は更新日2026-10-01、ユーザー確認済みの版。
- 読者像：ソフトウェア開発経験があり、ナレッジグラフ・オントロジーは初学者。第3・4・6・7・8章を読み、第2・5章の用語導入と関連説明を検索・参照し、前章までの前提と予告を確認した。序章〜第8章全体の再レビューではない。
- 提供された `reviews/assets/2026-10-11-chapter-09/` の検査結果は読まず、コードと静的対応を独立に再確認した。独立検査の結果は本報告書に記録する。

依頼時の第9章SHA-256は、レビュー開始時および検査時の実ファイルと一致した。

```text
d5ce1f72c9700d524e641fa895aa167101520a56e1bcfa0682a111d1af4d43d6
```

## 観点ごとの結果

| 観点 | 判定 | 確認範囲と結果 |
|---|---|---|
| 初出の用語 | 指摘あり | PG・RDF・OWL・SKOS・SHACLの基礎は前章までに導入済み。新しい構文記号とRDFSの名称はI09-01・03を参照 |
| 前提と学習順序 | 指摘あり | 貸出→IRI→Turtle→JSON-LD→制約→問い合わせの順序は自然。第4章の予告との不一致はI09-02 |
| 説明の十分さ | 指摘あり | 小例の問いと期待結果は明確。コードを読むための局所的な補足が必要（I09-01） |
| 正確性 | 問題なし | 確認した範囲で、構文・データモデル・推論と検査・探索方向の重大な誤りは見つからなかった |
| 根拠と断定 | 問題なし | 標準仕様と製品の例を区別し、小例の検査を性能・製品間互換性の実証へ拡張していない |
| 具体例・図・表 | 問題なし／図は対象外 | 四つのトリプル、JSON-LD、SPARQL、SHACLの内容と期待結果は一致。本章に図はない |
| 復習・演習 | 問題なし | 演習1は書名の一致条件を外す応用になっている。演習2も記載の欠落と現実の不存在を区別できる |
| 構成と範囲 | 指摘あり | OUTLINEの技術全体像に沿う。OWLの具体的な構文への接続だけは前章の予告を回収できていない（I09-02） |
| 章間の整合 | 指摘あり | 貸出の単位、方向、日時を省く理由は第3・6章と整合。第4章の予告はI09-02 |
| 読みやすさ | 問題なし | 同じ貸出の記録で新構文を読むため、既出の題材の再利用は有効。注意の反復や章全体の長さを理由に削るべき箇所はない |
| 技術的な体裁 | 問題なし／一部対象外 | 内部リンク3件、コードフェンス4組、保存例との一致、Python実行を確認。PG断片の製品実行は対象外 |

## 指摘

### I09-01：例に使う新しい構文の一部が説明されていない

- **重要度：中**。観点：初出の用語、説明の十分さ。
- 箇所：`docs/chapters/09-models-and-languages.md`、「JSON-LDで同じ内容を書く」38〜53行、「定義・語彙・制約を使い分ける」68〜80行。
- 代表箇所：`"@graph": [...]`、`{"@value": "知識の整理入門", "@language": "ja"}`、`sh:property [ ... sh:nodeKind sh:IRI ]`。
- 問題：JSON-LDの説明は `@context`・`@id`・`@type` までで、例で新たに使う `@graph`・`@value`・`@language` の読み方がない。SHACLでも `sh:NodeShape`・`sh:property`・角括弧・`sh:nodeKind sh:IRI` が未説明である。空白ノードの存在は19行で紹介されているが、角括弧との対応は示されていない。初学者は、どの部分が値の記述で、どの部分が検査条件のまとまりかを推測することになる。特に、IRIであることを要求する条件と、個数を要求する条件をコードから対応付けられない。
- 根拠：本章の到達点は具体的な構文・問い合わせ・制約を小例で確認すること。[JSON-LD 1.1 §4.9](https://www.w3.org/TR/json-ld11/#named-graphs)にはトップレベルの複数ノードを `@graph` でまとめてcontextを共有する例があり、[§9.5 Value Objects](https://www.w3.org/TR/json-ld11/#value-objects)は値と言語の対応を定義する。[Turtle §2.7](https://www.w3.org/TR/turtle/#unlabeled-bnodes)は角括弧による空白ノードを定義し、[SHACL §4.1.3](https://www.w3.org/TR/shacl/#NodeKindConstraintComponent)は値ノードの種類の検査を定義する。
- 改善方向：JSON-LD例の直後に、`@graph` はこの例で複数の対象の記述をまとめる、`@value` は値、`@language` はその言語、と短く対応付ける。SHACLも「shapeは検査条件のまとまり」「`sh:property [ ... ]` は検査する関係の条件を空白ノードにまとめる」「`sh:nodeKind sh:IRI` は相手をIRIに限る」程度を補う。構文の網羅的な解説や追加演習は不要。
- 執筆者の対応：未記入。
- レビュアー再確認：未実施。

### I09-02：第4章で予告したOWL構文が本章にない

- **重要度：中**。観点：章間の整合、構成と範囲。
- 箇所：`docs/chapters/09-models-and-languages.md`、「定義・語彙・制約を使い分ける」59〜66行、「変換と推論の対応範囲を確かめる」107行。関連箇所：`docs/chapters/04-ontologies.md` 134行。
- 該当箇所：第4章は「実行用のOWL構文は第9章」と予告する。第9章のOWLは役割表・出典・プロファイルの概説のみで、OWLの語を使った構文例がない。
- 問題：第4章までの読者は、図と文章で理解した公理をどのように機械向けの表現に移すのかを第9章で学べると期待する。しかし、`a ex:Loan` などの個別事実とSHACLの条件しか提示されないため、定義を表す記述への接続が途切れる。これはOWLの全機能を追加すべきという指摘ではない。
- 根拠：前章の明示的な予告と、本章にOWL構文がないという対応上の不一致。[OWL 2 Primer §6.1](https://www.w3.org/TR/owl2-primer/#Property_Characteristics)は、既に第2章から扱う逆向きの関係をTurtleの `owl:inverseOf` で短く表せることを示す。
- 改善方向：既出の「借りた人」とその逆関係を一つの短いTurtle例で示し、何が公理で、対応する推論器ならどの関係を導くかを添える。前章の例と本章の表をつなぐ最小限の補足でよい。OWL構文を後の担当章へ移す方針なら、第4章の予告を実際の担当箇所へ修正し、本章で扱う範囲を明確にする。現行の `verify.py` がOWL推論を実行しているという記載にはしない。
- 執筆者の対応：未記入。
- レビュアー再確認：未実施。

### I09-03：RDFSの名称を初出で補う

- **重要度：低**。観点：初出の用語。
- 箇所：`docs/chapters/09-models-and-languages.md`、「定義・語彙・制約を使い分ける」61行。
- 該当箇所：表の `RDFS`。
- 問題：RDFSは前章までに導入されておらず、本章でも略称と役割だけが示される。役割は表で読めるため学習を止めるほどではないが、正式な資料名と略称の対応が分かりにくい。
- 根拠：[W3C RDF Schema 1.1](https://www.w3.org/TR/rdf-schema/)という資料名で定義されている。
- 改善方向：表の名称を `RDFS（RDF Schema）` とする程度で十分。RDF・RDFS・OWL全体の再説明は不要。
- 執筆者の対応・採否と理由：未記入。
- レビュアー再確認：未実施。

## 独立に実施した技術確認

実行環境：Windows、Python 3.12.14、RDFLib 7.1.4、pySHACL 0.30.1。既存の `tmp/practice-env/` を使い、新しい環境の構築は行っていない。

```powershell
tmp/practice-env/Scripts/python.exe -X utf8 examples/rdf-practice/verify.py
```

終了コード0、`status: passed` を確認した。

| 確認 | 独立実行の結果 |
|---|---|
| TurtleとJSON-LD | 同じ四つのトリプルとして同型 |
| SPARQL | `https://example.org/library/A017` と「知識の整理入門」の一行。言語タグ `ja` もassertで確認 |
| 正常なデータのSHACL | `conforms: true` |
| 借りた人の記載を削除 | `conforms: false`、`MinCountConstraintComponent` と焦点ノードL08を確認 |
| 書名を削除 | 問い合わせ結果0行、貸した本のトリプルは残る |
| 借りた人をリテラルに置換する追加確認 | `conforms: false`、`NodeKindConstraintComponent` |
| 借りた人に二つ目のIRIを加える追加確認 | `conforms: false`、`MaxCountConstraintComponent` |

追加確認はメモリ上のRDFグラフだけを変えて実行し、保存例は変更していない。

本文の四つのコードブロックは対応する四ファイルと、前後の空白を除いて一致した。本文のローカルMarkdownリンク3件は参照先が存在し、コードフェンスは四組で閉じていた。

一次資料の照合では、上記の指摘に使った資料に加え、[RDF Concepts §3・4](https://www.w3.org/TR/rdf11-concepts/)、[RDFS §3.1](https://www.w3.org/TR/rdf-schema/#ch_range)、[SPARQL §5.1・5.2](https://www.w3.org/TR/sparql11-query/#BasicGraphPatterns)、[SKOS Primer §2](https://www.w3.org/TR/skos-primer/#secskosessentials)、[OWL 2 Profiles §1](https://www.w3.org/TR/owl2-profiles/#Introduction)、[Neo4jのパターン仕様](https://neo4j.com/docs/cypher-manual/current/patterns/fixed-length-paths/)、[TinkerPop Vertex Steps](https://tinkerpop.apache.org/docs/current/reference/#vertex-steps)を確認した。RDFSのrangeから所属を導く説明、名前付きグラフの名前に信頼の意味が自動で付かない説明、Cypherの関係型と向き、Gremlinのin/outの読み方は、確認した仕様と整合する。

### 実習ファイルのレビュー時ハッシュ

| ファイル | SHA-256 |
|---|---|
| `examples/rdf-practice/README.md` | `3a76552fc95615251138f1bac40209c58a084ef37d70bc704f9036f313f9da1b` |
| `examples/rdf-practice/requirements.txt` | `bcbf363e97fbbc6f45babde54e6d7f98cf837c6b7f89e571cee3c3025784feee` |
| `examples/rdf-practice/verify.py` | `4b6f79f21340e5e6b00d2b6dd1ebe3efd75d1e0332c4fdcc7333c57177366d4d` |
| `examples/rdf-practice/loans.ttl` | `97bb9f3ec45495ccc3a36b04181694e6ffa0ac9cea0cbca9840882e2a5116de8` |
| `examples/rdf-practice/loans.jsonld` | `6c76ccd25a8010d7908a4b83da116d50fe8316e8869b2d0f23487b06bb000e1f` |
| `examples/rdf-practice/loan-shapes.ttl` | `bc968b86f2aa3fbfb58750643cc3e60781c6bdb1a200dda1cd511eb3e66d4037` |
| `examples/rdf-practice/books.rq` | `b4c311f18cf2408a01f839890e25b523f3eee52aa918b64349e65fbf764a4002` |

## 未確認・対象外と最終状態

- 本章にMermaid図はなく、図の描画は対象外。前章の図を描画し直す確認も行っていない。
- Cypher・Gremlinは本文が読み方の断片だと明示しているため、製品へのデータ投入や問い合わせ実行は対象外。構文と向きの意味を一次資料で照合した。
- RDFS・OWL・SKOSの推論器実行、PG↔RDF変換の実装、製品間互換性・性能の測定は行っていない。現行本文もこれらの実証を完了したとは主張していない。
- READMEのコマンドによるvenv新規作成・pipインストールは再実行していない。macOS・Linuxの実行は未確認であり、実習READMEもその旨を記載している。
- 第10章以降は未執筆であること自体を不備にしていない。README・HANDOFF・編集計画の進捗管理全体は本レビューの編集・全面点検対象外。
- PDFは対象外。本文・例・既存証跡は編集していない。

**最終状態：要修正。** I09-01・I09-02への対応を独立レビュアーが再確認するまで、指定範囲のレビュー完了とはしない。I09-03は採否と理由を記録すればよい。

## 2026-10-11 修正後の再確認（1往復目）

上記は初回レビュー時点の記録として残す。以下が修正後の結果である。

再確認者：`/root/chapter_09_independent`。第9章の修正版全148行と、実習ファイル8件を再確認した。依頼時の修正版ハッシュと実ファイルは一致した。

```text
a355baa8f7aebe49a4f300fe0564b2a98492489e201a42f78b3e21aa5bd61f5a
```

### 指摘への対応と再確認

| ID | 執筆者の対応 | 独立レビュアーの再確認 |
|---|---|---|
| I09-01（中） | 55行に `@graph`・`@value`・`@language` とTurtleの対応を追加。83行にshape・`sh:NodeShape`・`sh:property [ ... ]`・角括弧・IRI種別制約の説明を追加 | **解消**。同じ例の直後・直前で記号と役割を対応付けられ、構文を推測して補う必要がなくなった。既存例の意味は変わっていない |
| I09-02（中） | 70〜79行に `owl:inverseOf` の最小例、公理の意味、個別事実と組み合わせた期待帰結を追加。実習にも `inverse.ttl` と推論確認を追加 | **解消**。第2・4章の逆関係の説明から、具体的なTurtle構文と導出結果へ接続できる。第4章134行の予告と整合した |
| I09-03（低） | 63行の名称を `RDFS（RDF Schema）` に変更 | **採用・解消**。名称の対応が初出で分かる |

追加説明は同じ貸出の例に収まり、新しい大きな題材や構文一覧には広がっていない。既存の問い合わせ・演習の意味、貸出の粒度、日時を省く範囲、第6〜8章の主張・来歴管理との関係に新たな矛盾は見つからなかった。

### 追加例と既存実習の独立実行

同じWindows / Python 3.12.14環境で、修正版の `verify.py` を再実行した。RDFLib 7.1.4、pySHACL 0.30.1に加え、`owlrl` 7.1.4を実行時のメタデータで確認した。

```powershell
tmp/practice-env/Scripts/python.exe -X utf8 examples/rdf-practice/verify.py
tmp/practice-env/Scripts/python.exe -m pip check
```

- `verify.py` は終了コード0、`status: passed`。
- TurtleとJSON-LDは同じ四つのトリプル。問い合わせはA017のIRIと日本語の書名の一行。
- 正常データのSHACLは適合、借りた人を削ったデータは不適合。書名欠落時の問い合わせ結果は0行で、貸した本のトリプルは残る。
- 新しい推論グラフは貸出データと `inverse.ttl` を読み込み、`ex:U03 ex:hasLoan ex:L08` が推論前に存在せず、`DeductiveClosure(OWLRL_Semantics).expand(...)` 後に存在することをassertしている。独立実行でも `inverse_relation_derived: true` を確認した。
- SHACL用の元データは推論グラフと分かれ、既存の `inference='none'` は維持されている。
- `requirements.txt` に `owlrl==7.1.4` が明示され、実習READMEもSHACL検査と別グラフの推論を説明している。`pip check` は `No broken requirements found.`。

逆関係の新例は、初回に参照した[OWL 2 Primer §6.1](https://www.w3.org/TR/owl2-primer/#Property_Characteristics)に加え、[OWL 2 Profiles §4.3 表5](https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules)の `prp-inv1`・`prp-inv2` と照合した。記述した公理と個別事実から逆向きの関係を導く内容は整合する。

本文の五つのコードブロックは保存例と、前後の空白を除いて一致した。コードフェンス五組とローカルリンク3件も再確認した。初回からある四つのデータ・問い合わせファイルのハッシュは変わっていない。

| 追加・変更された実習ファイル | 修正後のSHA-256 |
|---|---|
| `examples/rdf-practice/inverse.ttl` | `612c823a7c6fc9a0c6b6edf65f0130d1390958c5fb7970be397d959e19e11398` |
| `examples/rdf-practice/README.md` | `c5fc02fd33b85a4de8d6fb97414ced67c32e4a756fa66abd3fa78fdf6b6a5b21` |
| `examples/rdf-practice/requirements.txt` | `d63550d95befa6d02403729c616cdc948ddb8990280ffa05e6cd805d11436045` |
| `examples/rdf-practice/verify.py` | `62b26b5c550be5502db538e2aa2c4f20f0dd47229c53f8ae66b347906174966b` |

### 修正後の確認範囲と最終状態

全指摘の対応を再確認し、新たな高・中の指摘はない。初回の確認範囲と限界を維持し、OWL推論の実行についてだけ、追加した逆関係の小例を確認済みに更新する。OWL全機能、矛盾検出、他の推論器・製品の互換性や性能を確認したという意味ではない。新しいvenvでのインストール、macOS・Linux、Cypher・Gremlinの製品実行、PDFは引き続き未確認または対象外である。

**最終状態：指定範囲のレビュー完了。** 対象は上記SHA-256の第9章と、記録した実習ファイルである。
