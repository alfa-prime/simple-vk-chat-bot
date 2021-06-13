import requests
from vk_api.utils import get_random_id
from .setup import DispatcherSetup
from ..database.database import Users, BlackList, WhiteList
from ..hunter.hunter import Hunter
from ..assists.keyboards import Keyboards
from ..assists.messages import Messages
from ..utilites.helpers import make_dir, remove_dir


""" Класс утилит для диспетчера обработки сообщений """

class DispatcherTools(DispatcherSetup):
    def __init__(self, api, sender_id, upload):
        super().__init__(api, sender_id, upload)

    def _send_message(self, message=None, keyboard=None, attachments=None):
        """ посылает сообщение пользователю """
        self.api.messages.send(
            peer_id=self.sender_id,
            message=message,
            keyboard=keyboard,
            attachment=attachments,
            random_id=get_random_id()
        )

    def _get_sender_name(self):
        """
        получает имя пользователя по его id
        метод vk api https://vk.com/dev/users.get
        """

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
        """ выводит результат поиска """
        self._send_message(Messages.search_start())
        self.targets = Hunter(self.user)
        self._send_message(f'Найдено: {self.targets.total}')
        self._next_target()

    def _next_target(self):
        """ выводит сведения о следующей кандидатуре """
        self.user_input = 'process_targets'
        try:
            target = next(self.targets)
            attachments = self._process_profile_photos(target.target_id)

            # свойства для добавления кандидатуры в белый или черный список
            # методы _add_target_to_blacklist и _add_target_to_whitelist
            self.target_id = target.target_id
            self.target_name = target.name
            self.target_link = target.link
            self.target_bdate = target.bdate

            self._send_message(f'{target.index} из {target.total}', attachments=attachments)
            self._send_message(
                Messages.target_info(target.name, target.bdate),
                Keyboards.process_target(target.link)
            )

        except StopIteration:
            self._send_message('Больше кандидатур нет', Keyboards.new_search())

    def _next_chosen(self):
        """ выводит сведения о следущем избраном кандидате """
        self.user_input = 'process_chosen'
        try:
            chosen = next(self.white_list)
            attachments = self._process_profile_photos(chosen.target_id)

            # target_id используется для удаления записи из белого списка
            # метод _remove_target_from_white_list
            self.target_id = chosen.target_id

            self._send_message(f'{chosen.index} из {chosen.total}', attachments=attachments)
            self._send_message(Messages.target_info(chosen.name, chosen.bdate), Keyboards.process_chosen(chosen.link))
        except StopIteration:
            self._send_message('Больше избранных кандидатур нет.\n Искать новых?', Keyboards.ask_yes_or_no())

    def _add_user_to_database(self, user):
        """ добавляем пользователя в бд """
        check_user_exist = self.db_session.query(Users).filter_by(vk_user_id=user.id).all()
        if not check_user_exist:
            name = f'{self.user.first_name} {self.user.last_name}'
            link = f'vk.com/id{self.user.id}'
            self.db_session.add(Users(vk_user_id=user.id, name=name, link=link))
            self.db_session.commit()

    def _add_target_to_blacklist(self, user_id):
        """ добавляем кандидатуру в черный список (не будет выводится при следующем поиске) """
        self.db_session.add(BlackList(user_id=user_id, target_id=self.target_id))
        self.db_session.commit()
        self._next_target()

    def _add_target_to_whitelist(self, user_id):
        """ добавляем кандидатуру в белый список (не будет выводится при следующем поиске) """
        self.db_session.add(
            WhiteList(
                user_id=user_id,
                id=self.target_id,
                name=self.target_name,
                link=self.target_link,
                bdate=self.target_bdate
            )
        )

        self.db_session.commit()
        self._next_target()

    def _remove_target_from_white_list(self):
        """ удаляем кандидатуру из списка избранных """
        self.db_session.delete(self.db_session.query(WhiteList).filter_by(id=self.target_id).one())
        self.db_session.commit()
        self._next_chosen()

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
