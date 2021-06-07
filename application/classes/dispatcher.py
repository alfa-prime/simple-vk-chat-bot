from application.classes import DispatcherRoot
from application.classes.commands import Commands
from application.classes.user import User
from application.classes.keyboards import Keyboards
from application.classes.messages import Messages

class Dispatcher(DispatcherRoot):
    def __init__(self, api, sender_id, upload):
        super().__init__(api, sender_id, upload)

    def input(self, message):
        if message in Commands.all_commands():
            COMMANDS = {
                Commands.start.check(message): lambda: self._got_command_start(),
                Commands.help.check(message): lambda: self._got_command_help(),
                Commands.search.check(message): lambda: self._got_command_search(),
                Commands.source_user.check(message): lambda: self._got_enter_and_set_source_user(message),
                Commands.targets_sex.check(message): lambda: self._got_enter_and_set_target_sex(message),
                Commands.targets_relation.check(message): lambda: self._got_enter_and_set_target_relation(message),
                Commands.targets_age.check(message): lambda: self._got_enter_and_set_target_age(message)
            }
            COMMANDS[message]()

        elif self.user_input:
            TAKE_USER_INPUT = {
                'enter_id': lambda: self._got_enter_user_id(message),
                'age_from': lambda: self._got_enter_and_set_target_age_from(message),
                'age_to': lambda: self._got_enter_and_set_target_age_to(message),
                'choice_city': lambda: self._got_enter_and_set_search_option_city(message),
                'enter_city_name': lambda: self._got_enter_and_set_city_name(message),
                'process_targets': lambda: self._got_process_target_answer(message)

            }
            TAKE_USER_INPUT[self.user_input]()

        else:
            self._got_command_unknown()

    def _got_command_start(self):
        """ получена команда Начать """
        self._send_message(Messages.welcome(self.sender_name), keyboard=Keyboards.main())

    def _got_command_help(self):
        """ получена команда Инфо """
        self._send_message(Messages.info(), keyboard=Keyboards.search())

    def _got_command_unknown(self):
        """ получена неизвестная команда """
        self._send_message(Messages.unknown_command(), keyboard=Keyboards.main())

    def _got_command_search(self):
        """ получена команда Поиск """
        self._send_message(f'{self.sender_name},\nдля кого будем искать пару ?', Keyboards.choose_source_user())

    def _got_enter_and_set_source_user(self, received_message):
        """
        выбираем для кого ищем,
        для текущего пользователя,
        для другого пользователя (будет запрошен id)
        """
        if received_message == 'для меня':
            self.user = User(self.sender_id)
            self._ask_search_option_sex()
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
            self._ask_search_option_sex()
        else:
            self._send_message(check_result_message, Keyboards.new_search())

    def _ask_search_option_sex(self):
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
        self._send_message('Статус кандидатов:', Keyboards.ask_search_option_relation())

    def _got_enter_and_set_target_relation(self, received_message):
        """
        пользователь выбирает статус отношений
        id 1: не женат/не замужем 6: в активном поиске
        https://vk.com/dev/users.search параметр sex
        """
        if received_message == 'не женат/не замужем':
            self.user.search_attr['relation_id'] = 1
        elif received_message == 'в активном поиске':
            self.user.search_attr['relation_id'] = 6

        self._ask_search_option_age()

    def _ask_search_option_age(self):
        if self.user.age:
            self._send_message(Messages.ask_search_option_with_age(), Keyboards.ask_search_option_with_age())
        else:
            self._send_message(Messages.ask_search_option_without_age(), Keyboards.ask_search_option_without_age())

    def _got_enter_and_set_target_age(self, received_message):
        if received_message == 'диапазон':
            self._ask_search_option_age_from()

        elif received_message == 'ровестники':
            age_from = self.user.age - 2
            age_to = self.user.age + 2
            self.user.search_attr['age_from'] = age_from
            self.user.search_attr['age_to'] = age_to
            self._ask_search_option_city()

    def _ask_search_option_age_from(self):
        self.user_input = 'age_from'
        self._send_message(Messages.ask_search_option_age_from())

    def _got_enter_and_set_target_age_from(self, received_message):
        try:
            self.user.search_attr['age_from'] = int(received_message)
            self.user_input = 'age_to'
            self._send_message(Messages.ask_search_option_age_to())
        except ValueError:
            self._send_message(Messages.entered_age_is_not_valid())
            self._ask_search_option_age_from()

    def _ask_search_option_age_to(self):
        self._send_message(Messages.ask_search_option_age_to())

    def _got_enter_and_set_target_age_to(self, received_message):
        try:
            self.user.search_attr['age_to'] = int(received_message)
            self.user_input = None
            self._ask_search_option_city()
        except ValueError:
            self._send_message(Messages.entered_age_is_not_valid())
            self._ask_search_option_age_to()

    def _ask_search_option_city(self):
        self.user_input = 'choice_city'
        if self.user.city_name:
            self._send_message('В каком городе будем искать?\n', Keyboards.ask_search_option_city(self.user.city_name))
        else:
            self._ask_city_name_and_search()

    def _got_enter_and_set_search_option_city(self, received_message):
        if self.user.city_name:
            if received_message == self.user.city_name.lower():
                self.user.search_attr['city_id'] = self.user.city_id
                self._process_targets()
            else:
                self._ask_city_name_and_search()
        else:
            self._ask_city_name_and_search()

    def _ask_city_name_and_search(self):
        self.user_input = 'enter_city_name'
        self._send_message('Введите название города')

    def _got_enter_and_set_city_name(self, city_name):
        result = self.user.api.database.getCities(q=city_name, country_id=1)
        if result.get('items'):
            self.user.search_attr['city_id'] = result.get('items')[0].get('id')
            self.user.city_id = result.get('items')[0].get('id')
            self.user.city_name = result.get('items')[0].get('title')
            self._process_targets()
        else:
            self._send_message(f"'{city_name}' не обнаружен. Попробуем заново.")
            self._ask_city_name_and_search()

    def _got_process_target_answer(self, answer):
        if answer == 'да':
            self._next_target()
        elif answer == 'нет':
            self._next_target()
        elif answer == 'не знаю':
            self._next_target()
        elif answer == 'прервать поиск':
            self._send_message('Поиск прерван', Keyboards.new_search())
