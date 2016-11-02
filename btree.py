import attr
from buffer import Buffer

@attr.s
class BTree:
    root = attr.ib()
    # root can be either a NodeDatablock or a LeafDatablock
