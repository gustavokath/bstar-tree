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
        print(self.count_record)
        print(free_space)
        fmt = 'BH%sI%sH%ss' % (self.count_record, self.count_record+1, free_space)
        print(struct.calcsize(fmt))
        return struct.pack(fmt, self.type, self.count_record, *self.keys, *self.nexts, b'\x00')

    @classmethod
    def from_bytes(cls, address, data=None, count_record=0):
        """
        Creates a new TableDatablock in memory from a string of bytes
        """
        if(count_record == 0 and data is None):
            return cls(address=address, count_record=count_record, type=2, nexts=[], keys=[])

        raw_info = NodeDatablock.unpack(count_record, data)

        nexts = list(raw_info[2+count_record:])
        keys = list(raw_info[2:count_record+2])

        return cls(address=address, count_record=count_record, type=2, nexts=nexts, keys=keys)


    @staticmethod
    def unpack(count_record, data):
        free_space = NodeDatablock.DATABLOCK_SIZE - ((count_record * 6) + 6)  # Calculate the remaining space in the record data area

        fmt = 'BH%sI%sH%sx' % (count_record, count_record+1, free_space)
        return struct.unpack(fmt, data)  # Get binary header data

    def find_key(self, key_value):
        for i, key in self.keys:
            if(key < key_value):
                return self.nexts[i]
            elif(key > key_value and len(self.keys)-1 == i):
                return self.nexts[i+1]
        return None
