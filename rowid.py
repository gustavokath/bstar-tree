import attr
from table_datablock import TableDatablock


@attr.s
class Rowid:
    """
    Rowid points to a record in a datablock
    """
    dblock = attr.ib(validator=attr.validators.instance_of(TableDatablock))
    pos = attr.ib(validator=attr.validators.instance_of(int))

    def get_record(self):
        """
        Returns a Record from the Rowid
        """
        return self.dblock.get_records()[self.pos]