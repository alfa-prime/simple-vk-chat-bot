class Messages:
    @staticmethod
    def welcome(sender_name):
        return f'Здравствуйте, {sender_name}\n' \
                       f'Подробности по команде "Инфо"\n' \
                       f'Для поиска пары, команда "Поиск"\n'

    @staticmethod
    def info():
        return f'По команде "Поиск" ' \
                       f'бот запрашивает id пользователя ВК\n\n' \
                       f'После проверки id на валидность, ' \
                       f'бот пытается собрать необходимые для поиска данные, ' \
                       f'если какие-то не найдены, то просит у пользователя ввести их. ' \
                       f'Затем он ищет подходящие кандидатуры\n\n' \
                       f'Критерии совпадения:\n\n' \
                       f'семейное положение: в активном поиске или неженатые;\n\n' \
                       f'пол: пользователь сам выбрает пол кандидатов ;\n\n' \
                       f'возраст: если возраст известен, предлагается выбор:\n' \
                       f'1. родвестники (возраст пользователя +/- 2 года)\n' \
                       f'2. задается возрастной диапазон\n' \
                       f'в противном случае, только возрастной диапазон.\n\n' \
                       f'город: если город указан, то предлагается выбор:\n' \
                       f'1. искать в родном городе\n' \
                       f'2. указать другой город\n' \
                       f'в противном случае, поиск в родном городе не доступен'

    @staticmethod
    def choose_source_user(name):
        return f'{name},\nдля кого будем искать пару ?'

    @staticmethod
    def ask_search_option_sex():
        return f'Кого будем искать?'

    @staticmethod
    def ask_search_option_relation():
        return f'Статус кандидатов:'

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
        return 'Введите начало диапазона\n(целое число от 14 до 80)'

    @staticmethod
    def ask_search_option_age_to():
        return 'Введите конец диапазона\n(целое число от 14 до 80)'

    @staticmethod
    def entered_age_is_not_valid():
        return 'Введное значение неверно\nПопробуйте снова'

    @staticmethod
    def ask_search_option_city():
        return f'В каком городе будем искать?\n'

    @staticmethod
    def target_info(birthday, name, link):
        # если дата рождения не указана, так и пишем
        bday = birthday if birthday else 'нет данных'
        return f'Имя: {name}\n' \
               f'Дата рождения: {bday}\n' \
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
