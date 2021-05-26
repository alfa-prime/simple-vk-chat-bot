import vk_api

from application.settings import BOT_TOKEN

class BotAuht:
    def __init__(self):
        session = vk_api.VkApi(token=BOT_TOKEN)
        self.api = session.get_api()

class Bot(BotAuht):
    def __init__(self):
        super().__init__()
