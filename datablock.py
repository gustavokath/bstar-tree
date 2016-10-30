import attr
import struct

@attr.s
class Datablock:
    data = attr.ib()
    address = attr.ib()
    type = attr.ib(default=0)
    count_record = attr.ib(default=0)
    _dirty = attr.ib(default=False)
    deleted = attr.ib(default=False)
    DATABLOCK_SIZE = 2 * 1024

    def set_data(self, data):
        self.data = data
        self._dirty = True

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
        return cls(data=data, address=address, count_record=count_record)
