from .tools import DispatcherTools
from ..user.user import User
from ..assists.commands import Commands
from ..assists.keyboards import Keyboards
from ..assists.messages import Messages
from ..whitelist.whitelist import CurrentWhiteList

""" Класс обеспечивающий диалог бота с пользователем """
""" обрабатываются нажатия на кнопки и сообщения пользователя """

class Dispatcher(DispatcherTools):
    def __init__(self, api, sender_id, upload):
        super().__init__(api, sender_id, upload)

    def input(self, message):
        """ диалог бота с пользователем """
        if message in Commands.all_commands():
            """ обрабатываем команды (нажатие кнопок и текстовый ввод) """
            COMMANDS = {
                Commands.start.check(message): lambda: self._got_command_start(),
                Commands.help.check(message): lambda: self._got_command_help(),
                Commands.search.check(message): lambda: self._got_command_search(),
                Commands.source_user.check(message): lambda: self._got_enter_and_set_source_user(message),
                Commands.targets_sex.check(message): lambda: self._got_enter_and_set_target_sex(message),
                Commands.targets_relation.check(message): lambda: self._got_enter_and_set_target_relation(message),
                Commands.targets_age.check(message): lambda: self._got_enter_and_set_option_target_age(message),
            }
            COMMANDS[message]()

        elif self.user_input:
            """ обрабатываем данные введенные пользователем """
            TAKE_USER_INPUT = {
                'enter_id': lambda: self._got_enter_user_id(message),
                'age_from': lambda: self._got_enter_and_set_target_age_from(message),
                'age_to': lambda: self._got_enter_and_set_target_age_to(message),
                'choice_city': lambda: self._got_enter_and_set_search_option_city(message),
                'enter_city_name': lambda: self._got_enter_and_set_city_name(message),
                'process_targets': lambda: self._got_process_target_answer(message),
                'show_white_list_or_not': lambda: self._got_enter_while_list_show_or_not(message),
                'process_chosen': lambda: self._got_process_chosen_answer(message),
            }
            TAKE_USER_INPUT[self.user_input]()

        else:
            self._got_command_unknown()

    def _got_command_start(self):
        """ получена команда Начать """
        self._send_message(Messages.welcome(self._get_sender_name()), keyboard=Keyboards.main())

    def _got_command_help(self):
        """ получена команда Инфо """
        self._send_message(Messages.info(), keyboard=Keyboards.search())

    def _got_command_unknown(self):
        """ получена неизвестная команда """
        self._send_message(Messages.unknown_command(), keyboard=Keyboards.main())

    def _got_command_search(self):
        """ получена команда Поиск """
        self._send_message(f'{self._get_sender_name()},\nдля кого будем искать пару ?', Keyboards.choose_source_user())

    def _got_enter_and_set_source_user(self, received_message):
        """
        выбираем для кого ищем,
        для текущего пользователя,
        для другого пользователя (будет запрошен id)
        """
        if received_message == 'для меня':
            self.user = User(self.sender_id)
            self._add_user_to_database(self.user)
            self._white_list_exists()

        elif received_message == 'не для меня':
            self.user_input = 'enter_id'
            self._send_message('Введите id:')

    def _got_enter_user_id(self, received_message):
        """ получен id пользователя """
        search_user_id = received_message
        self.user = User(search_user_id)
        # проверяем id на валидность
        check_result, check_result_message = self._check_user_error_or_deactivated()

        if check_result:
            self._add_user_to_database(self.user)
            self._white_list_exists()

        else:
            self._send_message(check_result_message, Keyboards.new_search())

    def _ask_show_white_list_or_not(self):
        """ спрашиваем выводить белый спискок или нет """
        self.user_input = 'show_white_list_or_not'
        self._send_message(
            Messages.ask_show_white_list_or_not(self.user.first_name),
            Keyboards.ask_show_white_list_or_not()
        )

    def _got_enter_while_list_show_or_not(self, received_message):
        if received_message == 'да':
            self._next_chosen()
        elif received_message == 'нет':
            self._ask_search_option_sex()

    def _ask_search_option_sex(self):
        """ запрашиваем пол кандидатов """
        self._send_message('Кого будем искать?', Keyboards.ask_search_option_sex())

    def _got_enter_and_set_target_sex(self, received_message):
        """
        пользователь выбирает кого пола будут кандидаты
        id 1: женский, 2: мужской
        https://vk.com/dev/users.search параметр sex
        """
        if received_message == 'мужчин':
            self.user.search_attr['sex_id'] = 2
        elif received_message == 'женщин':
            self.user.search_attr['sex_id'] = 1

        self._ask_search_option_relation()

    def _ask_search_option_relation(self):
        """ запрашиваем семейное положение кандидатов """
        self._send_message('Статус кандидатов:', Keyboards.ask_search_option_relation())

    def _got_enter_and_set_target_relation(self, received_message):
        """
        пользователь выбирает статус отношений
        id 1: не женат/не замужем 6: в активном поиске
        https://vk.com/dev/users.search realtion
        """
        if received_message == 'не женат/не замужем':
            self.user.search_attr['relation_id'] = 1
        elif received_message == 'в активном поиске':
            self.user.search_attr['relation_id'] = 6

        self._ask_search_option_age()

    def _ask_search_option_age(self):
        """
        если возраст известен запрашивает вариант поиска по возрасту (ровестники или диапазон),
        иначе сразу переходит к запросу возрастного диапазона
        """
        if self.user.age:
            self._send_message(Messages.ask_search_option_with_age(), Keyboards.ask_search_option_with_age())
        else:
            self._ask_search_option_age_from()

    def _got_enter_and_set_option_target_age(self, received_message):
        """ получаем вариант поиска по возрасту (ровестники или диапазон) """
        if received_message == 'диапазон':
            self._ask_search_option_age_from()

        elif received_message == 'ровестники':
            self.user.search_attr['age_from'] = self.user.age - 2
            self.user.search_attr['age_to'] = self.user.age + 2
            self._ask_search_option_city()

    def _ask_search_option_age_from(self):
        """ запрашиваем начало возрастного диапазона """
        self.user_input = 'age_from'
        self._send_message(Messages.ask_search_option_age_from())

    def _got_enter_and_set_target_age_from(self, received_message):
        """ получаем, проверяем и устнавливаем начало возрастного диапазона """
        try:
            self.user.search_attr['age_from'] = int(received_message)
            self.user_input = 'age_to'
            self._send_message(Messages.ask_search_option_age_to())
        except ValueError:
            self._send_message(Messages.entered_age_is_not_valid())
            self._ask_search_option_age_from()

    def _ask_search_option_age_to(self):
        """ запрашиваем конец возрастного диапазона """
        self._send_message(Messages.ask_search_option_age_to())

    def _got_enter_and_set_target_age_to(self, received_message):
        """ получаем, проверяем и устнавливаем конец возрастного диапазона """
        try:
            self.user.search_attr['age_to'] = int(received_message)
            self._ask_search_option_city()
        except ValueError:
            self._send_message(Messages.entered_age_is_not_valid())
            self._ask_search_option_age_to()

    def _ask_search_option_city(self):
        """ запрашиваем вариант поиска по городу """
        self.user_input = 'choice_city'
        if self.user.city_name:
            self._send_message('В каком городе будем искать?\n', Keyboards.ask_search_option_city(self.user.city_name))
        else:
            self._ask_city_name_and_search()

    def _got_enter_and_set_search_option_city(self, received_message):
        """ получаем вариант поиска по городу """
        if self.user.city_name:
            if received_message == self.user.city_name.lower():
                self.user.search_attr['city_id'] = self.user.city_id
                # начинаем выводит найденные кандидатуры
                self._process_targets()
            else:
                self._ask_city_name_and_search()
        else:
            self._ask_city_name_and_search()

    def _ask_city_name_and_search(self):
        """ запрашиваем название города """
        self.user_input = 'enter_city_name'
        self._send_message('Введите название города')

    def _got_enter_and_set_city_name(self, city_name):
        """ получаем, проверяем и устанавлиеваем название города """
        result = self.user.api.database.getCities(q=city_name, country_id=1)
        if result.get('items'):
            self.user.search_attr['city_id'] = result.get('items')[0].get('id')
            self.user.city_id = result.get('items')[0].get('id')
            self.user.city_name = result.get('items')[0].get('title')
            # начинаем выводит найденные кандидатуры
            self._process_targets()
        else:
            self._send_message(f"'{city_name}' не обнаружен. Попробуем заново.")
            self._ask_city_name_and_search()

    def _got_process_target_answer(self, answer):
        """ обрабатываем ответы пользователя при просмотре кандидатур """
        self.user_input = 'process_targets'
        ANSWERS = {
            'да': lambda: self._add_target_to_whitelist(self.user.id),
            'нет': lambda: self._add_target_to_blacklist(self.user.id),
            'не знаю': lambda: self._next_target(),
            'прервать поиск': lambda: self._send_message('Поиск прерван', Keyboards.new_search()),
        }
        ANSWERS[answer]()

    def _got_process_chosen_answer(self, answer):
        """ обрабатываем ответы пользователя при просмотре избранных кандидатур """
        self.user_input = 'process_chosen'
        ANSWERS = {
            'следующий': lambda: self._next_chosen(),
            'убрать из избранного': lambda: self._remove_target_from_white_list(),
            'прервать просмотр': lambda: self._send_message('Продолжить поиск?', Keyboards.continue_search()),
            'да': lambda: self._ask_search_option_sex(),
            'нет': lambda: self._send_message('До свидания. Приходите еще.')
        }
        ANSWERS[answer]()

    def _white_list_exists(self):
        """ проверяем у пользователя наличие белого списка, если есть, то спрашиваем выводить или нет"""
        self.white_list = CurrentWhiteList(self.user.id)

        if self.white_list.items:
            self._ask_show_white_list_or_not()
        else:
            self._ask_search_option_sex()
