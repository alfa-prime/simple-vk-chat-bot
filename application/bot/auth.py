import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll
from vk_api.exceptions import ApiError
from application.settings import BOT_TOKEN

from ..utilites.logger import set_logger

logger = set_logger(__name__)


class BotAuthorization:
    def __init__(self):
        try:
            session = vk_api.VkApi(token=BOT_TOKEN)
            self.api = session.get_api()
            self.longpoll = VkLongPoll(session)
            self.upload = VkUpload(session)
        except ApiError as error:
            if error.code == 5:
                error_message = 'Авторизация бота не удалась. Нет токена. Смотрите README.MD пункт 1.1'
                logger.error(error_message)
                print(error_message)
            else:
                logger.error(error)
                print('Что-то пошло не так. Смотри логи')
            exit()



