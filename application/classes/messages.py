class Messages:
    @staticmethod
    def welcome(sender_name):
        message_body = f'Здравствуйте, {sender_name}\n' \
                       f'Для поиска пары, используйте команду "Поиск"\n' \
                       f'Подробности по команде "Инфо"\n'
        return message_body

    @staticmethod
    def info():
        message_body = f'По команде "Поиск"\n' \
                       f'бот запрашивает id или screen_name пользователя ВК,\n' \
                       f'для которого будет подыскивается пара.\n' \
                       f'После проверки id на валидность, \n' \
                       f'бот пытается собрать необходимые для поиска данные,\n' \
                       f'если какие-то не найдены, то просит у пользователя ввести их.'
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
