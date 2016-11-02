import attr
import struct
from datablock import Datablock


#Datablock format: B(Type) H(Count Records) N*(H(Next Datablock) I(Key Value))
@attr.s
class NodeDatablock(Datablock):
    nexts = attr.ib(default=[])
    keys = attr.ib(default=[])

    def get_data(self):
        """
        Convert header and records to bytes
        Format: TypeCountHeaderRecords
        """
        free_space = NodeDatablock.DATABLOCK_SIZE - ((self.count_record * 6) + 6)  # Calculate the remaining space in the record data area
        fmt = 'BH%sH%sIH%ss' % (self.count_record, self.count_record, free_space)
        return struct.pack(fmt, self.type, self.count_record, *self.nexts[:-1], *self.keys,
                           self.nexts[-1], b'\x00')

    @classmethod
    def from_bytes(cls, address, data, count_record):
        """
        Creates a new TableDatablock in memory from a string of bytes
        """
        raw_info = NodeDatablock.unpack(count_record, data)

        nexts = list(raw_info[2:2+count_record])
        nexts.append(raw_info[-1])
        keys = list(raw_info[2+count_record:-1])

        return cls(address=address, count_record=count_record, type=2, nexts=nexts, keys=keys)


    @staticmethod
    def unpack(count_record, data):
        free_space = NodeDatablock.DATABLOCK_SIZE - (
        (count_record * 6) + 6)  # Calculate the remaining space in the record data area

        fmt = 'BH%sH%sIH%sx' % (count_record, count_record, free_space)
        return struct.unpack(fmt, data)  # Get binary header data