from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id
import requests

from ..utilites.logger import set_logger
from ..utilites.helpers import make_dir, remove_dir
from ..classes.user import User
from ..classes.keyboards import Keyboards
from ..classes.messages import Messages
from ..classes.commands import Commands
from ..classes.hunter import Hunter

logger = set_logger(__name__)

class Dispatcher:
    def __init__(self, api, longpoll, upload):
        self.api = api
        self.longpoll = longpoll
        self.upload = upload
        self.sender_id = None
        self.sender_name = None
        self.user = None

    def process_message(self, received_message, sender_id):
        """ обрабатывает входящие сообщения пользователя, формирует ответ бота """
        self.sender_id = sender_id
        self.sender_name = self._get_sender_name()
        logger.info(f"{self.sender_name}: {received_message}")

        if received_message in Commands.start.value: received_message = 'старт'
        if received_message in Commands.help.value: received_message = 'помощь'
        if received_message in Commands.search.value: received_message = 'поиск'

        COMMANDS_MAPPER = {
            'старт': self._received_begin,
            'помощь': self._received_info,
            'поиск': self._received_search
        }

        if received_message in COMMANDS_MAPPER:
            COMMANDS_MAPPER.get(received_message)()
        else:
            self._send_message(Messages.unknown_command(), Keyboards.main())

    def _send_message(self, message=None, keyboard=None, attachments=None):
        """ посылает сообщение пользователю """
        self.api.messages.send(peer_id=self.sender_id,
                               message=message,
                               keyboard=keyboard,
                               attachment=attachments,
                               random_id=get_random_id())

        message = message.replace('\n\n', ' ').replace('\n', ' ')
        logger.info(f"Бот: {message}")

    def _received_begin(self):
        self._send_message(Messages.welcome(self.sender_name), Keyboards.main())

    def _received_info(self):
        self._send_message(Messages.info(), Keyboards.search())

    def _received_search(self):
        self._send_message(Messages.choose_whom_search(self.sender_name), Keyboards.choose_whom_search())
        user_choice = self._catch_user_input()

        if user_choice == 'для меня':
            self.user = User(self.sender_id)

        elif user_choice == 'не для меня':
            self._send_message(message='Введите id:')
            search_user_id = self._catch_user_input()
            self.user = User(search_user_id)

        check_result, check_result_message = self._check_user_error_or_deactivated()

        if check_result:
            self._send_message(Messages.user_info(self.user))
            self._set_search_option_by_sex()
            self._set_search_option_by_age()
            self._set_search_option_by_city()

            # self._send_message(f'Начинаем поиск {self.user}')
            self._send_message(f'Начинаем поиск.\n'
                               f'Пожалуйста, подождите немного.\n'
                               f'Идет сбор и обработка сведений.\n')

            hunter = Hunter(self.user)
            make_dir('temp')

            for index, (target_id, target_attr) in enumerate(hunter.targets.items()):

                r = requests.get(target_attr.get("photos").get("items")[0].get("url"))
                with open('temp\\pic.jpg', 'wb') as f:
                    f.write(r.content)

                image = 'temp\\pic.jpg'
                attachments = list()
                upload_image = self.upload.photo_messages(photos=image)[0]
                attachments.append(f'photo{upload_image.get("owner_id")}_{upload_image.get("id")}')

                self._send_message(Messages.target_info(target_attr), Keyboards.process_target(), attachments)

                answer = self._catch_user_input()

                if index != len(hunter.targets)-1:

                    if answer == 'да':
                        ...
                    elif answer == 'нет':
                        ...
                    elif answer == 'дальше':
                        ...
                    elif answer == 'прервать':
                        remove_dir('temp')
                        self._send_message('Поиск прерван', Keyboards.new_search())
                        break
                else:
                    remove_dir('temp')
                    self._send_message('Больше кандидатур нет', Keyboards.new_search())

        else:
            self._send_message(check_result_message, Keyboards.new_search())

    def _get_sender_name(self):
        """ получает имя пользователя по его id """
        return self.api.users.get(user_id=self.sender_id)[0].get('first_name')

    def _catch_user_input(self):
        """ ждет ввода значения от пользователя и возвращает его """
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                received_message = event.text.lower().strip()
                logger.info(f"{self.sender_name}: {received_message}")
                return received_message

    def _check_user_error_or_deactivated(self):
        """
        если аккаунт заблокирован или удален,
        возвращает соотвествующее сообщение для отправки в чат
        """
        if self.user.has_error:
            return False, self.user.has_error
        elif self.user.is_deactivated:
            return False, self.user.is_deactivated
        else:
            return True, None

    def _set_search_option_by_age(self):
        """
        если у юзера, которому подбирается пара, возраст определен
        дается возвожность выбора варианта поиска:
        1. ровестники [возраст пользователя +/- 2 года];
        2. возрастной диапазон [определяется пользователем],
        в противном случае, вариант один: возрастной диапазон [определяется пользователем]
        """
        if self.user.age:
            self._send_message(
                Messages.choose_search_option_by_age(self.user.age),
                Keyboards.choose_search_option_by_age()
            )
            user_choice = self._catch_user_input()
            if user_choice == 'диапазон':
                self._set_age_range()
            elif user_choice == 'ровестники':
                age_from = self.user.age - 2
                age_to = self.user.age + 2
                self.user.search_attr['age_from'] = age_from
                self.user.search_attr['age_to'] = age_to
        else:
            self._send_message(Messages.missing_age())
            self._set_age_range()

    def _set_age_range(self):
        """
        пользователь сам задет возрастной диапазон для поиска
        """
        while True:
            self._send_message('Введите начальное значение диапазона:')
            age_from = self._catch_user_input()
            self._send_message('Введите окончание диапазона:')
            age_to = self._catch_user_input()

            if age_from <= age_to:
                self.user.search_attr['age_from'] = age_from
                self.user.search_attr['age_to'] = age_to
                break
            else:
                self._send_message('Введный диапазон неверен. Попробуем заново.')

    def _set_search_option_by_sex(self):
        """
        пользователь сам выбирает кого пола будут кандидаты
        id пола  1: женский, 2: мужской, 0: любой
        значения ID можно посмотреть https://vk.com/dev/users.search параметр sex
        """
        self._send_message(
            message=Messages.choose_search_option_by_sex(self.user.sex),
            keyboard=Keyboards.choose_search_option_by_sex()
        )
        user_choice = self._catch_user_input()
        if user_choice == 'мужчин':
            self.user.search_attr['sex_id'] = 2
        elif user_choice == 'женщин':
            self.user.search_attr['sex_id'] = 1
        else:
            self.user.search_attr['sex_id'] = 0
            
    def _set_search_option_by_city(self):
        """
        если у юзера город указан, предлагаются варианты поиска:
        родной город, указать другой,
        в противном случае запрашивает имя города
        """

        if self.user.city_id:
            self._send_message(
                Messages.choose_search_option_by_city(self.user.city_name),
                Keyboards.choose_search_option_by_city(self.user.city_name)
            )
            user_choice = self._catch_user_input()
            if user_choice == self.user.city_name:
                self.user.search_attr['city_id'] = self.user.city_id
            elif user_choice == 'другой':
                self._set_city()
        else:
            self._send_message('Город: нет данных')
            self._set_city()

    def _set_city(self):
        """
        запрашивает название города, ищет его id
        поиск городов пока только по России [country_id=1]
        подробнее https://vk.com/dev/database.getCities
        """
        while True:
            self._send_message('Введите название города:')
            city_name = self._catch_user_input()
            result = self.user.api.database.getCities(q=city_name, country_id=1)
            if result.get('items'):
                self.user.search_attr['city_id'] = result.get('items')[0].get('id')
                self.user.city_id = result.get('items')[0].get('id')
                self.user.city_name = result.get('items')[0].get('title')
                break
            else:
                self._send_message(f"'{city_name}' не обнаружен. Попробуем заново.")
