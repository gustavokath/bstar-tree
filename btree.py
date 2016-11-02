import attr
from buffer import Buffer

@attr.s
class BTree:
    root = attr.ib()
