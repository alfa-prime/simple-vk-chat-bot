from dataclasses import dataclass
from types import SimpleNamespace

@dataclass
class UserProperties:
    """ свойства пользователя """
    id: int = None
    first_name: str = None
    last_name: str = None
    city_id: int = None
    city_name: str = None
    age: int = None

    has_error: str = None
    is_deactivated: str = None
    search_attr: \
        SimpleNamespace = SimpleNamespace(sex_id=None, city_id=None, age_from=None, age_to=None, relation_id=None)
