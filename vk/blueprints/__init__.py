import vk.blueprints.start
import vk.blueprints.states
import vk.blueprints.schedule

from vkbottle import Bot

def register_blueprints(bot: Bot):
    vk.blueprints.start.bp.load(bot)
    vk.blueprints.states.bp.load(bot)
    vk.blueprints.schedule.bp.load(bot)