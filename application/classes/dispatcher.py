from application.classes.keyboards import Keyboards
from application.classes.messages import Messages
from .hunter import Hunter
from .user import User

from ..classes.dispathcer_tools import DispatcherTools
from ..classes.commands import Commands


from ..utilites.logger import set_logger
logger = set_logger(__name__)

class Dispatcher(DispatcherTools):
    def __init__(self, api, longpoll, upload):
        super().__init__()
        self.api = api
        self.longpoll = longpoll
        self.upload = upload
        self.sender_id = None
        self.sender_name = None

    def process_message(self, received_message, sender_id):
        """ обрабатывает входящие сообщения пользователя, формирует ответ бота """
        self.sender_id = sender_id
        self.sender_name = self._get_sender_name()
        logger.info(f"{self.sender_name}: {received_message}")
        self._process_command(received_message)

    def _received_begin(self):
        """ получена команда Начать """
        self._send_message(Messages.welcome(self.sender_name), Keyboards.main())

    def _received_info(self):
        """ получена команда Инфо """
        self._send_message(Messages.info(), Keyboards.search())

    def _received_search(self):
        """ получена комадна Поиск """
        self._select_for_whom_search()

        # проверяем id на валидность
        check_result, check_result_message = self._check_user_error_or_deactivated()

        if check_result:
            self._send_message(Messages.user_info(self.user))
            self._set_search_option_by_sex()
            self._set_search_option_by_relation()
            self._set_search_option_by_age()
            self._set_search_option_by_city()
            self._send_message(Messages.search_start())
            hunter = Hunter(self.user)
            self._send_message(f'Найдено: {hunter.targets_count + 1}')
            self._process_search_dialog(hunter)
        else:
            self._send_message(check_result_message, Keyboards.new_search())

    def _process_command(self, received_message):
        """
        обрабатывает входящие от пользователя команды
        """
        if received_message in Commands.start.value: received_message = 'старт'
        if received_message in Commands.help.value: received_message = 'помощь'
        if received_message in Commands.search.value: received_message = 'поиск'

        COMMANDS_MAPPER = {
            'старт': self._received_begin,
            'помощь': self._received_info,
            'поиск': self._received_search
        }

        if received_message in COMMANDS_MAPPER:
            COMMANDS_MAPPER.get(received_message)()
        else:
            self._send_message(Messages.unknown_command(), Keyboards.main())

    def _process_search_dialog(self, hunter):
        """
        поисковый диалог с пользователем, с анализом ответов
        """
        for index, (target_id, target_attr) in enumerate(hunter.targets.items()):

            attachments = self._process_profile_photos(target_id)
            self._send_message(f'{index + 1} из {hunter.targets_count + 1}', attachments=attachments)
            self._send_message(Messages.target_info(target_attr), Keyboards.process_target())
            answer = self._catch_user_input()

            if index != len(hunter.targets) - 1:

                if answer == 'да':
                    ...
                elif answer == 'нет':
                    ...
                elif answer == 'может быть':
                    ...
                elif answer == 'прервать поиск':
                    self._send_message('Поиск прерван', Keyboards.new_search())
                    break

            else:
                self._send_message('Больше кандидатур нет', Keyboards.new_search())

    def _select_for_whom_search(self):
        """
        выбираем для кого искать пару, для текущего пользователя или для другого (вводится id)
        """
        self._send_message(Messages.choose_whom_search(self.sender_name), Keyboards.choose_whom_search())

        user_choice = self._catch_user_input()

        if user_choice == 'для меня':
            self.user = User(self.sender_id)

        elif user_choice == 'не для меня':
            self._send_message(message='Введите id:')
            search_user_id = self._catch_user_input()
            self.user = User(search_user_id)