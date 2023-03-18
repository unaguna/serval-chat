from typing import Optional, Iterable, Generator, Sequence, TextIO

import discord
import openai

import discord_bot


def _contains_any(target: str, candidate_list: Iterable[str]) -> bool:
    """指定した文字列に特定の文字列のいずれかが含まれるかどうかをチェックする。

    Args:
        target:
            候補文字列を含むかどうかを判定する文字列
        candidate_list:
            候補文字列からなるリスト

    Returns:
        target が candidate_list のいずれかの文字列を含むなら True、そうでないなら False。
    """
    for candidate in candidate_list:
        if candidate in target:
            return True
    return False


class Context:
    _channel_id: int
    _messages: list[dict]
    _write_fp: TextIO

    def __init__(self, *, channel_id: int, initial_instruction: str):
        self._channel_id = channel_id
        self._messages = [
            {"role": "system", "content": initial_instruction},
        ]

    def __enter__(self):
        self._write_fp = open(f"./env/{self._channel_id}.txt", mode="w+", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._write_fp.__exit__(exc_type, exc_val, exc_tb)

    def push_message(self, role: str, content: str):
        self._messages.append({"role": role, "content": content})
        self._write_fp.write(f"{role}\t{content}\n")

    def get_messages(self) -> Sequence[dict]:
        return self._messages


class ChatgptChatAlgorithm(discord_bot.ChatAlgorithm):
    """ChatGPT によるチャットボットの応答アルゴリズム
    """
    _channels: Optional[Sequence[int]]
    _model: Optional[str]
    _initial_instruction: str
    _chatgpt_adapters: dict[int, Generator[str, str, None]]

    def __init__(self, *, model: Optional[str] = None, channels: Optional[Sequence[int]] = None,
                 initial_instruction: Optional[str], api_key: str):
        self._model = model if model is not None else "gpt-3.5-turbo"
        self._channels = channels

        if initial_instruction is None:
            initial_instruction = "あなたは、けものフレンズのサーバルちゃんになりきって会話してください。いいですね。"
        self._initial_instruction = initial_instruction

        openai.api_key = api_key
        self._chatgpt_adapters = {}

    def close(self):
        for chatgpt_adapter in self._chatgpt_adapters.values():
            chatgpt_adapter.close()

    def generate_message(self, channel_id: int) -> Generator[str, str, None]:
        """文脈を維持してChatGPTとやりとりするgenerator"""

        with Context(channel_id=channel_id, initial_instruction=self._initial_instruction) as context:
            user_message = yield
            context.push_message("user", user_message)

            while True:
                res = openai.ChatCompletion.create(
                    model=self._model,
                    messages=context.get_messages(),
                )
                # TODO: エラーが返ってきた際の処理など
                res_message = res['choices'][0]['message']['content']
                context.push_message("assistant", res_message)

                user_message = yield res['choices'][0]['message']['content']
                context.push_message("user", user_message)

    def input_message(self, message: discord.Message, self_client: discord.Client) -> Optional[str]:
        # 自身や他のBotからのメッセージには応答しない
        if message.author.bot or message.author == self_client:
            return None

        if self._channels is not None:
            # 指定のチャンネル以外では応答しない
            if message.channel.id not in self._channels:
                return None
        else:
            # チャンネル名に特定文字列が含まれない場合は応答しない
            channel_name = message.channel.name
            if not _contains_any(channel_name, ('サバンナ', 'さばんな')):
                return None

        print('メッセージが送られました')
        print('サーバ', message.guild.name)
        print('チャンネル', message.channel.name)
        print('送信者', message.author.display_name)
        print('内容', message.content)

        if message.channel.id not in self._chatgpt_adapters:
            self._chatgpt_adapters[message.channel.id] = self.generate_message(message.channel.id)
            next(self._chatgpt_adapters[message.channel.id])

        return self._chatgpt_adapters[message.channel.id].send(message.content)
