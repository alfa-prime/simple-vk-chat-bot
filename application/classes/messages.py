class Messages:
    @staticmethod
    def welcome(sender_name):
        message_body = f'Здравствуйте, {sender_name}\n' \
                       f'Подробности по команде "Инфо"\n' \
                       f'Для поиска пары, команда "Поиск"\n'
        return message_body

    @staticmethod
    def info():
        message_body = f'По команде "Поиск" ' \
                       f'бот запрашивает id пользователя ВК\n\n' \
                       f'После проверки id на валидность, ' \
                       f'бот пытается собрать необходимые для поиска данные, ' \
                       f'если какие-то не найдены, то просит у пользователя ввести их. ' \
                       f'Затем он ищет подходящие кандидатуры.\n\n' \
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
                       f'в противном случае, поиск в родном городе не доступен.'

        return message_body

    @staticmethod
    def user_info(user):
        full_name = f"{user.first_name} {user.last_name}"
        # city = user.city_name if user.city_name else 'Нет данных'

        message_body = f'Найденые данные:\n' \
                       f'Имя: {full_name}\n' \
                       # f'Город: {city}'

        return message_body

    @staticmethod
    def choose_search_option_by_age(age):
        message_body = f'Возраст: {age}.\nКакой вариант поиска будем использовать?\n' \
                       f'"Ровестники":\nвозраст +/- 2 года;\n' \
                       f'"Диапазон":\nзадать желаемый возрастной диапазон.\nНапример от 20 до 25.'
        return message_body

    @staticmethod
    def choose_search_option_by_sex(sex):
        message_body = f'Пол: {sex}.\n' \
                       f'Кого будем искать?'
        return message_body

    @staticmethod
    def choose_search_option_by_city(city_name):
        message_body = f'Город: {city_name}.\nВ каком городе будем искать?\n'
        return message_body

    @staticmethod
    def missing_age():
        message_body = f'Возраст: Нет данных.\n' \
                       f'Поиск ровестников невозможен.\n' \
                       f'Задайте желаемый возрастной диапазон.\n' \
                       f'Например от 25 до 35.'
        return message_body

    @staticmethod
    def target_info(target):
        message_body = f'{target.get("name")}\n' \
                       f'{target.get("link")}'
        return message_body

    @staticmethod
    def unknown_command():
        message_body = f'Неизвестная комадна.\n' \
                      f'"Инфо" подробности\n' \
                      f'"Поиск" поиск пары\n'
        return message_body


