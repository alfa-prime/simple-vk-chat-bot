import json
from application.settings import API_VERSION

# 321895964 - id без города

# id семейного положения  1: не женат (не замужем), 6: в активном поиске
# значения ID можно посмотреть https://vk.com/dev/users.search параметр status
RELATION_IDS = (1, 6)

# список дополнительных полей для выдачи
# подробности https://vk.com/dev/users.search параметр fields
FIELDS_TO_SEARCH = 'relation, bdate, city'

class Hunter:
    def __init__(self, user):
        self.user = user
        self.search_attr = user.search_attr
        self.api = user.api

    def search(self):

        user_id = self.user.id
        sex_id = self.search_attr.get('sex_id')
        age_from = self.search_attr.get('age_from')
        age_to = self.search_attr.get('age_to')
        city_id = self.search_attr.get('city_id')

        # формирую уникальный отпечаток истории поиска юзера
        # идея такая: по заданым параметрам получаю все доступные данные,
        # и сохраняю их в базу и если в следующий попадаются такие же параметры,
        # то сведения берутся из базы, а не запрашиваются у ВК.
        imprint_user_search_history = f'{user_id}-{sex_id}-{age_from}-{age_to}-{city_id}'
        print(imprint_user_search_history)

        result = self.api.users.search(
            # описание всех параметров https://vk.com/dev/users.search
            city=city_id,
            age_from=age_from,
            age_to=age_to,
            sex=sex_id,
            fields=FIELDS_TO_SEARCH,
            has_photo=1,
            count=1000,
            v=API_VERSION
        )

        items = result.get('items')
        """
        фильтруем результат запроса, выбираем только тех у кого:
        1. страница доступна
        2. семейное положение: не женат (не замужем) или в активном поиске
        3. по непонятным пока для меня причинам в отбор попадают и другие города,
           поэтому 'жестко' фильтруется только запрошенный город
        """
        filtered_result = [v for v in items
                           if v.get('can_access_closed')
                           and v.get('relation') in RELATION_IDS
                           and v.get('city')
                           and v.get('city').get('id') == self.search_attr.get('city_id')]

        print(len(filtered_result))

        with open('result.json', 'w', encoding='utf-8',) as file:
            file.write(json.dumps(filtered_result, ensure_ascii=False, indent=4))
