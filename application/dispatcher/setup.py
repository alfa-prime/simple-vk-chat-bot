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

        self.target_id = None
        self.targets = None
        self.targets_count = None
