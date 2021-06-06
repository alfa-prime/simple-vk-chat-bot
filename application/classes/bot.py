from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id

from ..utilites.logger import set_logger
from ..classes.dispatcher import Dispatcher
from ..classes import BotAuthorization

logger = set_logger(__name__)

class Bot(BotAuthorization):
    def __init__(self):
        super().__init__()

        self.sender_id = None
        self.users = dict()

    def _send_message(self, sender_id=None, message=None, keyboard=None, attachments=None):
        """ посылает сообщение пользователю """
        self.api.messages.send(peer_id=sender_id,
                               message=message,
                               keyboard=keyboard,
                               attachment=attachments,
                               random_id=get_random_id())

        # message = message.replace('\n\n', ' ').replace('\n', ' ')
        logger.info(f"Бот: {message}")

    def start(self):
        logger.info('Бот успешно стартовал')

        while True:
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    received_message = event.text.lower().strip()
                    self.sender_id = event.user_id

                    if event.user_id not in self.users:
                        self.users[event.user_id] = Dispatcher(self.api, event.user_id, self.upload)

                    if event.type == VkEventType.MESSAGE_NEW:
                        self.users[event.user_id].input(received_message)
