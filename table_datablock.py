import attr
import struct
from datablock import Datablock
from record import Record
from rowid import Rowid


@attr.s
class TableDatablock(Datablock):
    header = attr.ib(default=[])
    records = attr.ib(default=[])

    def get_data(self):
        """
        Convert header and records to bytes
        """
        b = bytes()
        pack_records = b.join([record.pack() for record in self.records])
        fmt = 'BH%sH%ss' % (len(self.header), self.records_size())
        return struct.pack(fmt, self.type, self.count_record, *self.header, pack_records)

    def save_record(self, record):
        """
        Saves a Record to the datablock
        """
        if type(record) is not Record:
            raise TypeError("Wrong type for save_record()")
        # TODO: check if there's room in the Datablock
        # TODO: save to the Datablock

    def records_size(self):
        return TableDatablock.DATABLOCK_SIZE - ((len(self.header) * 2))

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

        records = TableDatablock.unpack_records(record_info[0], header, address) 

        return cls(address=address, count_record=count_record, type=1,
                   header=header, records=records)

    @staticmethod
    def unpack(count_record, data):
        records_size = TableDatablock.DATABLOCK_SIZE - ((count_record * 4) + 4)  # Calculate the remaining space in the record data area
        print(records_size)

        fmt_header = 'BH%sH%sx' % (count_record * 2, records_size)
        fmt_record = '%ss' % records_size

        header = struct.unpack(fmt_header, data)  # Get binary header data
        records = struct.unpack_from(fmt_record, data, (count_record * 4) + 4)  # Get binary records data
        return header, records

    @staticmethod
    def unpack_records(record_str, header, address):
        """
        Returns a list of Records included in the datablock
        """
        records = []
        for i in range(0, len(header), 2):
            info = struct.unpack_from('I%ss' % (header[i+1]-4), record_str, header[i])
            rowid = Rowid(dblock=address, pos=i)
            records.append(Record(code=info[0], description=info[1].decode(), rowid=rowid))
        return records

