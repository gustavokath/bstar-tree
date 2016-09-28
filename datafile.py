import attr
from datablock import Datablock

@attr.s
class Datafile:
    filename = attr.ib()
