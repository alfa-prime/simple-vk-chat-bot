import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from application.settings import BOT_TOKEN
from ..utilites.logger import set_logger

logger = set_logger(__name__)

class BotAuht:
    def __init__(self):
        session = vk_api.VkApi(token=BOT_TOKEN)
        self.api = session.get_api()
        self.longpoll = VkLongPoll(session)

class Bot(BotAuht):
    def __init__(self):
        super().__init__()

    def start(self):
        logger.info('Бот успешно стартовал')

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                received_message = event.text.lower().strip()
                print(received_message)

