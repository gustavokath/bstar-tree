import attr
import struct
from rowid import Rowid

def len_less_than_200(instance, attribute, value):
    if type(value) is not str:
        raise TypeError("Description must be a string")
    if len(value) > 200:
        raise ValueError("Description must be less than 200 chars long!")


@attr.s
class Record:
    code = attr.ib(validator=attr.validators.instance_of(int))
    description = attr.ib(validator=len_less_than_200)
    # WARNING: must call attr.validate(description) on EVERY update
    rowid = attr.ib(default=None)
    deleted = attr.ib(default=False)

    def pack(self):
        if(self.deleted):
            return b''
        return struct.pack('I%ss' % self.writeble_size(self.description), self.code, self.description.encode())

    def writeble_size(self, str_obj):
        size = len(str_obj)
        for i in range(0,4):
            if((size+i) % 4 == 0):
                return size+i
        return int(size)

    def size(self):
        return self.writeble_size(self.description) + 4
