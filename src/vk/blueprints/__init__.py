import src.vk.blueprints.start
import src.vk.blueprints.states
import src.vk.blueprints.schedule

from vkbottle import Bot


def register_blueprints(bot: Bot):
    src.vk.blueprints.start.bp.load(bot)
    src.vk.blueprints.states.bp.load(bot)
    src.vk.blueprints.schedule.bp.load(bot)
