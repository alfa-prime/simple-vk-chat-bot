class Dispatcher:
    @staticmethod
    def process_message(received_message, sender_name):
        if received_message == 'начать':
            message = f'Здравствуйте, {sender_name}'
            return dict(message=message)

        else:
            message = 'Неизвестная команда'
            return dict(message=message)
