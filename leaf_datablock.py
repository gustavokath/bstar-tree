import attr
import struct
from datablock import Datablock


#Datablock format: B(Type) H(Count Records) N*(H(Record Datablock)) N*(H(Record Position) N*(I(Key Value))
@attr.s
class LeafDatablock(Datablock):
    rowids = attr.ib(default=[])
    keys = attr.ib(default=[])

    def get_data(self):
        """
        Convert header and records to bytes
        Format: TypeCountHeaderRecords
        """
        free_space = LeafDatablock.DATABLOCK_SIZE - ((self.count_record * 8) + 4)  # Calculate the remaining space in the record data area
        rowid_buffer = bytearray(self.count_record*4)
        for i in range(0,len(self.records)):
            struct.pack_into('%ss' % 4, rowid_buffer, i*4, self.rowids[i].pack())

        fmt = 'BH%ss%sI%ss' % (len(self.rowids), len(self.keys), free_space)
        return struct.pack(fmt, self.type, self.count_record, *self.rowids, *self.keys, b'\x00')

    @classmethod
    def from_bytes(cls, address, data=None, count_record=0):
        """
        Creates a new TableDatablock in memory from a string of bytes
        """
        if(count_record == 0 and data is None):
            return cls(address=address, count_record=count_record, type=3, rowids=[], keys=[])

        raw_info = LeafDatablock.unpack(count_record, data)

        rowids = []
        for i in range(2,2*count_record+2,2):
            rowid = Rowid(dblock=raw_info[i], pos=raw_info[i+1])
            rowids.append(rowid)
        keys = list(raw_info[2*count_record+2:])

        return cls(address=address, count_record=count_record, type=3, rowids=rowids, keys=keys)

    @staticmethod
    def unpack(count_record, data):
        free_space = LeafDatablock.DATABLOCK_SIZE - ((count_record * 8) + 4)  # Calculate the remaining space in the record data area
        fmt = 'BH%sH%sI%sx' % (count_record*2, count_record, free_space)
        return  struct.unpack(fmt, data)  # Get binary header data

    def find_key(self, key_value):
        for i, key in self.keys:
            if(key == key_value):
                return self.rowids[i]
        return None
