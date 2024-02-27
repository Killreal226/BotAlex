import asyncio

from aiogram import Bot, Dispatcher
from loguru import logger

from app.config import config
from app.database import engine
from app.service.bot_tools.gpt_tools import Openai_API
from app.service.bot_tools.handlers import BoardSelectorHandlers, OtherHandlers


async def main():
    logger.add(config.LOG_FILE, rotation="1024 MB", level="INFO")

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    openai_api = Openai_API(config.OPENAI_TOKEN, config.DATA_MESSAGES["template_for_gpt"])
    BoardSelectorHandlers(dp, config.DATA_MESSAGES["messages_for_answers"], openai_api)
    OtherHandlers(dp, config.DATA_MESSAGES["messages_for_answers"])

    await dp.start_polling(bot)
    await engine.dispose()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
