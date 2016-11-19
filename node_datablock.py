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
        free_space = self.free_space()
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
        print('WANTED ' + str(key_value))
        print('FROM ' + str(self.address))
        print('KEYS ' + str(self.keys))
        for i, key in enumerate(self.keys):
            if(key > key_value):
                return self.nexts[i]
            elif(key < key_value and len(self.keys)-1 == i):
                return self.nexts[i+1]
            elif(key == key_value):
                return self.nexts[i+1]
        return None

    def update_data(self, keys=[], nexts=[]):
        print('keys')
        print(keys)
        self.keys = keys
        self.nexts = nexts
        self.count_record = len(keys)
        self._dirty = True

    def free_space(self):
        return NodeDatablock.DATABLOCK_SIZE - ((self.count_record * 6) + 6)  # Calculate the remaining space in the record data area

    def can_insert(self):
        free_space = self.free_space()-6 #Free space minus space that will be ocuped
        if(free_space < 0):
            return False
        return True

    def insert(self, key_value, left_addr, right_addr):
        if(len(self.keys) == 0):
            self.keys.append(key_value)
            self.nexts.append(left_addr)
            self.nexts.append(right_addr)
            self.count_record = len(self.keys)
            self._dirty = True
            return True

        for i, key in enumerate(self.keys):
            if(key == key_value): #If key already exists in the node
                return False
            if(key > key_value):
                self.keys.insert(i, key_value)
                self.nexts.insert(i, left_addr)
                self.count_record = len(self.keys)
                self._dirty = True
                return True

        self.keys.append(key_value)
        self.nexts.append(right_addr)
        self.count_record = len(self.keys)
        self._dirty = True
        return True

    def insert_and_split(self, key_value, left_addr, right_addr):
        """
        Insert and split node in the btree
        """
        inserted = self.insert(key_value, left_addr, right_addr)
        if(not inserted):
            return False
        length_keys = int(len(self.keys)/2)

        left_keys = self.keys[:length_keys]
        left_nexts = self.nexts[:length_keys+1]
        right_keys = self.keys[length_keys+1:]
        right_nexts = self.rowids[length_keys+1:]
        return left_keys, left_nexts, right_keys, right_nexts
