import attr
from buffer import Buffer
from rowid import Rowid

@attr.s
class BTree:
    root = attr.ib() #Store first datablock address
    buffer = attr.ib()

    def init(self):
        return self.buffer.new_datablock(3, self.root)

    def has_key(self, key_value):
        result = self.find_key(key_value)
        if(result is None):
            return False
        return True

    def find_key(self, key_value):
        root_dblock = self.buffer.get_datablock(self.root)
        next_addr = root_dblock.find_key(key_value)
        while(next_addr is not None):
            next_dblock = self.buffer.get_datablock(next_addr)
            next_addr = next_dblock.find_key(key_value)
            if(isinstance(next_addr, Rowid)):
                return next_addr
        return None

#    def insert(self, key_value):
