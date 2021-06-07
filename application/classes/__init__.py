from dataclasses import dataclass

import requests
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll
from vk_api.utils import get_random_id

from application.classes.hunter import Hunter
from application.classes.keyboards import Keyboards
from application.classes.messages import Messages
from application.settings import BOT_TOKEN, APP_ID, USER_TOKEN, API_VERSION
from application.utilites.helpers import make_dir, remove_dir


class BotAuthorization:
    def __init__(self):
        session = vk_api.VkApi(token=BOT_TOKEN)
        self.api = session.get_api()
        self.longpoll = VkLongPoll(session)
        self.upload = VkUpload(session)

class UserAuthorization:
    def __init__(self):
        session = vk_api.VkApi(app_id=APP_ID, token=USER_TOKEN)
        self.api = session.get_api()
        self.api_error = vk_api.VkApiError
        self.api_version = API_VERSION

@dataclass
class UserProperties:
    """ хранит сведения о свойствах пользователя """
    id: int = None
    first_name: str = None
    last_name: str = None
    sex: str = None
    city_id: int = None
    city_name: str = None
    age: int = None

    has_error: str = None
    is_deactivated: str = None
    search_attr: dict = None

class DispatcherRoot:
    def __init__(self, api, sender_id, upload):
        self.api = api
        self.sender_id = sender_id
        self.sender_name = self._get_sender_name()
        self.upload = upload

        self.user = None
        self.user_input = None
        self.targets = None
        self.targets_count = None

    def _send_message(self, message=None, keyboard=None, attachments=None):
        """ посылает сообщение пользователю """
        self.api.messages.send(peer_id=self.sender_id,
                               message=message,
                               keyboard=keyboard,
                               attachment=attachments,
                               random_id=get_random_id())

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

    def _process_targets(self):
        self._send_message(Messages.search_start())
        hunter_one = Hunter(self.user)
        self._send_message(f'Найдено: {hunter_one.targets_count}')
        self.targets = hunter_one.targets
        self.targets_count = hunter_one.targets_count
        self._next_target()

    def _next_target(self):
        self.user_input = 'process_targets'
        try:
            target = next(self.targets)
            index, target_id, name, link, bdate = target.split(',')
            attachments = self._process_profile_photos(int(target_id))

            self._send_message(f'{index} из {self.targets_count}', attachments=attachments)
            self._send_message(Messages.target_info(name, link, bdate), Keyboards.process_target())
        except StopIteration:
            self._send_message('Больше кандидатур нет', Keyboards.new_search())

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
