from vk_api.longpoll import VkEventType

from ..utilites.logger import set_logger
from ..classes.dispatcher import Dispatcher
from ..classes import BotAuthorization

logger = set_logger(__name__)

class Bot(BotAuthorization):
    def __init__(self):
        super().__init__()

    def start(self):
        logger.info('Бот успешно стартовал')
        dispatcher = Dispatcher(self.api, self.longpoll, self.upload)

        for event in self.longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

                received_message = event.text.lower().strip()
                sender_id = event.user_id
                dispatcher.process_message(received_message, sender_id)
