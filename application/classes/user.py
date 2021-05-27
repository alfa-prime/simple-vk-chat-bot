from dataclasses import dataclass
import re
from datetime import datetime
import vk_api

from ..utilites.logger import set_logger
from ..settings import USER_TOKEN, APP_ID, API_VERSION

# список дополнительных полей для выдачи при запросе расширенной информации о пользователях (users.get)
FIELDS_TO_SEARCH = 'sex, bdate, city, relation'

logger = set_logger(__name__)

class UserAuth:
    def __init__(self):
        session = vk_api.VkApi(app_id=APP_ID, token=USER_TOKEN)
        self.api = session.get_api()

@dataclass
class UserProperties:
    """ хранит сведения о свойствах пользователя """
    first_name: str = None
    last_name: str = None
    sex_id: int = None
    city_id: int = None
    city_name: str = None
    age: int = None

    has_error: str = None
    is_deactivated: str = None

class User(UserAuth, UserProperties):
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
        """  получение 'сырых' свойств пользователя """
        try:
            return self.api.users.get(user_ids=input_id, fields=FIELDS_TO_SEARCH, v=API_VERSION)[0]
        except vk_api.ApiError as error:
            return dict(error.error)

    def _set_properties(self, properties):
        """ устанавливает свойства для текущего пользователя """
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
            except TypeError as error:
                logger.error(error)