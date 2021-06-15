from ..database import session


class DispatcherSetup:
    def __init__(self, api, sender_id, upload):
        self.api = api
        self.sender_id = sender_id
        self.upload = upload
        self.db_session = session.create()

        self.user = None
        self.user_input = None
        self.search_user_id = None

        self.white_list = None

        self.targets = None
        # для хранения свойств текущей просматриваемой кандидатуры
        # для внесения в белый DispatcherTools._add_target_to_whitelist
        # и черный DispatcherTools._add_target_to_blacklist списки
        self.target = None
        # для хранения target_id текущей просматриваемой кандидатуры
        # для удаления из белого списка DispatcherTools._remove_target_from_white_list
        self.target_id = None
