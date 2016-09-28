import attr
from datafile import Datafile

@attr.s
class BTree:
    maxnodes = attr.ib()
