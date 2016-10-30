import attr
import struct
from datablock import Datablock


@attr.s
class TableDatablock(Datablock):
    header = attr.ib(default=[])
    records = attr.ib(default='')

    def get_data(self):
        """
        Convert header and records to bytes
        """
        fmt = 'BH%sH%ss' % (len(self.header), len(self.records))
        return struct.pack(fmt, self.type, self.count_record, *self.header, self.records)

    @classmethod
    def from_bytes(cls, address, data, count_record):
        """
        Creates a new TableDatablock in memory from a string of bytes
        """
        header = []
        header_info, record_info = TableDatablock.unpack(count_record, data)

        for i in range(0, count_record * 2, 2):
            header.append(header_info[i+2])  #Get record begin position
            header.append(header_info[i + 2 + 1])  #Get record length

        return cls(address=address, count_record=count_record, type=1,
                   header=header, records=record_info[0])

    @staticmethod
    def unpack(count_record, data):
        records_size = TableDatablock.DATABLOCK_SIZE - ((count_record * 4) + 4)  # Calculate the remaining space in the record data area
        print(records_size)

        fmt_header = 'BH%sH%sx' % (count_record * 2, records_size)
        fmt_record = '%ss' % records_size

        header = struct.unpack(fmt_header, data)  # Get binary header data
        records = struct.unpack_from(fmt_record, data, (count_record * 4) + 4)  # Get binary records data
        return header, records

