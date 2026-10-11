# 第17章の独立レビュー

実施日：2026-10-11。初回判定：**要修正**（高0件・中1件・低0件）。

## 担当・基準・対象

- 執筆担当：親エージェント `/root`。
- 独立レビュアー：`/root/chapter_17_independent`。執筆に参加せず、会話履歴を引き継がない新しい文脈で、本文・実習ファイル・一次資料から判断した。執筆者のセルフレビュー報告は評価に用いていない。
- 基準：`OUTLINE.md`（2026-09-26）、`REVIEW_POLICY.md`（2026-10-01、ユーザー確認済み）。
- 主対象：下記manifestの9ファイル（第17章1ファイル、実習8ファイル）を全文確認した。
- manifest：`tmp/chapter-17-review-manifest.json`、SHA-256 `9b9c19f26b53a92eb907870a96683a8919efb51a1a761954bc5b68b8459baed3`。
- 開始時・初回報告終了時に、manifestと全対象のSHA-256の一致を確認した。

| 対象 | SHA-256 |
|---|---|
| docs/chapters/17-incremental-practice.md | a448b57d09cd9aff86e6abfcd4580b564c3656be1ec4af67c75b995e1be9b96f |
| examples/development-practice/.gitignore | 34d3284d614af518304b6714440832122a173df357dee98a9ed5d59ce197d0f7 |
| examples/development-practice/practice.py | 2ff2baf4945a3b88d413033c87967dcc425959dbbf9fd6b9d92b0ebf19a28c89 |
| examples/development-practice/README.md | 8f80cc41f8b5d999fa30b2ca5f18e0c3e4fae7c15f011a9164f69b7a57f80f95 |
| examples/development-practice/related-tests.rq | 5001967e38c6e499ffce73abe4ea34b3af0894f27770158063cd8d78ee3227d7 |
| examples/development-practice/requirements.txt | bcbf363e97fbbc6f45babde54e6d7f98cf837c6b7f89e571cee3c3025784feee |
| examples/development-practice/shapes.ttl | 8213da2d18a4f8bd1564e1589d881994a49aa23df4c7876b0b7cabfd31c9e402 |
| examples/development-practice/sources/trace-v1.md | 30a1027a7acb10c2c2d3d481c8fef938f985791b396f4c45df82d0f8ee618ec3 |
| examples/development-practice/sources/trace-v2.md | bf2cd599be4394d788670cb211a5740bed7cbb1de755bb9bde0f2d8d4d96124d |

整合確認には第9・11・13・16章の本文、第8・12・14章の関連説明、第15章の制約充足と実行範囲の説明、README・HANDOFF・編集計画を用いた。既存章全体の再レビューではない。README等が第13章までを現状とする点は、執筆途中の進捗として扱った。公開前の進捗更新は執筆担当の作業となる。

## 観点別の結果

| 観点 | 結果 | 確認した範囲と判断 |
|---|---|---|
| 初出の用語 | 問題なし | IRI・SPARQL・SHACL・RDFLib・pySHACLは第9・11章で説明済み。MCPは第12章、作業用の文脈は第14章、制約充足は第15章に説明がある。モデルベーステストは表で状態・操作からテストを導く役割を示しており、詳細知識を演習の前提にしていない。 |
| 前提と学習順序 | 問題なし | 図書室の構文実習から開発対応へ題材を移す説明があり、要件→APIとテスト→APIの方向、検索での逆向きの照合を本文で確認できる。 |
| 説明の十分さ | 問題なし | 一つの問い、四列の原本、手作業のモデル、制約検査、自動化、更新の順で追える。実習READMEに実行入口と制限がある。 |
| 正確性 | 指摘あり | SHACLによる記載検査と実テストの実行を区別できている。JSON作成は問い合わせ結果を使用しておらず、C17-01の不一致がある。 |
| 根拠と断定 | 指摘あり | 架空の対応表、LLM未呼出し、費用・精度未実測、実システム未接続は明示されている。問い合わせからJSONへの接続の記述はC17-01を要修正。 |
| 具体例・図・表 | 問題なし | v1のT-01からv2のT-03への差替え、T-02の除外理由、原本位置は一致。図1点を独自に描画・目視し、矢印・文字の欠けや重なりを認めなかった。 |
| 復習・演習 | 問題なし | 復習3問、演習2問は本文から考えられる。演習1は一要件一行のパーサ制限と形式改訂の必要性を解答で示す。演習2はグラフと回答資料の更新を区別する。 |
| 構成と範囲 | 問題なし | OUTLINEの手作業モデル、問い合わせ・制約検証、抽出とAI連携の試行、更新運用、発展テーマを小例で扱う。外部AIの実装追加や説明の一律増量は必要ない。 |
| 章間の整合 | 問題なし | 第8章の版管理と再構築、第12・14章の根拠付き文脈、第16章の同条件比較へつながる。 |
| 読みやすさ | 問題なし | 各節の作業と確認できる範囲が短い段落で分かれている。専門用語の再説明がなくても既読章を前提に追える。 |
| 技術的な体裁 | 指摘あり | 対象Markdownのローカルリンク4件は存在、フェンスは各ファイルで閉じている。図1点は描画成功。標準実習は成功し、行順変更時のJSONの不一致をC17-01として記録。 |

