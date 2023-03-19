import asyncio
import logging
import sys
from abc import ABC, abstractmethod
from typing import Optional

import aioconsole
import discord
from discord import Interaction
from discord.app_commands import CommandTree


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

    @abstractmethod
    def forget_context(self, interaction: Interaction):
        """文脈をリセットする"""
        ...

    def close(self):
        pass


class ChatBot:
    """discord のチャットボット。

    discord への接続と送受信を行う。
    """
    _intents: discord.Intents
    _command_tree: CommandTree
    _chat_algorithm: ChatAlgorithm
    _bot_token: str
    _name: str

    def __init__(self, algorithm: ChatAlgorithm, bot_token: str, name: str = 'Chat Bot'):
        self._chat_algorithm = algorithm
        self._bot_token = bot_token
        self._name = name
        self._intents = discord.Intents.default()
        self._intents.message_content = True
        self._client = discord.Client(intents=self._intents)
        self._command_tree = CommandTree(self._client)

        self._client.event(self.on_ready)
        self._client.event(self.on_message)

        @self._command_tree.command(description="このチャンネルでの会話の文脈をリセットします。")
        async def forget_context(interaction: Interaction):
            await self.command_forget_context(interaction)

    async def start(self):
        await self._client.start(self._bot_token)

    async def close(self):
        logging.getLogger("servalchat.console").info(f'{self._name} を停止します')
        self._chat_algorithm.close()
        await self._client.change_presence(status=discord.Status.offline)
        await self._client.close()

    async def command_forget_context(self, interaction: Interaction):
        self._chat_algorithm.forget_context(interaction)
        await interaction.response.send_message("文脈をリセットしました")

    async def on_ready(self):
        await self._command_tree.sync()
        logging.getLogger("servalchat.console").info(f'{self._name} が起動しました')

    async def on_message(self, message: discord.Message):
        logging.getLogger("servalchat.discord").debug(f"メッセージが送られました; server={message.guild.name}, "
                                                      f"channel={message.channel.name}, "
                                                      f"sender={message.author.display_name}, "
                                                      f"content={message.content}")

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
