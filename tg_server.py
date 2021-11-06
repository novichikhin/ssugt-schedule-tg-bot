import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.config import config
from src.tg.handlers import register_handlers


async def main() -> None:
    logging.basicConfig(filename='tg_server.log', format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    storage = MemoryStorage()
    bot = Bot(token=config.TG_API_TOKEN)
    dp = Dispatcher(bot, storage=storage)

    register_handlers(dp)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
