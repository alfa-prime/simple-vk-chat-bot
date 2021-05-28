class Dispatcher:
    """
        обрабатывает входящие сообщения пользователя, кроме поиска,
        формирует ответ бота
    """
    @staticmethod
    def process_message(received_message, sender_name):
        if received_message == 'начать':
            message = f'Здравствуйте, {sender_name}.\n' \
                      f'Для поиска пары, используйте \n' \
                      f'команду Поиск\n' \

            return dict(message=message)

        else:
            return dict(message='Неизвестная команда')
