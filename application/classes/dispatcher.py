from ..classes.user import User

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

        if '#' in received_message:
            user = User(received_message[1:])
            if user.has_error:
                message = user.has_error
            elif user.is_deactivated:
                message = user.is_deactivated
            else:
                message = user
            return dict(message=message)

        else:
            message = 'Неизвестная команда'
            return dict(message=message)
