from application.database import session
from application.database.database import WhiteList

""" белый список текущего пользователя """

class CurrentWhiteList:
    def __init__(self, user_id):
        self.counter = 0
        self.total_count = None
        self.db_session = session.create()
        self.items = self._get_items(user_id)

    def _get_items(self, user_id):
        result = self.db_session.query(WhiteList).filter_by(user_id=user_id).all()
        self.total_count = len(result)
        return iter(result) if self.total_count > 0 else False

    def __iter__(self):
        return self

    def __next__(self):
        self.counter += 1
        item = next(self.items)
        return dict(
            index=self.counter,
            target_id=item.id,
            name=item.name,
            link=item.link,
            bdate=item.bdate,
            total=self.total_count
        )
