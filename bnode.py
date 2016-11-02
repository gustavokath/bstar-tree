import attr
from buffer import Buffer
from node_datablock import NodeDatablock


@attr.s
class BNode:
    datablock = attr.ib(validator=attr.validators.instance_of(NodeDatablock))