import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from ..utilites.logger import set_logger
from ..classes.dispatcher import Dispatcher
from ..classes.user import User

from application.settings import BOT_TOKEN

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
        dispatcher = Dispatcher()

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                received_message = event.text.lower().strip()
                sender_id = event.user_id
                sender_name = self._get_user_name(sender_id)
                logger.info(f"{sender_name}: {received_message}")

                if '#' in received_message:
                    self._process_search(received_message[1:], sender_id)
                else:
                    message = dispatcher.process_message(received_message, sender_name)
                    self._send_message(sender_id, **message)

    def _process_search(self, user_id, sender_id):
        """ обработка поискового запроса """
        user = User(user_id)

        if user.has_error:
            message = dict(message=user.has_error)
        elif user.is_deactivated:
            message = dict(message=user.is_deactivated)
        else:
            message = dict(message=user)

        self._send_message(sender_id, **message)
                
    def _send_message(self, sender_id, message):
        """ посылает сообщение пользователю """
        self.api.messages.send(peer_id=sender_id, message=message, random_id=get_random_id())
        logger.info(f"Бот: {message}")

    def _get_user_name(self, user_id):
        """ получает имя пользователя по его id """
        return self.api.users.get(user_id=user_id)[0].get('first_name')
