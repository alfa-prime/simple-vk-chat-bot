class Messages:
    @staticmethod
    def welcome(sender_name):
        return f'Здравствуйте, {sender_name}\n' \
                       f'Подробности по команде "Инфо"\n' \
                       f'Для поиска пары, команда "Поиск"\n'

    @staticmethod
    def info():
        return f'' \
               f'По команде "Поиск" бот запрашивает для кого искать пару:\n\n' \
               f'для текущего пользователя (смотри пункт 2);\n\n' \
               f'для другого пользователя бот запрашивает id пользователя, проверяет его валидность, ' \
               f'в случае если id не валиден предлагается осуществить новый поиск, ' \
               f'иначе (смотри пункт 2);\n\n' \
               f'2. Бот запрашивает пол кандитатов, пользователь сам выбрает (мужской, женский);\n\n' \
               f'3. Бот запрашивает семейное положение кандидатов, пользователь сам выбирает ' \
               f'(в активном поиске или неженатые);\n\n' \
               f'4. Если возраст пользователя известен, предлагается выбор:\n' \
               f'- ровестники (возраст пользователя +/- 2 года);\n' \
               f'- возрастной диапазон;\n\n' \
               f'в противном случае, только возрастной диапазон.\n\n' \
               f'6. Если город пользователя известен, предлагается выбор:\n' \
               f'- искать в родном городе\n' \
               f'- указать другой город\n\n' \
               f'в противном случае, пользователь сам указывает город\n'

    @staticmethod
    def ask_search_option_with_age():
        return f'Какой вариант поиска будем использовать?\n' \
               f'Ровестники: возраст +/- 2 года;\n' \
               f'Диапазон: желаемый диапазон возрастов\nНапример от 20 до 25'

    @staticmethod
    def ask_search_option_without_age():
        return f'Задайте желаемый возрастной диапазон\nНапример от 20 до 25'

    @staticmethod
    def ask_search_option_age_from():
        return 'Введите начало возрастного диапазона\n(целое число от 14 до 80)'

    @staticmethod
    def ask_search_option_age_to():
        return 'Введите конец возрастного диапазона\n(целое число от 14 до 80)'

    @staticmethod
    def entered_age_is_not_valid():
        return 'Введное значение неверно\nПопробуйте снова'

    @staticmethod
    def target_info(name, link, bdate):
        return f'Имя: {name}\n' \
               f'Дата рождения: {bdate}\n' \
               f'Подробности: {link}'

    @staticmethod
    def search_start():
        return f'Начинаем поиск\n' \
               f'Пожалуйста, подождите немного\n' \
               f'Идет сбор и обработка сведений\n'

    @staticmethod
    def unknown_command():
        return f'Неизвестная комадна\n' \
               f'"Инфо" подробности\n' \
               f'"Поиск" поиск пары\n'