## 指摘

### C17-01：AI用JSONが検索結果ではなく原本の先頭行から作られる

- 重要度：**中**。
- 観点：正確性、根拠と断定、技術的な体裁。
- 代表箇所：`examples/development-practice/practice.py` 85–88行、`row = records2[0]` とその値を使うcontextの作成。
- 関連箇所：`docs/chapters/17-incremental-practice.md`「AIへ渡す根拠を作る」61行、「問い合わせ結果から、要件ID・API・テスト・原文位置・公開版をまとめる」。

本文では問い合わせ結果をJSONへつなぐが、実装はv2の最初の原本行をそのまま選んでいる。検索結果の検査とJSONの作成が独立しており、正常な四列・要件ごとに一行という制限の範囲でも結果を取り違えられる。配布された行順では正しいJSONになることは確認した。

対象ファイルを編集せず、一時ディレクトリに問い合わせ・shape・原本をコピーし、v2のR-01行とR-02行だけを交換した。`practice.py`をimportし、ROOTをその一時ディレクトリに向けてmainを実行すると、次の結果になった。

```text
status: passed
v2_query: A-01, T-03, trace-v2#R-01
context.requirement: R-02
context.api: A-02
context.test: T-02
context.source.text: | R-02 | 特別申請を受け付ける | A-02 | T-02 |
```

原本の対応内容は変更しておらず、パーサも正常入力として受理している。読者が表を並べ替えただけで、R-01へのAI入力候補が別要件へ変わり、成功表示で見逃す。この章の「知識の構築と利用の接続を確かめる」という到達点に直接関わるため、修正が必要である。

