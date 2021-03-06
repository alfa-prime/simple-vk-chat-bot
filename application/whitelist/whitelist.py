from application.database import session
from application.database.models import Record
from application.database.database import WhiteList

""" белый список текущего пользователя """

class CurrentWhiteList:
    def __init__(self, user_id):
        self.db_session = session.create()

        self.total = 0
        self._counter = 0

        self.items = self._get_items(user_id)

    def _get_items(self, user_id):
        result = self.db_session.query(WhiteList).filter_by(user_id=user_id).all()
        self.total = len(result)
        return iter(result) if self.total > 0 else False

    def __iter__(self):
        return self

    def __next__(self):
        self._counter += 1
        item = next(self.items)
        return Record(self._counter, item.target_id, item.name, item.link, item.bdate, self.total)
