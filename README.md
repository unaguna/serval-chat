# Serval Chat (discord bot)

Serval Chat は、仮想人格「サーバル」と対話できる discord bot です。
Serval Chat は実に**2種類**もの応答をすることができます。


## 依存関係

本モジュールの動作には以下のソフトウェアを使用します。

- Python 3.7 以上の実行環境
- MeCab (バージョン 0.996 で動作確認)
    - 形態素解析ツールです。discord で受け取った他人の発言を解析するために使用します。


## 起動方法

1. [MeCab](https://taku910.github.io/mecab/#download) 本体と辞書をダウンロードし、インストールする。（windows では、辞書付きのバイナリパッケージをダウンロード・インストールするだけで済みます）

1. Discord Developer Portal で Application と Bot を作成する。
    - 補足: 作成した Bot のトークンは後で使用する。

1. 作成した Bot を、サーバルと会話したいサーバに招待する。

1. Python 3.7 以上が動作する環境を作る。
    - **注意**: python の x86 or x64 は、MeCab のものに合わせること。
   
1. 下記のコマンドで必要パッケージをインストールする。
    ```shell
    # python の仮想環境を使う場合は、使用した仮想環境作成方法に応じて、conda コマンドなり Activate.ps1 や Activate.bat なりを使っておく
    pip install aioconsole
    pip install discord.py
    pip install mecab
    ```

1. このリポジトリをダウンロードし、serval_chat.py を実行する。ただし、環境変数 SERVAL_CHAT_TOKEN に、作成した Bot のトークンを指定すること。
    - PowerShell での実行例
        ```shell
        Set-Item env:SERVAL_CHAT_TOKEN "ここにBOTトークンを入れる"
        # python の仮想環境を使う場合は、使用した仮想環境作成方法に応じて、conda コマンドなり Activate.ps1 なりを使っておく
        # カレントディレクトリは serval_chat.py があるディレクトリに移しておく
        python serval_chat.py
        ```
    
1. Discord 上でサーバルがオンラインになっていれば成功。
    - 次回以降は、環境変数の設定と serval_chat.py のみで起動できます。


## 動作仕様

特定のテキストチャンネルで、他の人の発言に反応して発言します。

### 動作するチャンネル

サーバルを招待したサーバに「さばんな」もしくは「サバンナ」が付くテキストチャンネルがあれば、そこで動作します。（該当するチャンネルがない場合、サーバルは動作しません。）

該当するチャンネルが複数ある場合、そのすべてで動作します。

### 応答

サーバルが動作するチャンネルに質問文と思われる発言があると「わかんないや」と応答し、そうでない発言があると「すごーい」と応答します。
