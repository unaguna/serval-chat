import asyncio
import logging
import sys

import aioconsole

import discord_bot
from cnf import Config
from serval_chat_algorithm import ServalMecabChatAlgorithm, ChatgptChatAlgorithm


def _set_logger(name=None):
    formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')

    # INFO以下のログを標準出力する
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    stdout_handler.setFormatter(formatter)

    # WARNING以上のログを標準エラー出力する
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(formatter)

    # ロガーにハンドラを設定する
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)


def main():
    args = sys.argv
    config = Config("")
    config.from_pyfile(args[1])

    # アルゴリズム設定を選択
    chatbot_model = config["CHATBOT_MODEL"].casefold()
    if chatbot_model == "chatgpt":
        algorithm = ChatgptChatAlgorithm(model=config.get("CHATGPT_MODEL"),
                                         channels=config.get("DISCORD_CHANNELS"),
                                         initial_instruction=config.get("CHATGPT_INITIAL_INSTRUCTION"),
                                         api_key=config['CHATGPT_API_KEY'],
                                         context_dir_path=config.get("CHATGPT_CONTEXT_DIR"))
    elif chatbot_model == "simple_mecab":
        algorithm = ServalMecabChatAlgorithm()
    else:
        raise ValueError(config["CHATBOT_MODEL"])

    chat_bot = discord_bot.ChatBot(algorithm,
                                   bot_token=config['DISCORD_BOT_TOKEN'],
                                   name=config.get('NAME', 'サーバル'))

    # 何らかの標準入力があるまで待機し、標準入力があれば bot を停止する非同期関数
    async def wait_input_and_close():
        # キーボード入力があるまで待機
        await aioconsole.ainput()

        # bot を終了
        await chat_bot.close()

    # discord イベントの待機と、標準入力の待機を並列して行う
    asyncio.get_event_loop().run_until_complete(asyncio.gather(chat_bot.start(), wait_input_and_close()))


if __name__ == '__main__':
    _set_logger()
    main()
