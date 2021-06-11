from vk_api.longpoll import VkEventType
from vk_api.exceptions import ApiError
from ..bot.auth import BotAuthorization
from ..dispatcher.dispatcher import Dispatcher
from ..utilites.logger import set_logger

logger = set_logger(__name__)

class Bot(BotAuthorization):
    def __init__(self):
        super().__init__()
        self.users = dict()

    def start(self):
        logger.info('Бот стартовал')
        try:
            for event in self.longpoll.listen():

                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    received_message = event.text.lower().strip()

                    if event.user_id not in self.users:
                        self.users[event.user_id] = Dispatcher(self.api, event.user_id, self.upload)

                    if event.type == VkEventType.MESSAGE_NEW:
                        self.users[event.user_id].input(received_message)
        except ApiError as error:
            if error.code == 912:
                error_message = 'Возможности ботов отключены, для их подключения перейдите в настройки бота. ' \
                                'Смотрите README.MD пункт 3 -> 1.4'
                logger.error(error_message)
                print(error_message)
            else:
                logger.error(error)
                print('Что-то пошло не так. Смотри логи')