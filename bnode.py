import attr
from buffer import Buffer


@attr.s
class BNode:
    tree = attr.ib()
    contents = attr.ib(default=attr.Factory(list))
    children = attr.ib(default=attr.Factory(list))