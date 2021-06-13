from typing import NamedTuple

""" 
для удобной передачи данных между классами 
используется в классах Hunter и WhiteList при возврате метода __next__
"""

class Record(NamedTuple):
    index: int
    target_id: int
    name: str
    link: str
    bdate: str
    total: int
