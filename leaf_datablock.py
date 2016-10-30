import attr
import struct
from datablock import Datablock


#Datablock format: B(Type) H(Count Records) N*(H(Record Datablock)) N*(H(Record Position) N*(I(Key Value))
@attr.s
class LeafDatablock(Datablock):
    recs_dblock = attr.ib(default=[])
    recs_pos = attr.ib(default=[])
    keys = attr.ib(default=[])

    def get_data(self):
        """
        Convert header and records to bytes
        Format: TypeCountHeaderRecords
        """
        free_space = LeafDatablock.DATABLOCK_SIZE - ((self.count_record * 8) + 4)  # Calculate the remaining space in the record data area
        fmt = 'BH%sH%sH%sI%ss' % (self.count_record, self.count_record, self.count_record, free_space)
        return struct.pack(fmt, self.type, self.count_record, *self.recs_dblock, *self.recs_pos,
                           *self.keys, b'\x00')

    @classmethod
    def from_bytes(cls, address, data, count_record):
        """
        Creates a new TableDatablock in memory from a string of bytes
        """

        raw_info = LeafDatablock.unpack(count_record, data)

        recs_dblock = list(raw_info[2:2+count_record])
        recs_pos = list(raw_info[2+count_record:2*count_record+2])
        keys = list(raw_info[2*count_record +2:])


        return cls(address=address, count_record=count_record, type=3, recs_dblock=recs_dblock,
                   recs_pos=recs_pos, keys=keys)

    @staticmethod
    def unpack(count_record, data):
        free_space = LeafDatablock.DATABLOCK_SIZE - ((count_record * 8) + 4)  # Calculate the remaining space in the record data area
        fmt = 'BH%sH%sH%sI%sx' % (count_record, count_record, count_record, free_space)
        return  struct.unpack(fmt, data)  # Get binary header data