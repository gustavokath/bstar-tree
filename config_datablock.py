import attr
import struct
import math
import re
import copy
from datablock import Datablock
from record import Record
from rowid import Rowid


@attr.s
class ConfigDatablock(Datablock):
    btree_root = attr.ib(default=16300)

    def get_data(self):
        """
        Convert header and records to bytes
        """
        fmt = 'BHI'
        data = struct.pack(fmt, self.type, self.count_record, self.btree_root)
        return data

    def records_size(self):
        return TableDatablock.DATABLOCK_SIZE - 8

    def update_btree_root(self, new_addr):
        self.btree_root = new_addr
        self._dirty = True

    @classmethod
    def from_bytes(cls, address, data=None, count_record=0):
        """
        Creates a new TableDatablock in memory from a string of bytes
        """
        if(count_record == 0 and data is None):
            config_dblock = cls(address=address, count_record=count_record, type=4,
                       btree_root=16300)
            config_dblock._dirty = True
            return config_dblock

        raw_info = ConfigDatablock.unpack(count_record, data)

        return cls(address=address, count_record=count_record, type=4, btree_root=raw_info[2])

    @staticmethod
    def unpack(count_record, data):
        records_size = ConfigDatablock.DATABLOCK_SIZE -  8 # Calculate the remaining space in the record data area

        fmt_header = 'BHI%sx' % records_size

        info = struct.unpack(fmt_header, data)  # Get binary header data
        return info
