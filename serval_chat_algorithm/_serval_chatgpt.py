from typing import Optional, Iterable, Generator, Sequence

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


class ChatgptChatAlgorithm(discord_bot.ChatAlgorithm):
    """ChatGPT によるチャットボットの応答アルゴリズム
    """
    _channels: Optional[Sequence[int]]
    _model: Optional[str]
    _initial_instruction: str
    _chatgpt_adapter: Generator[str, str, None]

    def __init__(self, *, model: Optional[str] = None, channels: Optional[Sequence[int]] = None,
                 initial_instruction: Optional[str], api_key: str):
        self._model = model if model is not None else "gpt-3.5-turbo"
        self._channels = channels

        if initial_instruction is None:
            initial_instruction = "あなたは、けものフレンズのサーバルちゃんになりきって会話してください。いいですね。"
        self._initial_instruction = initial_instruction

        openai.api_key = api_key
        self._chatgpt_adapter = self.generate_message()
        next(self._chatgpt_adapter)

    def generate_message(self) -> Generator[str, str, None]:
        """文脈を維持してChatGPTとやりとりするgenerator"""

        messages = [
            {"role": "system", "content": self._initial_instruction},
        ]
        user_message = yield
        messages.append({"role": "user", "content": user_message})

        while True:
            res = openai.ChatCompletion.create(
                model=self._model,
                messages=messages,
            )
            # TODO: エラーが返ってきた際の処理など
            res_message = res['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": res_message})

            user_message = yield res['choices'][0]['message']['content']
            messages.append({"role": "user", "content": user_message})

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

        return self._chatgpt_adapter.send(message.content)
