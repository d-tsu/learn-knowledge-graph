# 第9章：データモデル・標準・問い合わせ言語

更新日：2026-10-11。執筆とレビューの状況は[README](../../README.md)で確認できる。

## この章の到達点

貸出の同じ記録を、PGの構造とRDFのトリプルで読めるようになる。RDFの具体的な構文、問い合わせ、制約を小さな例で確認し、表現を移すときに何を保つかを考える。

## 記述する内容と、書き方を分ける

第6章で決めた「貸出L-08でU-03にA-017を貸した」という内容を使う。PGなら貸出・利用者・蔵書をノードにし、関係に型を付ける。書名は蔵書ノードの属性にできる。RDFなら、貸出を主語とする「借りた人」「貸した本」のトリプルと、蔵書の書名を述べるトリプルにする。

PGのラベルや属性の扱いは製品のデータモデルに従う。RDFは、主語・述語・目的語を組にした共通のデータモデルである。RDFには複数の具体的な書き方があり、TurtleとJSON-LDはその例である。[Neo4jのグラフ概念](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)、[W3C RDF 1.1 Concepts §3](https://www.w3.org/TR/rdf11-concepts/#section-rdf-graph)

## IRI・値・空白ノード

**IRI**（Internationalized Resource Identifier）は、対象や関係を識別する文字列である。ここでは `https://example.org/library/A017` を一冊の蔵書に、`https://example.org/library/book` を「貸した本」という関係に使う。`example.org` は例示用であり、実際の図書室への接続先ではない。

書名の文字列や冊数の数値は**リテラル**として表す。IRIで識別した一冊と、その書名のリテラルは別のものになる。RDFには、IRIを付けずに対象を表す**空白ノード**もある。他の公開版から長く参照する対象には、識別子をどう維持するかを別途決める。空白ノードの内部ラベルを恒久的なIDとして流用しない。[W3C RDF 1.1 Concepts §3.2–3.4](https://www.w3.org/TR/rdf11-concepts/#section-IRIs)

## Turtleで書く

**Turtle**は、IRIの共通部分を短く書けるRDFの構文である。次の例では `ex:` が `https://example.org/library/` の略になる。`a` はクラスへの所属を表す `rdf:type` の省略形、`;` は同じ主語について続ける記号、`.` は文の終わりである。[W3C Turtle §2](https://www.w3.org/TR/turtle/#turtle-language)

```turtle
@prefix ex: <https://example.org/library/> .

ex:L08 a ex:Loan ;
    ex:borrower ex:U03 ;
    ex:book ex:A017 .
ex:A017 ex:title "知識の整理入門"@ja .
```

`@ja` は文字列の言語が日本語であることを示す。この四つのトリプルは、貸出の種類、借りた人、貸した本、書名を記録している。第6章の日時は、構文を読むためのこの小例では省いている。そのため「現在借りている本」ではなく「この貸出で貸した本」を調べる例として使う。

## JSON-LDで同じ内容を書く

**JSON-LD**は、JSONのキーや値がどのIRIを表すかを対応付けられる構文である。`@context` がその対応を指定し、`@id` が対象のIRI、`@type` がクラスへの所属を示す。JSONの見た目が同じでも、contextが違えばRDFとしての意味も変わり得る。[W3C JSON-LD 1.1](https://www.w3.org/TR/json-ld11/#basic-concepts)

```json
{
  "@context": {"ex": "https://example.org/library/"},
  "@graph": [
    {"@id": "ex:L08", "@type": "ex:Loan",
     "ex:borrower": {"@id": "ex:U03"},
     "ex:book": {"@id": "ex:A017"}},
    {"@id": "ex:A017",
     "ex:title": {"@value": "知識の整理入門", "@language": "ja"}}
  ]
}
```

この例のTurtleとJSON-LDは、同じ四つのトリプルを表す。文字列の差分が違っても、RDFとして読み込んだ内容を比較できる。ここではcontextを文書内に置く。外部contextを使う場合は、参照する版と取得できない場合の扱いも決める。

`@graph` は、この例では複数の対象の記述をまとめる。`@value` は文字列の値、`@language` はその言語を指定する。Turtleの `"知識の整理入門"@ja` と、JSON-LDの値と言語の組が対応する。

## 定義・語彙・制約を使い分ける

RDFのトリプルだけでは、任意に付けた関係名の意味は決まらない。共通の語彙や言語で、分類の定義や検査条件を追加する。

| 言語・語彙 | 何を書くか | 貸出・分類の例 |
|---|---|---|
| RDFS（RDF Schema） | クラス、下位クラス、プロパティの基本的な意味 | 印刷書籍は印刷資料の下位クラス |
| OWL | より詳しいクラス・関係・個体についての公理 | 二つの関係が互いに逆向きである |
| SKOS | 検索・整理に使う概念、名称、関連関係 | 貸出用資料の別名を管理する |
| SHACL | 指定したRDFデータに対する検査条件 | 貸出に借りた人を一つ記載する |

これらはトリプルで記述できるが、利用する処理は違う。例えばRDFSの `rdfs:range` は、関係の相手があるクラスに属すると導くために使う。「相手の型が違えば入力を拒否する」というデータ検査とは意味が違う。[W3C RDFS §3](https://www.w3.org/TR/rdf-schema/#ch_properties)、[OWL 2 Primer](https://www.w3.org/TR/owl2-primer/)、[SKOS Primer](https://www.w3.org/TR/skos-primer/)

第2・4章の逆向きの関係は、OWLの `owl:inverseOf` で記述できる。次は「貸出で本を借りた人」と「利用者が本を借りた貸出」を互いに逆の関係とする公理である。[OWL 2 Primer §6.1](https://www.w3.org/TR/owl2-primer/#Property_Characteristics)

```turtle
@prefix ex: <https://example.org/library/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

ex:borrower owl:inverseOf ex:hasLoan .
```

冒頭の `ex:L08 ex:borrower ex:U03` とこの公理を使うと、対応する推論器は `ex:U03 ex:hasLoan ex:L08` を導ける。個別の貸出記録と、関係どうしの意味を定める公理を分けて読む。

次は、貸出の借りた人にIRIを一つ記載するSHACLの例である。`sh:targetClass` は検査対象のクラス、`sh:path` は検査する関係、`sh:minCount` と `sh:maxCount` は値の個数を指定する。[W3C SHACL §2・4.2](https://www.w3.org/TR/shacl/#core-components)

**shape**は検査条件のまとまりで、`sh:NodeShape` は対象ノードに適用する形である。`sh:property [ ... ]` は関係の値に対する条件をまとめる。角括弧は空白ノードを表し、`sh:nodeKind sh:IRI` はその値をIRIに限る。

```turtle
@prefix ex: <https://example.org/library/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

ex:LoanShape a sh:NodeShape ;
    sh:targetClass ex:Loan ;
    sh:property [
        sh:path ex:borrower ;
        sh:minCount 1 ; sh:maxCount 1 ; sh:nodeKind sh:IRI
    ] .
```

冒頭のデータはこの制約を満たす。借りた人のトリプルを削ると違反になる。上の制約は相手のIRIの実在や、利用者が業務上借りられるかまでは検査していない。どのデータと推論設定で検査したかも結果と一緒に記録する。

## 問い合わせ言語で関係をたどる

**SPARQL**はRDFを問い合わせる言語である。次の問いは「U-03に対応する貸出で貸した本のIDと書名を出す」。`?loan` などは一致した対象を入れる変数、`WHERE` 内は一致させるトリプルの形である。[W3C SPARQL 1.1 §2](https://www.w3.org/TR/sparql11-query/#WritingSimpleQueries)

```sparql
PREFIX ex: <https://example.org/library/>
SELECT ?book ?title WHERE {
  ?loan a ex:Loan ; ex:borrower ex:U03 ; ex:book ?book .
  ?book ex:title ?title .
}
ORDER BY ?book
```

結果はA017のIRIと、日本語の書名「知識の整理入門」の一行になる。書名が未記載の本は、この問い合わせでは結果に出ない。検索結果にないことを、本が存在しない証拠にはしない。

PGには**Cypher**や**Gremlin**を使う構成がある。Cypherはノードと関係のパターンを記述し、Gremlinはグラフ上の移動や絞り込みを組み合わせる。例えばCypherの `(loan:Loan)-[:BORROWER]->(user:User)` は型付きの関係の形を表す。Gremlinの `in('BORROWER').out('BOOK')` は借りた人から貸出へ戻り、貸した本へ進むという移動の一部を表す。これらは読み方の断片であり、データ投入から実行までを提供する例ではない。[Neo4j Cypherのパターン](https://neo4j.com/docs/cypher-manual/current/patterns/)、[Apache TinkerPopのGremlin](https://tinkerpop.apache.org/docs/current/reference/#intro)

## 変換と推論の対応範囲を確かめる

PGからRDFへ変換するときは、ラベル・関係の属性・多重の関係・値の型をどう写すか決める。例えば同じ二つの対象を結ぶ二本の関係に別々の出典が付くなら、第6章のように主張ごとにIDを持たせる案がある。単純な主語・関係・相手へ潰すと、二つの根拠を分けられなくなる。

RDF側でも、IRIの対応、リテラルの型と言語、原文の位置、公開版を保つ。複数のグラフを名前付きでまとめるRDFデータセットもあるが、その名前だけで「この出典を信頼する」といった意味が自動的に決まるわけではない。[W3C RDF 1.1 Concepts §4](https://www.w3.org/TR/rdf11-concepts/#section-dataset)

推論器を選ぶときは「OWL対応」という表示だけで決めない。使う公理と、OWLの対応範囲を限定した**プロファイル**を確認する。OWL 2 EL・QL・RLは扱う表現と計算の性質を調整した範囲である。必要な公理を含む小例で、期待する帰結と矛盾の扱いを試す。第11章でツールと対応付ける。[W3C OWL 2 Profiles](https://www.w3.org/TR/owl2-profiles/)

## 実行して確かめる範囲

上の構文は、[実習データと検査プログラム](../../examples/rdf-practice/README.md)に同じ内容を保存している。RDFLib 7.1.4、pySHACL 0.30.1、OWL-RL 7.1.4を使い、構文の一致、問い合わせの一行、借りた人を削った場合の制約違反、逆向きの関係の導出を確認する。これらは教材の小例の確認であり、他製品の互換性や処理性能の測定ではない。

## 復習

- TurtleとJSON-LDの書き方が違っても、同じRDFを表すとはどういうことか。
- RDFSの関係の相手の定義と、SHACLによる入力検査は何が違うか。
- PGの関係に付いた出典をRDFへ移すとき、何を保つか。

## 演習と解答例

### 演習1：書名がない本

U-03にA-022を貸した記録を追加したが、A-022の書名は記載しなかった。本章のSPARQLでA-022は出るだろうか。どの本を貸したかだけを調べるには何を変えるか。

解答例：`?book ex:title ?title` も一致条件なので、A-022は結果に出ない。蔵書IDだけが必要なら書名の条件を外し、`SELECT ?book` とする。書名がないことと貸出の記録がないことを区別する。

### 演習2：違反と不明

貸出L-30には借りた人の記載がない。SHACLの上の制約に違反した。この結果から「L-30には現実に借りた人がいない」と言えるだろうか。

解答例：言えない。検査結果は、指定したデータに必要な記載がないことを示す。担当者は原本へ戻って相手を確認する。存在についての公理や、現実の状態とは区別する。

前：[第8章](08-quality-and-lifecycle.md) ／ 続き：第10章「保存・問い合わせ基盤」
