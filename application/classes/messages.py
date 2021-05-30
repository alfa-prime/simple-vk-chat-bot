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
                       f'Затем он ищет подходящие кандидатуры\n' \
                       f'Критерии совпадения:\n\n' \
                       f'город: совпадает с городом пользователя;\n' \
                       f'пол: противоположный;\n' \
                       f'семейное положение: в активном поиске или неженатые;\n' \
                       f'возраст: ровестники (возраст пользователя +/- 2 года) или задается диапазон'
        return message_body

    @staticmethod
    def user_info(user):
        full_name = f"{user.first_name} {user.last_name}"

        sex_id_to_text = {1: 'женский', 2: 'мужской', 0: 'не указан'}
        sex = sex_id_to_text[user.sex_id]

        age = user.age if user.age else 'Нет данных'
        city = user.city_name if user.city_name else 'Нет данных'

        message_body = f'Имя: {full_name}\n' \
                       f'Пол: {sex}\n' \
                       f'Возраст: {age}\n' \
                       f'Город: {city}'

        return message_body

    @staticmethod
    def choose_search_option_by_age(age):
        message_body = f'Возраст: {age}. Какой вариант поиска будем использовать?\n' \
                       f'"Ровестники": возраст +/- 2 года;\n' \
                       f'"Диапазон": задать возрастной диапазон. Например от 20 до 25.'
        return message_body
