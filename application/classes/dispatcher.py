class Dispatcher:
    @staticmethod
    def process_message(received_message, sender_name, message=None):
        if received_message == 'начать':
            message = f'Здравствуйте, {sender_name}'
        return dict(message=message)
