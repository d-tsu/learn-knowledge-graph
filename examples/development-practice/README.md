# 開発対応の小さな実習

[第17章](../../docs/chapters/17-incremental-practice.md)の架空の表からRDFを作り、問い合わせ・SHACL検証・版の更新を確かめる。Python 3.12、RDFLib 7.1.4、pySHACL 0.30.1を使う。

Windows PowerShellでリポジトリのルートから実行する。

```powershell
python -m venv examples/development-practice/.venv
examples/development-practice/.venv/Scripts/python.exe -m pip install -r examples/development-practice/requirements.txt
examples/development-practice/.venv/Scripts/python.exe examples/development-practice/practice.py
```

実行結果の`status`が`passed`なら、v1でT-01、v2でT-03を取得し、根拠の欠落を違反として検出し、不正な二つの原本を拒否した。v2の結果にはT-01を残さない。問い合わせ結果に対応する原文行をIDで照合し、`output/context-v2.json`にAIへ渡す候補情報を出力する。原本の行順を交換しても同じ対象とテストを渡すことを確認する。外部AIへの送信は行わない。

原本は四列・要件ごとに一行の表に限定する。自由文や別の表構造には対応しない。sourceの`https://example.org/practice/trace-v1#R-01`は教材用識別子で、`sources/trace-v1.md`のR-01行に対応する。実際にアクセスできるWebページを意味しない。JSONには元のローカル相対パス・行番号・原文も含む。

作成したグラフはメモリ上で処理する。原本の差替えごとに全件を作り直す。実際のAPIやテストは用意していないため、対応の正しさ、AIの回答品質、システムの動作はこの実習の確認範囲に含まれない。
