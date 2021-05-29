import re
from datetime import datetime

from ..classes import UserAuthorization, UserProperties
from ..utilites.logger import set_logger

# список дополнительных полей для выдачи при запросе расширенной информации о пользователях (users.get)
# подробности https://vk.com/dev/users.get параметр fields
FIELDS_TO_SEARCH = 'sex, bdate, city'

logger = set_logger(__name__)

class User(UserAuthorization, UserProperties):
    """  получает, обрабатывает и проставляет свойства пользователя """
    def __init__(self, input_id):
        super().__init__()
        self._process_properties(input_id)

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
        """  получение свойств пользователя """
        try:
            return self.api.users.get(user_ids=input_id, fields=FIELDS_TO_SEARCH, v=self.api_version)[0]
        except self.api_error as error:
            return dict(error.error)

    def _set_properties(self, properties):
        """ устанавливает свойства пользователя """
        self.first_name = properties.get('first_name')
        self.last_name = properties.get('last_name')
        self.sex_id = properties.get('sex')

        city = properties.get('city')
        if city:
            self.city_id = city.get('id')
            self.city_name = city.get('title')

        birthday = properties.get('bdate')
        if birthday:
            try:
                birth_year = re.search(r'\d{4}', birthday)[0]
                current_year = datetime.now().year
                self.age = current_year - int(birth_year)
            except TypeError:
                logger.error('Год рождения не найден. Возраст неизвестен.')

        self.search_attr = dict(
            # msg_if_val_none будет выводится, когда бот будет запрашивать недостающие сведения
            sex_id=dict(value=self._swap_sex_id(), msg_if_val_none='Пол не определен кого будем искать?'),
            city_id=dict(value=self.city_id, msg_if_val_none='ID города неизвестен'),
            city_name=dict(value=self.city_name, msg_if_val_none='Город не определен'),
            age=dict(value=self.age, msg_if_val_none='Возраст неизвестен. Задайте возрастной диапазон от и до'),
            age_from=dict(value=''),
            age_to=dict(value='')
        )

    def _swap_sex_id(self):
        """
        для параметров поиска замена sex_id на противоположный
        значения id https://vk.com/dev/users.search параметр sex_id
        1: женщина, 2: мужчина, 0: любой
        """
        swap = {1: 2, 2: 1, 0: None}
        return swap.get(self.sex_id)
