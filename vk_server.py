import asyncio
import logging

from vkbottle.bot import Bot

from src.config import config
from src.vk.blueprints import register_blueprints


async def main() -> None:
    logging.basicConfig(filename='vk_server.log', format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    bot = Bot(config.VK_ACCESS_TOKEN)
    register_blueprints(bot)

    await bot.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
