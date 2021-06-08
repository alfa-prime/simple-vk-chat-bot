import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll
from application.settings import BOT_TOKEN

class BotAuthorization:
    def __init__(self):
        session = vk_api.VkApi(token=BOT_TOKEN)
        self.api = session.get_api()
        self.longpoll = VkLongPoll(session)
        self.upload = VkUpload(session)
