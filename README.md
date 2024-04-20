# Veilog filelist parser

## Usage

```ps
make build
```

## Install
```ps
make install
```


## python -m <module> 環境における lanch.json
* module と pythonPath を追加し、program を削除する。
* module には __init__.py と __main__.py が格納されているモジュール名を記載する。
* pythonPath には仮想環境ディレクトリの Python 実行ファイル名を記載する。

## unittest の実行方法
* テストケースディレクトリへ __init__.py を格納する
* 以下コマンドを実行する
```ps
python -m unittest
```
* VSCode のテスト エクスプローラーを利用す場合は、 unittest 環境構築後、VSCode のテスト エクスプローラーのナビゲーションに従って VSCode を操作すれば構築できる。