from enum import Enum
from itertools import chain

class Commands(Enum):
    start = ('начать', 'привет', 'здравствуй', 'здоров', 'старт', 'погнали', 'hi')
    help = ('помощь', 'инфо', 'help', 'команда', '?')
    search = ('искать', 'новый поиск', 'поиск', 'ищи')
    source_user = ('для меня', 'не для меня')
    targets_sex = ('мужчин', 'женщин')
    targets_relation = ('не женат/не замужем', 'в активном поиске')
    targets_age = ('ровестники', 'диапазон')

    def check(self, value):
        """ проверяет существует ли команда """
        if value in self.value:
            return value

    @staticmethod
    def all_commands():
        """ выводит список всех команд """
        return list(chain(*[x.value for x in Commands]))
