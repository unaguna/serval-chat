import asyncio
import sys
from abc import ABC, abstractmethod
from typing import Optional

import aioconsole
import discord


class ChatAlgorithm(ABC):

    @abstractmethod
    def input_message(self, message: discord.Message, self_client: discord.Client) -> Optional[str]:
        """discord のメッセージを受け取り、内容に応じて送信する文章を返す。

        Args:
            message:
                受信したメッセージ
            self_client:
                Bot自身の Client オブジェクト

        Returns:
            botからメッセージを送る場合は、その内容。送らない場合は None。
        """
        ...


class ChatBot:
    """discord のチャットボット。

    discord への接続と送受信を行う。
    """
    _chat_algorithm: ChatAlgorithm
    _bot_token: str
    _name: str

    def __init__(self, algorithm: ChatAlgorithm, bot_token: str, name: str = 'Chat Bot'):
        self._chat_algorithm = algorithm
        self._bot_token = bot_token
        self._name = name
        self._client = discord.Client()

        self._client.event(self.on_ready)
        self._client.event(self.on_message)

    async def start(self):
        await self._client.start(self._bot_token)

    async def close(self):
        print(f'{self._name} を停止します')
        await self._client.change_presence(status=discord.Status.offline)
        await self._client.close()

    async def on_ready(self):
        print(f'{self._name} が起動しました')

    async def on_message(self, message: discord.Message):
        response = self._chat_algorithm.input_message(message, self._client)

        # 送信メッセージが指定された場合、メッセージを送信する。
        if response is not None:
            # メッセージの送信先
            channel = message.channel

            await channel.send(response)


if __name__ == '__main__':
    # サンプルの BOT を起動する。
    # トークンは実行時引数に指定すること。
    # 標準入力で Enter を入力することで停止する。

    args = sys.argv[1:]

    if len(args) < 1:
        print('引数が不足しています。', file=sys.stderr)
        exit(1)

    token = args[0]

    class SampleChatAlgorithm(ChatAlgorithm):
        def input_message(self, message: discord.Message, self_client: discord.Client) -> Optional[str]:
            # Botからのメッセージには応答しない
            if message.author.bot:
                return None

            print('メッセージが送られました')
            print('サーバ', message.guild.name)
            print('チャンネル', message.channel.name)
            print('送信者', message.author.display_name)
            print('内容', message.content)

            # 特定の内容の文が送られたらメッセージを送り返す
            if message.author != self_client and message.content == 'foo':
                return 'bar'

            return None

    chat_bot = ChatBot(SampleChatAlgorithm(), token, name='Sample Chat Bot')

    # 何らかの標準入力があるまで待機し、標準入力があれば bot を停止する非同期関数
    async def wait_input_and_close():
        # キーボード入力があるまで待機
        await aioconsole.ainput()

        # bot を終了
        await chat_bot.close()

    # discord イベントの待機と、標準入力の待機を並列して行う
    asyncio.get_event_loop().run_until_complete(asyncio.gather(chat_bot.start(), wait_input_and_close()))
