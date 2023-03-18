# Serval Chat (discord bot)

Serval Chat は、仮想人格「サーバル」と対話できる discord bot です。


## 依存関係

本モジュールの動作には以下のソフトウェアを使用します。

- Python 3.10 以上の実行環境
- (使うモデルによっては不要) MeCab (バージョン 0.996 で動作確認)
    - 形態素解析ツールです。discord で受け取った他人の発言を解析するために使用します。


## 起動方法

1. (使うモデルによっては不要) [MeCab](https://taku910.github.io/mecab/#download) 本体と辞書をダウンロードし、インストールする。（windows では、辞書付きのバイナリパッケージをダウンロード・インストールするだけで済みます）

1. Discord Developer Portal で Application と Bot を作成する。このとき、Bot の "Message Content Intent" を ON にする。
    - 補足: 作成した Bot のトークンは後で使用する。

1. 作成した Bot を、サーバルと会話したいサーバに招待する。

1. Python 3.10 以上が動作する環境を作る。
    - **注意**: python の x86 or x64 は、MeCab のものに合わせること。
   
1. 下記のコマンドで必要パッケージをインストールする。
    ```shell
    # python の仮想環境を使う場合は、使用した仮想環境作成方法に応じて、conda コマンドなり Activate.ps1 や Activate.bat なりを使っておく
    pip install aioconsole
    pip install discord.py
    pip install mecab
    pip install openai
    ```

1. このリポジトリをダウンロードし、config.py を作成して設定を記載し、serval_chat.py を実行する。

   - config.py の内容例
      ```python
      # 利用するモデル
      CHATBOT_MODEL = "simple_mecab"  # 2種類の返答ができるモデル
      # CHATBOT_MODEL = "chatgpt"  # ChatGPTを利用するモデル

      # Discord の Bot トークン
      DISCORD_BOT_TOKEN = "xxxxxx"
         
      # モデル chatgpt を使う場合の、Bot が応答するチャンネルID (指定なしならチャンネル名に「さばんな」か「サバンナ」が含まれるチャンネルに応答する)
      # DISCORD_CHANNELS = [
      #     0,
      # ]
         
      # モデル chatgpt を使う場合の、ChatGPT API key
      # CHATGPT_API_KEY = "sk-xxxxxx"
        
      # モデル chatgpt を使う場合の最初の指示。指定しない場合、サーバルとして振舞うことを依頼する。
      # CHATGPT_INITIAL_INSTRUCTION = ""
      ```
    - PowerShell での実行例
        ```shell
        # カレントディレクトリは serval_chat.py があるディレクトリに移しておく
        python serval_chat.py ./config.py
        ```
    
1. Discord 上でサーバルがオンラインになっていれば成功。
    - 次回以降は、serval_chat.py のみで起動できます。


## 動作仕様

特定のテキストチャンネルで、他の人の発言に反応して発言します。

### 動作するチャンネル

サーバルを招待したサーバに「さばんな」もしくは「サバンナ」が付くテキストチャンネルがあれば、そこで動作します。（config.py にチャンネルIDを指定した場合は指定したチャンネルで動作します。該当するチャンネルがない場合、サーバルは動作しません。）

該当するチャンネルが複数ある場合、そのすべてで動作します。

### 応答

config.py で設定したモデルによって、以下の応答をします。

#### simple-mecab

サーバルが動作するチャンネルに質問文と思われる発言があると「わかんないや」と応答し、そうでない発言があると「すごーい」と応答します。

#### chatgpt

ChatGPT に発言を送信し、その返答をそのまま応答します。
