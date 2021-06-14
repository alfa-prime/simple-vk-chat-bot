from typing import NamedTuple

""" 
для удобной передачи данных между классами 
используется в классах Hunter и WhiteList при возврате метода __next__

https://docs.python.org/3.6/library/typing.html?highlight=namedtuple#typing.NamedTuple
"""

class Record(NamedTuple):
    index: int
    target_id: int
    name: str
    link: str
    bdate: str
    total: int
