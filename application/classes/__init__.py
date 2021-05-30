from dataclasses import dataclass
import vk_api
from vk_api.longpoll import VkLongPoll
from application.settings import BOT_TOKEN, APP_ID, USER_TOKEN, API_VERSION

class BotAuthorization:
    def __init__(self):
        session = vk_api.VkApi(token=BOT_TOKEN)
        self.api = session.get_api()
        self.longpoll = VkLongPoll(session)

class UserAuthorization:
    def __init__(self):
        session = vk_api.VkApi(app_id=APP_ID, token=USER_TOKEN)
        self.api = session.get_api()
        self.api_error = vk_api.VkApiError
        self.api_version = API_VERSION


@dataclass
class UserProperties:
    """ хранит сведения о свойствах пользователя """
    first_name: str = None
    last_name: str = None
    sex_id: int = None
    sex_by_text: str = None
    city_id: int = None
    city_name: str = None
    age: int = None

    has_error: str = None
    is_deactivated: str = None
    search_attr: dict = None
