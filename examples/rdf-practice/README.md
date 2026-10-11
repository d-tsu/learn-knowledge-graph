# RDFの小さな実習

第9章のTurtle・JSON-LD・SHACL・SPARQLを、そのまま保存した例です。Python 3.12で動作を確認しています。データは架空で、外部サービスへ接続しません。

PowerShellでは、このフォルダで次のコマンドを実行します。

```powershell
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe verify.py
```

macOS・Linuxでは `python3 -m venv .venv` で作り、実行パスを `.venv/bin/python` に置き換えます。これらのOSでは未実行です。既に環境がある場合は、必要なパッケージの版を確認してください。

`verify.py` は二つの構文が同じ四つのトリプルになること、問い合わせがA017と書名を返すこと、借りた人の記載を削ると制約違反になることを確かめます。書名だけを削ると問い合わせ結果がなくなる一方、貸した本の関係が残ることも確認します。成功時はJSONの `status` が `passed` になります。

| ファイル | 内容 |
|---|---|
| loans.ttl / loans.jsonld | 同じ貸出の記録を二つの構文で表す |
| loan-shapes.ttl | 借りた人のIRIを一つ記載する制約 |
| books.rq | U03に貸した本のIDと書名を取得する問い合わせ |
| inverse.ttl | 借りた人と貸出を逆向きに結ぶOWLの公理 |
| verify.py | 正常なデータと一部を削ったデータの比較 |

SHACL検査には `inference='none'` を指定しています。別のグラフでOWL-RLによる推論を行い、U03からL08への逆向きの関係が導かれることも確認します。検査と推論は混ぜず、それぞれの入力を用意しています。DB製品間の互換性や性能は測っていません。第17章では、要件とテストの対応を扱う実習へ進みます。
