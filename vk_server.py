import asyncio
from dependencies import *
from vkbottle.bot import Bot
from vk.config import VkConfig
from vk.blueprints import register_blueprints

async def main():
    logging.basicConfig(filename='vk_server.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    bot = Bot(VkConfig.ACCESS_TOKEN)
    register_blueprints(bot)

    await bot.run_polling()

if __name__ == '__main__':
    asyncio.run(main())