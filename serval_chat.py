import asyncio
import os

import aioconsole

import discord_bot
from serval_chat_algorithm import ServalMecabChatAlgorithm, ServalChatgptChatAlgorithm


def main():
    bot_token = os.environ.get('SERVAL_CHAT_TOKEN')

    if bot_token is None:
        raise ValueError('環境変数に SERVAL_CHAT_TOKEN (使用するボットトークン) が指定されていません')

    chat_bot = discord_bot.ChatBot(ServalChatgptChatAlgorithm(os.environ['SERVAL_CHAT_CHATGPT_TOKEN']), bot_token,
                                   name='サーバル')

    # 何らかの標準入力があるまで待機し、標準入力があれば bot を停止する非同期関数
    async def wait_input_and_close():
        # キーボード入力があるまで待機
        await aioconsole.ainput()

        # bot を終了
        await chat_bot.close()

    # discord イベントの待機と、標準入力の待機を並列して行う
    asyncio.get_event_loop().run_until_complete(asyncio.gather(chat_bot.start(), wait_input_and_close()))


if __name__ == '__main__':
    main()
