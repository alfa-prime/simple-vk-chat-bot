import requests

from .keyboards import Keyboards
from .messages import Messages
from ..classes.dispatcher_root import DispatcherRoot
from ..utilites.helpers import make_dir, remove_dir

from ..utilites.logger import set_logger

logger = set_logger(__name__)

class DispatcherTools(DispatcherRoot):
    def __init__(self):
        super().__init__()

    def _get_sender_name(self):
        """ получает имя пользователя по его id """
        return self.api.users.get(user_id=self.sender_id)[0].get('first_name')

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

    def _set_search_option_by_sex(self):
        """
        пользователь выбирает кого пола будут кандидаты
        id пола  1: женский, 2: мужской
        https://vk.com/dev/users.search параметр sex
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

    def _set_search_option_by_relation(self):
        """
        пользователь выбирает статус отношений
        id 1: не женат/не замужем 6: в активном поиске
        https://vk.com/dev/users.search параметр sex
        """
        self._send_message(
            message=Messages.choose_search_option_by_relation(),
            keyboard=Keyboards.choose_search_option_by_relation()
        )
        user_choice = self._catch_user_input()
        if user_choice == 'не женат/не замужем':
            self.user.search_attr['relation_id'] = 1
        elif user_choice == 'в активном поиске':
            self.user.search_attr['relation_id'] = 6

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
            self._send_message('Введите начальное значение диапазона\n(целое число от 14 до 80)')
            age_from = self._catch_user_input()
            self._send_message('Введите окончание диапазона\n(целое число от 14 до 80)')
            age_to = self._catch_user_input()

            if age_from <= age_to:
                self.user.search_attr['age_from'] = int(age_from)
                self.user.search_attr['age_to'] = int(age_to)
                break
            else:
                self._send_message('Введный диапазон неверен. Попробуем заново.')

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
        используется метод vk api https://vk.com/dev/database.getCities
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