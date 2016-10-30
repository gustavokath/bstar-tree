import attr
import struct

@attr.s
class Datablock:
    address = attr.ib()
    type = attr.ib(default=0)
    count_record = attr.ib(default=0)
    _dirty = attr.ib(default=False)
    deleted = attr.ib(default=False)
    DATABLOCK_SIZE = 2 * 1024  # We think this is bytes because all operations in this value are with numbers in bytes

    def get_data(self):
        return struct.pack('cH%ss' % (Datablock.DATABLOCK_SIZE - 3),self.type, self.count_record, b'0')

    def delete(self):
        self.deleted = True
        self._dirty = True

    def empty(self):
        return self.data == b'\0'

    @classmethod
    def from_bytes(cls, address, data, count_record):
        """
        Creates a new Datablock in memory from a string of bytes
        """
        return cls(address=address, count_record=count_record)
