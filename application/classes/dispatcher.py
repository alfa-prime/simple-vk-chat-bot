from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id

from ..utilites.logger import set_logger
from ..classes.user import User
from ..classes.keyboards import Keyboards

logger = set_logger(__name__)

class Dispatcher:
    def __init__(self, api, longpoll):
        self.api = api
        self.longpoll = longpoll

    def _send_message(self, sender_id, message):
        """ посылает сообщение пользователю """
        self.api.messages.send(peer_id=sender_id, **message, random_id=get_random_id())
        logger.info(f"Бот: {message}")

    def _catch_user_input(self, sender_name):
        """ ждет ввода значения от пользователя и возвращает его """
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                received_message = event.text.lower().strip()
                logger.info(f"{sender_name}: {received_message}")
                return received_message

    def process_message(self, received_message, sender_id):
        """ обрабатывает входящие сообщения пользователя, формирует ответ бота """
        sender_name = self._get_sender_name(sender_id)
        logger.info(f"{sender_name}: {received_message}")

        if received_message == 'начать':
            message_body = f'Здравствуйте, {sender_name}\n' \
                      f'Для поиска пары, используйте команду "Поиск"\n' \
                      f'Подробности по команде "Инфо"\n'
            reply_message = dict(message=message_body, keyboard=Keyboards.main())

        elif received_message == 'инфо':
            message_body = f'По команде "Поиск"\n' \
                      f'бот запрашивает id или screen_name пользователя ВК,\n' \
                      f'для которого будет подыскивается пара.\n' \
                      f'После проверки id на валидность, \n' \
                      f'бот пытается собрать необходимые для поиска данные,\n' \
                      f'если какие-то не найдены, то просит у пользователя ввести их.'
            reply_message = dict(message=message_body, keyboard=Keyboards.search())

        elif received_message == 'поиск':
            self._send_message(sender_id, dict(message='Введите id или screen_name:'))
            search_user_id = self._catch_user_input(sender_name)
            user = User(search_user_id)

            check_result, check_result_message = self._check_user_error_or_deactivated(user)

            if check_result:
                reply_message = dict(message=user)
            else:
                reply_message = check_result_message

        else:
            reply_message = dict(message='Неизвестная команда')

        self._send_message(sender_id, reply_message)

    @staticmethod
    def _check_user_error_or_deactivated(user):
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

    def _get_sender_name(self, user_id):
        """ получает имя пользователя по его id """
        return self.api.users.get(user_id=user_id)[0].get('first_name')