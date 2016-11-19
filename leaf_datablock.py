import attr
import struct
from datablock import Datablock
from rowid import Rowid


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
        free_space = self.free_space()
        rowid_buffer = bytearray(self.count_record*4)
        for i in range(0,len(self.rowids)):
            struct.pack_into('%ss' % 4, rowid_buffer, i*4, self.rowids[i].pack())

        fmt = 'BH%ss%sI%ss' % (len(rowid_buffer), len(self.keys), free_space)
        return struct.pack(fmt, self.type, self.count_record, rowid_buffer, *self.keys, b'\x00')

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
        #print('WANTED ' + str(key_value))
        #print('FROM ' + str(self.address))
        #print('KEYS ' + str(self.keys))
        for i, key in enumerate(self.keys):
            if(key == key_value):
                return self.rowids[i]
        return None

    def free_space(self):
        return LeafDatablock.DATABLOCK_SIZE - ((self.count_record * 8) + 4)  # Calculate the remaining space in the record data area

    def can_insert(self):
        free_space = self.free_space()-8 #Free space minus space that will be ocuped
        if(free_space < 0):
            return False
        return True

    def insert(self, key_value, rowid):
        if(len(self.keys) == 0):
            self.keys.append(key_value)
            self.rowids.append(rowid)
            self.count_record = len(self.keys)
            self._dirty = True
            return True

        for i, key in enumerate(self.keys):
            if(key == key_value): #If key already exists in teh leaf
                return False
            if(key > key_value):
                self.keys.insert(i, key_value)
                self.rowids.insert(i, rowid)
                self.count_record = len(self.keys)
                self._dirty = True
                return True

        self.keys.append(key_value)
        self.rowids.append(rowid)
        self.count_record = len(self.keys)
        self._dirty = True
        return True

    def insert_and_split(self, key_value, rowid):
        """
        Insert and split leaf in the btree
        """
        inserted = self.insert(key_value, rowid)
        if(not inserted):
            return False
        length = int(len(self.keys)/2)

        left_keys = self.keys[:length]
        left_rowids = self.rowids[:length]
        right_keys = self.keys[length+1:]
        right_rowids = self.rowids[length+1:]
        return left_keys, left_rowids, right_keys, right_rowids

    def update_data(self, keys=[], rowids=[]):
        self.keys = keys
        self.rowids = rowids
        self.count_record = len(keys)
        self._dirty = True
