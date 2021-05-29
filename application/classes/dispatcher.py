from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id

from ..utilites.logger import set_logger
from ..classes.user import User
from ..classes.keyboards import Keyboards
from ..classes.messages import Messages
from ..classes.hunter import Hunter

logger = set_logger(__name__)

class Dispatcher:
    def __init__(self, api, longpoll):
        self.api = api
        self.longpoll = longpoll
        self.sender_id = None
        self.sender_name = None

    def process_message(self, received_message, sender_id):
        """ обрабатывает входящие сообщения пользователя, формирует ответ бота """
        self.sender_id = sender_id
        self.sender_name = self._get_sender_name(sender_id)
        logger.info(f"{self.sender_name}: {received_message}")

        if received_message == 'начать':
            self._send_message(message=Messages.welcome(self.sender_name), keyboard=Keyboards.main())

        elif received_message == 'инфо':
            self._send_message(message=Messages.info(), keyboard=Keyboards.search())

        elif received_message == 'поиск':
            self._send_message(message='Введите id:')
            search_user_id = self._catch_user_input(self.sender_name)
            user = User(search_user_id)
            check_result, check_result_message = self._check_user_error_or_deactivated(user)

            if check_result:
                self._send_message(message='Найденые сведения о пользователе:')
                self._send_message(message=Messages.user_info(user))

                missing_data = {k: v['msg_if_val_none'] for k, v in user.search_attr.items() if v['value'] is None}

                if missing_data.get('age'):
                    self._send_message(message=missing_data.get('age'))
                    self._set_age_range(user)

                hunter = Hunter(user)
                hunter.search()

            else:
                self._send_message(message=check_result_message, keyboard=Keyboards.search())

        else:
            self._send_message(message='Неизвестная команда')

    def _get_sender_name(self, user_id):
        """ получает имя пользователя по его id """
        return self.api.users.get(user_id=user_id)[0].get('first_name')

    def _send_message(self, message=None, keyboard=None):
        """ посылает сообщение пользователю """
        self.api.messages.send(peer_id=self.sender_id, message=message, keyboard=keyboard, random_id=get_random_id())
        logger.info(f"Бот: {message}")

    def _catch_user_input(self, sender_name):
        """ ждет ввода значения от пользователя и возвращает его """
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                received_message = event.text.lower().strip()
                logger.info(f"{sender_name}: {received_message}")
                return received_message

    @staticmethod
    def _check_user_error_or_deactivated(user):
        """
        если аккаунт заблокирован или удален,
        возвращает соотвествующее сообщение для отправки в чат
        """
        if user.has_error:
            return False, user.has_error
        elif user.is_deactivated:
            return False, user.is_deactivated
        else:
            return True, None

    def _set_age_range(self, user):
        """
        в случае отсутсвия данных о возрасте,
        задаем возрастной диапазон
        """
        while True:
            self._send_message(message='Введите начальное значение диапазона:')
            age_from = self._catch_user_input(self.sender_name)
            self._send_message(message='Введите окончание диапазона:')
            age_to = self._catch_user_input(self.sender_name)

            if age_from < age_to:
                self._send_message(message=f'Введенный возрастной диапазон {age_from}-{age_to}')
                user.search_attr['age_from']['value'] = age_from
                user.search_attr['age_to']['value'] = age_to
                break
            else:
                self._send_message(message='Введный диапазон неверен. Попробуем заново:')
