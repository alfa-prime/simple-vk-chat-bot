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