根拠はコードと上記の実行結果、本文61行の説明である。[RDFLib 7.1.4のSPARQL説明](https://rdflib.readthedocs.io/en/7.1.4/intro_to_sparql.html)でも、SELECTの結果はqueryから返るResultRowの変数束縛であり、原本行の並びとは別のものと確認できる。

修正方向：実際のv2問い合わせ結果を保持し、そのAPI・テスト・出典に対応する原本行をIDで照合してJSONへまとめる。R-01の問い合わせとJSONの対象・テスト・原文が一致することを検査する。原本行の交換でも対応が保たれる確認を追加すれば、この問題を直接検出できる。全体の構成変更や外部AIへの接続は不要である。

執筆者の対応：未記入。独立再確認：未実施。

## 実行・描画・出典の確認

Pythonは`tmp/practice-env/Scripts/python.exe`を使用し、実行時に`PYTHONUTF8=1`を設定した。実測の版はPython 3.12.14、RDFLib 7.1.4、pySHACL 0.30.1である。

標準実習の実行では、`status=passed`、v1のA-01/T-01/trace-v1#R-01、v2のA-01/T-03/trace-v2#R-01、`missing_source_conforms=false`、不正原本2件の拒否、旧T-01の除去を確認した。生成された`output/context-v2.json`もR-01/A-01/T-03、v2の5行目、`execution_status=not executed`を保持していた。C17-01の追加試験は一時コピーのみで実行した。

第17章のMermaid1点を`render-chapter-diagrams.cjs`とMermaid 11.12.0、Edge headlessで独自に描画した。`tmp/chapter17-independent-diagrams/`のPNGを目視し、要件→API、テスト→API、テスト→原本行の方向と日本語ラベルが本文に合うことを確認した。SVG/PNGとrender-check.jsonは再生成できる確認用ファイルである。

技術判断のために以下の一次資料を確認した（確認日2026-10-11）。

- [W3C SHACL §2.1.3.2、§4.1.3、§4.2.1](https://www.w3.org/TR/shacl/)：クラスを対象にするshape、IRIの型、最低個数の検査を確認。根拠の内容や現実のテスト実行を保証する制約ではないという説明と整合する。
- [W3C SPARQL 1.1 §5.1](https://www.w3.org/TR/sparql11-query/#BasicGraphPatterns)：要件→API、テスト→同じAPI、テスト→出典のパターン照合を確認。
- [RDFLib 7.1.4 Querying with SPARQL](https://rdflib.readthedocs.io/en/7.1.4/intro_to_sparql.html)：Graph.queryとSELECT結果の扱いを確認。
- [pySHACL v0.30.1 Python Module Use](https://github.com/RDFLib/pySHACL/tree/v0.30.1#python-module-use)：validateの返値とinference='none'の指定を確認。

## 未確認・対象外と最終状態

- 新規の空の仮想環境でのpipインストールは未実施。指定の準備済み環境で、requirements.txtの2パッケージの版と実行を確認した。
- AI接続、AI回答の品質・費用、DB・MCP接続、実際のAPI・テストの実行、製品での効果は未確認。この実習は実装・実証したと主張していないため、今回の範囲の必須確認には含めない。
- 図の確認はローカル描画のみ。GitHub・スマートフォンでの表示、実読者の理解は未確認。PDFは作成していない。
- 任意のMarkdown入力、全ての不正入力へのパーサの耐性は未確認。四列・一要件一行という教材の限定範囲で確認した。
- 本文・実習コード・原本は編集していない。保存するレビュー成果はこの報告書のみ。

初回の最終状態は**要修正**。C17-01への対応と独立再確認が終わるまで、指定範囲をレビュー完了とはしない。

## C17-01への対応と独立再確認（2026-10-11、1往復目）

初回の記録は上記のまま保持する。この節が修正版についての最新の判定である。

修正版manifestのSHA-256は`6f3adba63eb0c9d1648474b886b1081155f60a492d6b0ae4aad85b8078d00186`。再確認の開始時・終了時に、manifestと対象9ファイル全てのハッシュ一致を確認した。初回から変更された対象は次の2ファイルのみである。本文・問い合わせ・shape・原本等、他7ファイルのハッシュは初回の表と同じである。

| 変更対象 | 修正版SHA-256 |
|---|---|
| examples/development-practice/practice.py | f03925185376d25335e785fb003cca6dfa847e45af4466506514071e9d24e5ed |
| examples/development-practice/README.md | eb20a1e07d37893e286b8399d4d35ddd366dc51f6ca44c597eb656a0bbeddd98 |

執筆者は実際のv2のSELECT結果を保持し、`context_from_query`で要件ID・API・テスト・出典IRIと一致する原文行を照合するよう修正した。問い合わせ結果または一致する行が一つでなければValueErrorになる。標準実習内に行交換の確認を追加し、READMEにもID照合と行順変更時の確認を記載した。

独立レビュアーは変更されたコード・READMEを全文読み、以下を同じ指定環境で再実行した。

1. 標準実習：`status=passed`。v1のT-01、v2のT-03、根拠欠落による不適合、不正原本2件の拒否、旧T-01の除去が保たれた。`reordered_source_context_matches=true`も確認した。通常のJSONはR-01/A-01/T-03、v2の5行目である。
2. 独立した行交換試験：コードに追加された検査だけに頼らず、レビュアー側でv2原本文字列のR-01行とR-02行を交換し、build→実際のSELECT→context_from_queryを実行した。問い合わせはA-01/T-03/trace-v2#R-01を返し、JSONもR-01/A-01/T-03を保持した。原文位置は6行目に変わり、原文はR-01の行で一致した。公開版v2、未実行の状態も保たれた。対象原本は編集していない。
3. 照合の関連影響：API・テストが一致しない結果、旧版の出典IRI、空の問い合わせ結果をそれぞれ渡し、全てValueErrorとして拒否されることを確認した。検索で得ていない別要件を先頭行から採用する経路は除去されている。

本文61行の「問い合わせ結果から…まとめる」という説明と、修正版の処理は一致する。実習の入力制限や外部AI未接続という説明も保たれた。図と他の本文に変更がないため、初回に実施した描画・目視・リンク・用語・演習の確認を引き継ぐ。新たな高・中・低の指摘はない。

| 指摘ID | 執筆者の対応 | 独立再確認 |
|---|---|---|
| C17-01（中） | SELECT結果と原文行のID照合へ修正。行交換の検査とREADMEの説明を追加 | **解消**。行交換でも同じ対象とテスト、変更後の原文位置となることを独立に再現した |

修正版の最終状態：**指定範囲のレビュー完了**。未解決の高・中・低の指摘は0件。初回に記録した未確認・対象外の範囲は引き続き残る。特に、これは教材のローカル実習と文書の確認であり、AI回答品質や実製品への適用効果の実証を意味しない。
