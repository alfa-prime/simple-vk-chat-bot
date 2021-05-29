from ..classes.keyboards import Keyboards

class Dispatcher:
    """
        обрабатывает входящие сообщения пользователя, кроме поиска,
        формирует ответ бота
    """
    @staticmethod
    def process_message(received_message, sender_name):
        if received_message == 'начать':
            message = f'Здравствуйте, {sender_name}\n' \
                      f'Для поиска пары, используйте команду "Поиск"\n' \
                      f'Подробности по команде "Инфо"\n' \

            return dict(message=message, keyboard=Keyboards.main())

        if received_message == 'инфо':
            message = f'По команде "Поиск"\n' \
                      f'бот запрашивает id или screen_name пользователя ВК,\n' \
                      f'для которого будет подыскивается пара.\n' \
                      f'После проверки id на валидность, \n' \
                      f'бот пытается собрать необходимые для поиска данные,\n' \
                      f'если какие-то не найдены, то просит у пользователя ввести их.'
            return dict(message=message, keyboard=Keyboards.search())

        else:
            return dict(message='Неизвестная команда')
