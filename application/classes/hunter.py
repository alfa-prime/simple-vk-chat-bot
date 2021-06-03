from application.settings import API_VERSION

# 321895964 - id без города

# id семейного положения  1: не женат (не замужем), 6: в активном поиске
# значения ID можно посмотреть https://vk.com/dev/users.search параметр status
RELATION_IDS = (1, 6)

# список дополнительных полей для выдачи
# подробности https://vk.com/dev/users.search параметр fields
FIELDS_TO_SEARCH = 'relation, bdate, city, sex'

class Hunter:
    def __init__(self, user):
        self.user = user
        self.search_attr = user.search_attr
        self.user_api = user.api
        self.targets = self.search()
        self.targets_count = None

    def search(self):
        raw_data = self._get_raw_data()
        filtered_data = self._filter_out_raw_data(raw_data)
        return self._make_targets_list(filtered_data)

    def _get_raw_data(self):
        sex_id = self.search_attr.get('sex_id')
        age_from = self.search_attr.get('age_from')
        age_to = self.search_attr.get('age_to')
        city_id = self.search_attr.get('city_id')

        params = dict(
            city=city_id,
            age_from=age_from,
            age_to=age_to,
            sex=sex_id,
            fields=FIELDS_TO_SEARCH,
            sort=1,
            has_photo=1,
            count=1000,
            v=API_VERSION
        )

        result = self.user_api.users.search(**params).get('items')
        # todo: добавить проверку если ничего не найдено
        return result

    def _filter_out_raw_data(self, raw_data):
        """
        фильтруем результат запроса, выбираем только тех у кого:
        1. страница доступна
        2. семейное положение: не женат (не замужем) или в активном поиске
        3. по непонятным пока для меня причинам в отбор попадают и другие города,
        поэтому запрошенный город фильтруется дополнительно
        4. по полу, так же как и по городам
        """
        print(raw_data)

        result = [v for v in raw_data
                  if v.get('can_access_closed')
                  and v.get('relation') in RELATION_IDS
                  and v.get('city')
                  and v.get('city').get('id') == self.search_attr.get('city_id')
                  and v.get('sex') == self.search_attr.get('sex_id')
                  ]

        self.targets_count = len(result)
        return result

    def _make_targets_list(self, filtered_data):
        result = {}

        for item in filtered_data:
            # метод photos.get https://vk.com/dev/photos.get
            target_id = item.get('id')
            photos = self.user_api.photos.get(owner_id=target_id, album_id='profile', extended=1, count=1000)

            user_full_name = f"{item.get('first_name')} {item.get('last_name')}"
            vk_link = f"vk.com/id{target_id}"
            birthday = item.get('bdate')
            photos_count = photos.get('count')

            result[target_id] = dict(
                name=user_full_name,
                link=vk_link,
                birthday=birthday,
                photos=dict(count=photos_count, items=[]))

            for i in range(photos_count):
                likes = photos.get('items')[i].get('likes').get('count')
                url = photos.get('items')[i].get('sizes')[-1].get('url')
                result[target_id]['photos']['items'].append(dict(likes=likes, url=url))

        return result
