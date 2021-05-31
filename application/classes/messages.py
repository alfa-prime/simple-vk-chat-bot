class Messages:
    @staticmethod
    def welcome(sender_name):
        message_body = f'Здравствуйте, {sender_name}\n' \
                       f'Для поиска пары, используйте команду "Поиск"\n' \
                       f'Подробности по команде "Инфо"\n'
        return message_body

    @staticmethod
    def info():
        message_body = f'По команде "Поиск"' \
                       f'бот запрашивает id пользователя ВК\n\n' \
                       f'После проверки id на валидность, ' \
                       f'бот пытается собрать необходимые для поиска данные, ' \
                       f'если какие-то не найдены, то просит у пользователя ввести их.\n\n' \
                       f'Затем он ищет подходящие кандидатуры\n\n' \
                       f'Критерии совпадения:\n' \
                       f'город: совпадает с городом пользователя;\n' \
                       f'пол: пользователю предоставляется возможность самому выбрать пол кандидатов ;\n' \
                       f'семейное положение: в активном поиске или неженатые;\n' \
                       f'возраст: ровестники (возраст пользователя +/- 2 года) или задается диапазон'
        return message_body

    @staticmethod
    def user_info(user):
        full_name = f"{user.first_name} {user.last_name}"
        sex = user.sex_by_text
        age = user.age if user.age else 'Нет данных'
        city = user.city_name if user.city_name else 'Нет данных'

        message_body = f'Найденые данные:\n' \
                       f'Имя: {full_name}\n' \
                       f'Пол: {sex}\n' \
                       f'Возраст: {age}\n' \
                       f'Город: {city}'

        return message_body

    @staticmethod
    def choose_search_option_by_age(age):
        message_body = f'Возраст: {age}.\nКакой вариант поиска будем использовать?\n' \
                       f'"Ровестники":\nвозраст +/- 2 года;\n' \
                       f'"Диапазон":\nзадать возрастной диапазон.\nНапример от 20 до 25.'
        return message_body

    @staticmethod
    def choose_search_option_by_sex(sex):
        message_body = f'Пол: {sex}.\n' \
                       f'Кого будем искать?'
        return message_body

    @staticmethod
    def missing_age():
        message_body = f'Возраст: Нет данных.\n' \
                       f'Поиск ровестников невозможен.\n' \
                       f'Задайте возрастной диапазон.\n' \
                       f'Например от 25 до 35.'
        return message_body

