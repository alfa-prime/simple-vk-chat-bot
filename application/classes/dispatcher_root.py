from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id

from ..utilites.logger import set_logger

logger = set_logger(__name__)

class DispatcherRoot:
    def __init__(self):
        self.sender_id = None
        self.sender_name = None
        self.user = None
        self.api = None
        self.longpoll = None
        self.upload = None

    def _send_message(self, message=None, keyboard=None, attachments=None):
        """ посылает сообщение пользователю """
        self.api.messages.send(peer_id=self.sender_id,
                               message=message,
                               keyboard=keyboard,
                               attachment=attachments,
                               random_id=get_random_id())

        message = message.replace('\n\n', ' ').replace('\n', ' ')
        logger.info(f"Бот: {message}")

    def _catch_user_input(self):
        """ ждет ввода значения от пользователя и возвращает его """
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                received_message = event.text.lower().strip()
                logger.info(f"{self.sender_name}: {received_message}")
                return received_message
