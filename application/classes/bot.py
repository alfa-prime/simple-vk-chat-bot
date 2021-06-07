from vk_api.longpoll import VkEventType

from ..utilites.logger import set_logger
from ..classes.dispatcher import Dispatcher
from ..classes import BotAuthorization

logger = set_logger(__name__)

class Bot(BotAuthorization):
    def __init__(self):
        super().__init__()
        self.users = dict()

    def start(self):
        logger.info('Бот успешно стартовал')

        while True:
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    received_message = event.text.lower().strip()

                    if event.user_id not in self.users:
                        self.users[event.user_id] = Dispatcher(self.api, event.user_id, self.upload)

                    if event.type == VkEventType.MESSAGE_NEW:
                        self.users[event.user_id].input(received_message)
