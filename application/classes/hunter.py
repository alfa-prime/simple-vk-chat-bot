import json
from application.settings import API_VERSION

# id семейного положения  1: не женат (не замужем), 6: в активном поиске, 0: не указано
# значения ID можно посмотреть https://vk.com/dev/users.search параметр status
RELATION_IDS = (1, 6, 0)

class Hunter:
    def __init__(self, user):
        self.search_attr = user.search_attr
        self.api = user.api

    def search(self):
        result = self.api.users.search(
            city=self.search_attr.get('city_id').get('value'),
            age_from=self.search_attr.get('age_from').get('value'),
            age_to=self.search_attr.get('age_to').get('value'),
            sex=self.search_attr.get('sex_id').get('value'),
            fields='relation',
            sort=0,
            count=500,
            v=API_VERSION
        )

        with open('result.json', 'w', encoding='utf-8',) as file:
            file.write(json.dumps(result, ensure_ascii=False, indent=4))
