from enum import Enum

class Commands(Enum):
    start = ('начать', 'привет', 'здравствуй', 'здоров', 'старт', 'погнали', 'hi')
    help = ('помощь', 'инфо', 'help', 'команда')
    search = ('искать', 'новый поиск', 'поиск', 'ищи')
    choose_source_user = ('для меня', 'не для меня')
    choose_targets_sex = ('мужчин', 'женщин')
    choose_targets_relation = ('не женат/не замужем', 'в активном поиске')
    choose_targets_age = ('ровестники', 'диапазон')

