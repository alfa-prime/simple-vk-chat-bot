import requests
from vk_api.utils import get_random_id
from application.classes.commands import Commands
from application.classes.hunter import Hunter
from application.classes.keyboards import Keyboards
from application.classes.messages import Messages

from application.classes.user import User
from application.utilites.helpers import make_dir, remove_dir


class Dispatcher:
    def __init__(self, api, sender_id, upload):
        super().__init__()
        self.user_input = None
        self.api = api
        self.sender_id = sender_id
        self.sender_name = self.get_sender_name()
        self.user = None
        self.upload = upload
        self.targets = None
        self.targets_count = None

    def input(self, received_message):
        if received_message in Commands.start.value:
            self.got_command_start()

        elif received_message in Commands.help.value:
            self.got_command_help()

        elif received_message in Commands.search.value:
            self.got_command_search()

        elif received_message in Commands.choose_source_user.value:
            self.got_enter_and_set_source_user(received_message)

        elif received_message in Commands.choose_targets_sex.value:
            self.got_enter_and_set_target_sex(received_message)

        elif received_message in Commands.choose_targets_relation.value:
            self.got_enter_and_set_target_relation(received_message)

        elif received_message in Commands.choose_targets_age.value:
            return self.got_enter_and_set_target_age(received_message)

        elif self.user_input:
            """ получаем введеные пользователем значения """
            if self.user_input == 'enter_id':
                self.got_enter_user_id(received_message)

            elif self.user_input == 'age_from':
                self.got_enter_and_set_target_age_from(received_message)

            elif self.user_input == 'age_to':
                self.got_enter_and_set_target_age_to(received_message)

            elif self.user_input == 'choice_city':
                self.got_enter_and_set_search_option_city(received_message)

            elif self.user_input == 'enter_city_name':
                self.got_enter_and_set_city_name(received_message)

            elif self.user_input == 'process_targets':
                self.got_process_target_answer(received_message)

        else:
            self.got_command_unknown()

    def _send_message(self, message=None, keyboard=None, attachments=None):
        """ посылает сообщение пользователю """
        self.api.messages.send(peer_id=self.sender_id,
                               message=message,
                               keyboard=keyboard,
                               attachment=attachments,
                               random_id=get_random_id())

    def got_command_start(self):
        """ получена команда Начать """
        self._send_message(Messages.welcome(self.sender_name), keyboard=Keyboards.main())

    def got_command_help(self):
        """ получена команда Инфо """
        self._send_message(Messages.info(), keyboard=Keyboards.search())

    def got_command_unknown(self):
        """ получена неизвестная команда """
        self._send_message(Messages.unknown_command(), keyboard=Keyboards.main())

    def got_command_search(self):
        """ получена команда Поиск """
        self._send_message(Messages.choose_source_user(self.sender_name), Keyboards.choose_source_user())

    def got_enter_and_set_source_user(self, received_message):
        """
        выбираем для кого ищем,
        для текущего пользователя,
        для другого пользователя (будет запрошен id)
        """
        if received_message == 'для меня':
            self.user = User(self.sender_id)
            self.ask_search_option_sex()
        elif received_message == 'не для меня':
            self.user_input = 'enter_id'
            self._send_message('Введите id:')

    def got_enter_user_id(self, received_message):
        """ получен id пользователя """
        search_user_id = received_message
        self.user = User(search_user_id)
        # проверяем id на валидность
        check_result, check_result_message = self.check_user_error_or_deactivated()

        if check_result:
            self.ask_search_option_sex()
        else:
            self._send_message(check_result_message, Keyboards.new_search())

    def ask_search_option_sex(self):
        self._send_message(Messages.ask_search_option_sex(), Keyboards.ask_search_option_sex())

    def got_enter_and_set_target_sex(self, received_message):
        """
        пользователь выбирает кого пола будут кандидаты
        id 1: женский, 2: мужской
        https://vk.com/dev/users.search параметр sex
        """
        if received_message == 'мужчин':
            self.user.search_attr['sex_id'] = 2
        elif received_message == 'женщин':
            self.user.search_attr['sex_id'] = 1

        self.ask_search_option_relation()

    def ask_search_option_relation(self):
        self._send_message(Messages.ask_search_option_relation(), Keyboards.ask_search_option_relation())

    def got_enter_and_set_target_relation(self, received_message):
        """
        пользователь выбирает статус отношений
        id 1: не женат/не замужем 6: в активном поиске
        https://vk.com/dev/users.search параметр sex
        """
        if received_message == 'не женат/не замужем':
            self.user.search_attr['relation_id'] = 1
        elif received_message == 'в активном поиске':
            self.user.search_attr['relation_id'] = 6

        self.ask_search_option_age()

    def ask_search_option_age(self):
        if self.user.age:
            self._send_message(Messages.ask_search_option_with_age(),
                               Keyboards.ask_search_option_with_age())
        else:
            self._send_message(Messages.ask_search_option_without_age(),
                               Keyboards.ask_search_option_without_age())

    def got_enter_and_set_target_age(self, received_message):
        if received_message == 'диапазон':
            self.ask_search_option_age_from()

        elif received_message == 'ровестники':
            age_from = self.user.age - 2
            age_to = self.user.age + 2
            self.user.search_attr['age_from'] = age_from
            self.user.search_attr['age_to'] = age_to
            self.ask_search_option_city()

    def ask_search_option_age_from(self):
        self.user_input = 'age_from'
        self._send_message(Messages.ask_search_option_age_from())

    def got_enter_and_set_target_age_from(self, received_message):
        try:
            self.user.search_attr['age_from'] = int(received_message)
            self.user_input = 'age_to'
            self._send_message(Messages.ask_search_option_age_to())
        except ValueError:
            self._send_message(Messages.entered_age_is_not_valid())
            self.ask_search_option_age_from()

    def ask_search_option_age_to(self):
        self._send_message(message=Messages.ask_search_option_age_to())

    def got_enter_and_set_target_age_to(self, received_message):
        try:
            self.user.search_attr['age_to'] = int(received_message)
            self.user_input = None
            self.ask_search_option_city()
        except ValueError:
            self._send_message(Messages.entered_age_is_not_valid())
            self.ask_search_option_age_to()

    def ask_search_option_city(self):
        self.user_input = 'choice_city'
        self._send_message(Messages.ask_search_option_city(),
                           Keyboards.ask_search_option_city(self.user.city_name))

    def got_enter_and_set_search_option_city(self, received_message):
        if received_message == self.user.city_name.lower():
            self.user.search_attr['city_id'] = self.user.city_id
            self.process_targets()
        else:
            self.ask_city_name_and_search()

    def ask_city_name_and_search(self):
        self.user_input = 'enter_city_name'
        self._send_message('Введите название города')

    def got_enter_and_set_city_name(self, city_name):
        result = self.user.api.database.getCities(q=city_name, country_id=1)
        if result.get('items'):
            self.user.search_attr['city_id'] = result.get('items')[0].get('id')
            self.user.city_id = result.get('items')[0].get('id')
            self.user.city_name = result.get('items')[0].get('title')
            self.process_targets()
        else:
            self._send_message(f"'{city_name}' не обнаружен. Попробуем заново.")
            self.ask_city_name_and_search()

    def process_targets(self):
        self._send_message(Messages.search_start())
        hunter = Hunter(self.user)
        self._send_message(f'Найдено: {hunter.targets_count}')
        self.targets = hunter.targets
        self.targets_count = hunter.targets_count
        self.next_target()

    def next_target(self):
        self.user_input = 'process_targets'
        try:
            target = next(self.targets)
            index, target_id, name, link, bdate = target.split(',')
            attachments = self._process_profile_photos(int(target_id))
            self._send_message(f'{index} из {self.targets_count}', attachments=attachments)
            self._send_message(Messages.target_info(bdate, name, link), Keyboards.process_target())
        except StopIteration:
            self._send_message('Больше кандидатур нет', Keyboards.new_search())

    def got_process_target_answer(self, answer):
        if answer == 'да':
            self.next_target()
        elif answer == 'нет':
            self.next_target()
        elif answer == 'не знаю':
            self.next_target()
        elif answer == 'прервать поиск':
            self._send_message('Поиск прерван', Keyboards.new_search())

    def get_sender_name(self):
        """ получает имя пользователя по его id """
        return self.api.users.get(user_id=self.sender_id)[0].get('first_name')

    def check_user_error_or_deactivated(self):
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

    def _process_profile_photos(self, target_id):
        """
        получаем фотографии профиля пользователя, если фотографий больше трех, то только топ-3 по лайкам
        """
        photos = self.user.api.photos.get(owner_id=target_id, album_id='profile', extended=1, count=1000)
        photos_count = photos.get('count')

        if photos_count == 0:
            # получаем аватарку из свойств пользователя, так как по непонятным для меня причинам при заданных
            # параметрах поиска все равно есть пользватели, у которых в альбоме profile нет фотографий
            # используется метод vk api https://vk.com/dev/users.get
            # метод экспериментальный, протестирован только на одном известном случае

            user_info = self.user.api.users.get(user_ids=target_id, fields='photo_max_orig')[0]
            avatar_url = user_info.get('photo_max_orig')
            request = requests.get(avatar_url)
            make_dir('temp')

            with open('temp\\avatar.jpg', 'wb') as file:
                file.write(request.content)

            image = 'temp\\avatar.jpg'
            upload_image = self.upload.photo_messages(photos=image)[0]
            remove_dir('temp')

            return f'photo{upload_image.get("owner_id")}_{upload_image.get("id")}'

        elif photos_count > 3:
            photos_ids_with_likes = {v.get('id'): v.get('likes').get('count') for v in photos.get('items')}
            top_three_photos_ids = sorted(photos_ids_with_likes.items(), key=lambda x: x[1], reverse=True)[:3]
            return [f'photo{target_id}_{v[0]}' for v in top_three_photos_ids]

        else:
            return [f'photo{target_id}_{v.get("id")}' for v in photos.get('items')]
