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
        self.user = None

    def process_message(self, received_message, sender_id):
        """ обрабатывает входящие сообщения пользователя, формирует ответ бота """
        self.sender_id = sender_id
        self.sender_name = self._get_sender_name()
        logger.info(f"{self.sender_name}: {received_message}")

        if received_message == 'начать':
            self._send_message(message=Messages.welcome(self.sender_name), keyboard=Keyboards.main())

        elif received_message == 'инфо':
            self._send_message(message=Messages.info(), keyboard=Keyboards.search())

        elif received_message == 'поиск':
            self._send_message(message='Введите id:')
            search_user_id = self._catch_user_input()
            self.user = User(search_user_id)
            check_result, check_result_message = self._check_user_error_or_deactivated(self.user)

            if check_result:
                self._send_message(message=Messages.user_info(self.user))
                self._request_missing_data()
                self._set_search_option_by_age()
                self._set_search_option_by_sex()

                hunter = Hunter(self.user)
                hunter.search()

            else:
                self._send_message(message=check_result_message, keyboard=Keyboards.search())

        else:
            self._send_message(message='Неизвестная команда')

    def _get_sender_name(self):
        """ получает имя пользователя по его id """
        return self.api.users.get(user_id=self.sender_id)[0].get('first_name')

    def _send_message(self, message=None, keyboard=None):
        """ посылает сообщение пользователю """
        self.api.messages.send(peer_id=self.sender_id, message=message, keyboard=keyboard, random_id=get_random_id())
        message = message.replace('\n\n', ' ').replace('\n', ' ')
        logger.info(f"Бот: {message}")

    def _catch_user_input(self):
        """ ждет ввода значения от пользователя и возвращает его """
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                received_message = event.text.lower().strip()
                logger.info(f"{self.sender_name}: {received_message}")
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
        пользователь сам задет возрастной диапазон для поиска
        """
        while True:
            self._send_message(message='Введите начальное значение диапазона:')
            age_from = self._catch_user_input()
            self._send_message(message='Введите окончание диапазона:')
            age_to = self._catch_user_input()

            if age_from <= age_to:
                user.search_attr['age_from'] = age_from
                user.search_attr['age_to'] = age_to
                break
            else:
                self._send_message(message='Введный диапазон неверен. Попробуем заново:')

    def _request_missing_data(self):
        """ запрашивает недостающие данные для поиска """
        missing_data = {k: v for k, v in self.user.search_attr.items() if v is None}

        if 'age' in missing_data:
            self._send_message(message=Messages.missing_age())
            self._set_age_range(self.user)

    def _set_search_option_by_age(self):
        """
        если у юзера, которому подбирается пара, возраст определен
        дается возвожность выбора варианта поиска:
        1. ровестники [возраст пользователя +/- 2 года];
        2. возрастной диапазон [определяется пользователем]
        """
        if self.user.age:
            self._send_message(
                message=Messages.choose_search_option_by_age(self.user.age),
                keyboard=Keyboards.choose_search_option_by_age()
            )
            user_choice = self._catch_user_input()
            if user_choice == 'диапазон':
                self._set_age_range(self.user)
            elif user_choice == 'ровестники':
                age_from = self.user.age - 2
                age_to = self.user.age + 2
                self.user.search_attr['age_from'] = age_from
                self.user.search_attr['age_to'] = age_to

    def _set_search_option_by_sex(self):
        """
        пользователь сам выбирает кого пола будут кандидаты
        id пола  1: женский, 2: мужской, 0: любой
        значения ID можно посмотреть https://vk.com/dev/users.search параметр sex
        """
        self._send_message(
            message=Messages.choose_search_option_by_sex(self.user.sex_by_text),
            keyboard=Keyboards.choose_search_option_by_sex()
        )
        user_choice = self._catch_user_input()
        if user_choice == 'мужчины':
            self.user.search_attr['sex_id'] = 2
        elif user_choice == 'женщины':
            self.user.search_attr['sex_id'] = 1
        else:
            self.user.search_attr['sex_id'] = 0
