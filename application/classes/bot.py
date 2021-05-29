from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id

from ..utilites.logger import set_logger
from ..classes.dispatcher import Dispatcher
from ..classes.user import User
from ..classes import BotAuthorization
from ..classes.keyboards import Keyboards

logger = set_logger(__name__)

class Bot(BotAuthorization):
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

                if received_message == 'поиск':
                    self._send_message(sender_id, dict(message='Введите id или screen_name:'))
                    search_user_id = self._catch_user_input()
                    user = User(search_user_id)
                    result, result_message = self._check_user_error_deactivated(user)

                    if result:
                        if not user.age:
                            self._send_message(sender_id, dict(message='Введите возраст:'))
                            age = self._catch_user_input()
                            user.search_attr['age'] = age
                            user.age = age
                            message = dict(message=user)
                        else:
                            message = dict(message=user)
                    else:
                        message = result_message
                else:
                    message = dispatcher.process_message(received_message, sender_name)

                self._send_message(sender_id, message)

    def _catch_user_input(self):
        """ ждет ввода значения от пользователя и возвращает его """
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                return event.text.lower().strip()

    @staticmethod
    def _check_user_error_deactivated(user):
        """
        если аккаунт заблокирован или удален,
        возвращает соотвествующее сообщение для отправки в чат
        """
        if user.has_error:
            return False, dict(message=user.has_error, keyboard=Keyboards.search())
        elif user.is_deactivated:
            return False, dict(message=user.is_deactivated, keyboard=Keyboards.search())
        else:
            return True, None

    def _send_message(self, sender_id, message):
        """ посылает сообщение пользователю """
        self.api.messages.send(peer_id=sender_id, **message, random_id=get_random_id())
        logger.info(f"Бот: {message}")

    def _get_user_name(self, user_id):
        """ получает имя пользователя по его id """
        return self.api.users.get(user_id=user_id)[0].get('first_name')
