from dataclasses import dataclass
from types import SimpleNamespace as Simple

"""
dataclass - https://docs.python.org/3/library/dataclasses.html
SimpleNamespace - https://docs.python.org/3/library/types.html -> Additional Utility Classes and Functions 
"""

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
    search_attr: Simple = Simple(sex_id=None, city_id=None, age_from=None, age_to=None, relation_id=None)
