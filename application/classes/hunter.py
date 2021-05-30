import json
from application.settings import API_VERSION

# id семейного положения  1: не женат (не замужем), 6: в активном поиске
# значения ID можно посмотреть https://vk.com/dev/users.search параметр status
RELATION_IDS = (1, 6)

# список дополнительных полей для выдачи
# подробности https://vk.com/dev/users.search параметр fields
FIELDS_TO_SEARCH = 'relation, bdate'

class Hunter:
    def __init__(self, user):
        self.search_attr = user.search_attr
        self.api = user.api

    def search(self):
        result = self.api.users.search(
            # описание всех параметров https://vk.com/dev/users.search
            city=self.search_attr.get('city_id').get('value'),
            age_from=self.search_attr.get('age_from').get('value'),
            age_to=self.search_attr.get('age_to').get('value'),
            sex=self.search_attr.get('sex_id').get('value'),
            fields=FIELDS_TO_SEARCH,
            has_photo=1,
            sort=0,
            count=1000,
            v=API_VERSION
        )

        items = result.get('items')
        filtered_result = [v for v in items if v.get('can_access_closed') and v.get('relation') in RELATION_IDS]
        print(len(filtered_result))

        with open('result.json', 'w', encoding='utf-8',) as file:
            file.write(json.dumps(filtered_result, ensure_ascii=False, indent=4))
