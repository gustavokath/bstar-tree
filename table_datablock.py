import attr
import struct
from collections import namedtuple
from datablock import Datablock



@attr.s
class TableDatablock(Datablock):
    header = attr.ib(default=[])
    records = attr.ib(default='')

    def get_data(self):
        """
        Convert header and records to bytes
        Format: TypeHeaderRecords
        """
        records_size = TableDatablock.DATABLOCK_SIZE - ((len(self.header) * 4) + 4)  # Calculate the remaining space in the record data area
        self.data = struct.pack('cH%sH%sx' % (len(self.header), records_size), self.type, self.count_record, self.header, self.records)

    @classmethod
    def from_bytes(cls, address, data, count_record):
        """
        Creates a new TableDatablock in memory from a string of bytes
        """
        records_size = TableDatablock.DATABLOCK_SIZE-((count_record * 4) + 4)  # Calculate the remaining space in the record data area
        header = []
        RecordInfo = namedtuple('RecordInfo', 'begin size')  # Create tuple to store header info
        header_info = struct.unpack('cH%sH%sx' % (count_record * 2, records_size), data)  # Get binary header data
        i = 0
        while i < count_record * 2:
            header.append(RecordInfo._make((header_info[i+2], header_info[i+2+1])))  # Create Record Info tuple
            i += 2

        record_info = struct.unpack_from('%ss' % records_size, data, (count_record * 4) + 4)  # Get binary records data
        return cls(data=data, address=address, count_record=count_record, type=1, header=header, records=record_info[0])

