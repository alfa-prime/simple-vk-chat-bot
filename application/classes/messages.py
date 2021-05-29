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

