import attr
from buffer import Buffer
from leaf_datablock import LeafDatablock
from rowid import Rowid


@attr.s
class BLeaf:
    datablock = attr.ib(validator=attr.validators.instance_of(LeafDatablock))
    left_sibling = attr.ib(validator=attr.validators.instance_of(BLeaf))
    right_sibling = attr.ib(validator=attr.validators.instance_of(BLeaf))
    rowid = attr.ib(validator=attr.validators.instance_of(Rowid))