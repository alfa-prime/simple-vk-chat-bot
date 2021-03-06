import re
from datetime import datetime

from .auth import UserAuthorization
from .properties import UserProperties
from ..utilites.logger import set_logger

logger = set_logger(__name__)

class User(UserAuthorization, UserProperties):
    """  получает, обрабатывает и проставляет свойства пользователя """
    def __init__(self, input_id):
        super().__init__()
        self._process_properties(input_id)

        if self.has_error and 'no access_token' in self.has_error:
            error_message = 'Авторизация пользователя не удалась. Нет токена. Смотрите README.MD пункт 4 -> 2.1'
            print(error_message)
            logger.error(error_message)
            exit()

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.id!r}, {self.first_name!r}, {self.last_name!r}, {self.city_name!r}, {self.age!r}, '
                f'has_error: {self.has_error!r}, is_deactivated: {self.is_deactivated!r}, '
                f'search_attr: {self.search_attr!r})')

    def _process_properties(self, input_id):
        """ обработка полученных свойств """
        raw = self._get_raw_properties(input_id)

        if 'error_msg' in raw:
            self.has_error = raw.get('error_msg')
        elif 'deactivated' in raw:
            self.is_deactivated = 'Аккуант удалён' if raw.get('deactivated') == 'deleted' else 'Аккаунт заблокирован'
        else:
            self._set_properties(raw)

    def _get_raw_properties(self, input_id):
        """  получение свойств пользователя, метод vk api https://vk.com/dev/users.get """
        # список дополнительных полей для выдачи
        FIELDS_TO_SEARCH = 'sex, bdate, city, country'
        try:
            return self.api.users.get(user_ids=input_id, fields=FIELDS_TO_SEARCH, v=self.api_version)[0]
        except self.api_error as error:
            return dict(error.error)

    def _set_properties(self, raw_properties):
        """ устанавливает свойства пользователя """
        self.id = raw_properties.get('id')
        self.first_name = raw_properties.get('first_name')
        self.last_name = raw_properties.get('last_name')

        city = raw_properties.get('city')
        if city:
            self.city_id = city.get('id')
            self.city_name = city.get('title')

        self.search_attr.city_id = self.city_id

        birthday = raw_properties.get('bdate')
        if birthday:
            try:
                birth_year = re.search(r'\d{4}', birthday)[0]
                current_year = datetime.now().year
                self.age = current_year - int(birth_year)
            except TypeError:
                logger.error('Год рождения не найден. Возраст неизвестен.')
