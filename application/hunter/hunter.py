from datetime import datetime
from vk_api.execute import VkFunction
from ..database import session
from ..database.models import Record
from ..database.database import BlackList, WhiteList

""" Класс поиска кандидатур для пользователя """

class Hunter:
    def __init__(self, user):
        self.user = user
        self.user_api = user.api
        self.search_attr = user.search_attr

        self._counter = 0
        self.total = 0

        self.targets = iter(self._search())

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(search_attr: {self.search_attr!r}, targets_count: {self.total!r}, targets: {self.targets!r})')

    def _search(self):
        """ запускаем процедуру поиска и возвращем список найденых кандидатур """
        raw_data = self._get_raw_data()
        filtered_data = self._filter_out_raw_data(raw_data)
        self.total = len(filtered_data)
        return self._make_targets_list(filtered_data)

    def _get_raw_data(self):
        """ получаем исходные данные всех найденных кандидатур """
        current_year = datetime.now().year
        year_to = current_year - self.search_attr.age_from
        year_from = current_year - self.search_attr.age_to
        sex_id = self.search_attr.sex_id
        city_id = self.search_attr.city_id
        relation_id = self.search_attr.relation_id
        raw_data = list()

        for year in range(year_from, year_to):
            code = self._exec_string(city_id, sex_id, year, relation_id)
            data = VkFunction(code=code)

            for item in data(self.user_api):
                raw_data += item

        return raw_data

    @staticmethod
    def _exec_string(city_id, sex_id, year, relation_id):
        """
        используется метод vk api https://vk.com/dev/execute
        формируем код для использвания vk api exec
        выбираются пользователи по году и месяцу рождения
        с одни user_token ограничение выборки 7 лет,
        так же крупные города все что больше 1000 записей (за один месяц года) не попадет в выборку,
        ограничение метода vk api https://vk.com/dev/users.search
        """
        api = f"API.users.search({{'count':1000, 'city':{city_id}, 'birth_month': 1, 'birth_year':{year}, " \
              f"'has_photo':1,'sex':{sex_id}, 'fields':'city, sex, relation, bdate', 'status': {relation_id}}}).items"
        for i in range(2, 13):
            api += f", API.users.search({{'count':1000, 'city':{city_id}, 'birth_month':{i}, 'birth_year':{year}," \
                   f"'has_photo':1,'sex': {sex_id}, 'fields':'city, sex, relation, bdate'," \
                   f"'status': {relation_id}}}).items"
        return f"return [{api}];"

    def _filter_out_raw_data(self, raw_data):
        """
        фильтруем результат поиска, выбираем только тех у кого:
        1. страница доступна
        2. по непонятным пока для меня причинам в отбор попадают и другие города,
        поэтому запрошенный город фильтруется дополнительно
        3. по полу, так же как и по городам
        4. исключаются кандидаты, которые были внесены в BlackList и WhiteList
        """
        db_session = session.create()

        black_list = db_session.query(BlackList).filter_by(user_id=self.user.id).all()
        black_list_ids = [items.target_id for items in black_list]

        white_list = db_session.query(WhiteList).filter_by(user_id=self.user.id).all()
        white_list_ids = [items.id for items in white_list]

        result = [v for v in raw_data if
                  not v.get('is_closed')
                  and v.get('city')
                  and v.get('city').get('id') == self.search_attr.city_id
                  and v.get('sex') == self.search_attr.sex_id
                  and v.get('id') not in black_list_ids
                  and v.get('id') not in white_list_ids
                  ]

        return result

    def _make_targets_list(self, filtered_data):
        """ формируем и возвращаем список найденых кандидатур """
        result = tuple()
        for item in filtered_data:
            self._counter += 1
            target_id = item.get('id')
            full_name = f"{item.get('first_name')} {item.get('last_name')}"
            link = f"https://vk.com/id{target_id}"
            bdate = item.get('bdate') if item.get('bdate') else 'Нет данных'
            result += Record(self._counter, target_id, full_name, link, bdate, self.total),
        return result

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.targets)
