from vk_api.execute import VkFunction
from datetime import datetime

# список дополнительных полей для выдачи
# подробности https://vk.com/dev/users.search параметр fields
FIELDS_TO_SEARCH = 'city, bdate, sex, relation'

class Hunter:
    def __init__(self, user):
        self.user = user
        self.search_attr = user.search_attr
        self.user_api = user.api
        self.targets_count = 0
        self.targets = self._search()

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(search_attr: {self.search_attr!r}, targets_count: {self.targets_count!r}, targets: {self.targets!r})')

    def _search(self):
        raw_data = self._get_raw_data()
        filtered_data = self._filter_out_raw_data(raw_data)
        self.targets_count = len(filtered_data)
        return self._make_targets_list(filtered_data)

    @staticmethod
    def _exec_string(city_id, sex_id, year, relation_id):
        """
        используется метод vk api https://vk.com/dev/execute
        формируем код для использвания vk api exec
        выбираются пользователи по году и месяцу рождения
        с одни user_token ограничение выборки 7 лет,
        так же крупные городв все что больше 1000 записей, откидывается
        ограничение метода vk api https://vk.com/dev/users.search
        """
        api = f"API.users.search({{'count':1000, 'city':{city_id}, 'birth_month': 1, 'birth_year':{year}, " \
              f"'has_photo':1,'sex':{sex_id}, 'fields':'city, sex, relation, bdate', 'status': {relation_id}}}).items"
        for i in range(2, 13):
            api += f", API.users.search({{'count':1000, 'city':{city_id}, 'birth_month':{i}, 'birth_year':{year}," \
                   f"'has_photo':1,'sex': {sex_id}, 'fields':'city, sex, relation, bdate'," \
                   f"'status': {relation_id}}}).items"
        return f"return [{api}];"

    def _get_raw_data(self):
        current_year = datetime.now().year
        year_to = current_year - self.search_attr.get('age_from')
        year_from = current_year - self.search_attr.get('age_to')
        sex_id = self.search_attr.get('sex_id')
        city_id = self.search_attr.get('city_id')
        relation_id = self.search_attr.get('relation_id')
        raw_data = list()

        for year in range(year_from, year_to):
            code = self._exec_string(city_id, sex_id, year, relation_id)
            data = VkFunction(code=code)

            for item in data(self.user_api):
                raw_data += item

        return raw_data

    def _filter_out_raw_data(self, raw_data):
        """
        фильтруем результат запроса, выбираем только тех у кого:
        1. страница доступна
        2. по непонятным пока для меня причинам в отбор попадают и другие города,
        поэтому запрошенный город фильтруется дополнительно
        3. по полу, так же как и по городам
        """
        result = [v for v in raw_data if
                  not v.get('is_closed')
                  and v.get('city')
                  and v.get('city').get('id') == self.search_attr.get('city_id')
                  and v.get('sex') == self.search_attr.get('sex_id')]
        return result

    @staticmethod
    def _make_targets_list(filtered_data):
        result = []
        for index, item in enumerate(filtered_data):
            target_id = item.get('id')
            user_full_name = f"{item.get('first_name')} {item.get('last_name')}"
            vk_link = f"vk.com/id{target_id}"
            birthday = item.get('bdate') if item.get('bdate') else 'Нет данных'
            result.append(f'{index + 1}, {target_id}, {user_full_name}, {vk_link}, {birthday}')
        return iter(result)
