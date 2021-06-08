import vk_api
from application.settings import APP_ID, USER_TOKEN, API_VERSION

class UserAuthorization:
    def __init__(self):
        session = vk_api.VkApi(app_id=APP_ID, token=USER_TOKEN)
        self.api = session.get_api()
        self.api_error = vk_api.VkApiError
        self.api_version = API_VERSION
