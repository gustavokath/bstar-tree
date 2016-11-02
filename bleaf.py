import attr
from buffer import Buffer


@attr.s
class BLeaf:
    tree = attr.ib()
    rowid = attr.ib()
    next = attr.ib()