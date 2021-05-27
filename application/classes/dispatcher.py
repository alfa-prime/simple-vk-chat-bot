class Dispatcher:
    @staticmethod
    def process_message(received_message, sender_name):
        if received_message == 'начать':
            message = f'Здравствуйте, {sender_name}.\n\n' \
                      f'Отправте мне id или screen_name\n' \
                      f'пользователя VK, введеный через #.\n' \
                      f'Например: #durov.\n\n' \
                      f'И я постараюсь найти ему подходящую пару.'
            return dict(message=message)

        else:
            return dict(message='Неизвестная команда')
