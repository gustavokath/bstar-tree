import attr
import struct
import math
import re
import copy
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
        records_buffer = bytearray(self.records_size())
        for i in range(0,len(self.records)):
            struct.pack_into('%ss' % self.header[2*i+1], records_buffer, self.header[2*i], self.records[i].pack())
        fmt = 'BH%sH%ss' % (len(self.header), len(records_buffer))
        data = struct.pack(fmt, self.type, self.count_record, *self.header, records_buffer)
        return data

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


    def free_contiguous_space(self, space_needed):
        if(len(self.header) == 0):
            return 0

        for i in range(0, len(self.header), 2):
            if(i+2 >= len(self.header)):
                #Check for space in the end of the records area
                if(self.records_size() -(self.header[i]+self.header[i+1]) >= space_needed):
                    return self.header[i]+self.header[i+1]
                else:
                    return -1

            #sCheck for space between records








            space_between = self.header[i+2]-(self.header[i]+self.header[i+1])
            if(self.header[i+1] == 0): #If header wanted is deleted, ignore header space
                space_between += 4

            if(space_needed <= space_between):
                return self.header[i]+self.header[i+1]
        return -1

    def write_data(self, record, position=None):
        if(position is None):
            position = self.free_contiguous_space(record.size()+4)
            if(position == -1):
                print('Error writing data')
                return False
        # Insert Header in the right position
        place = -1
        for i  in range(0, len(self.header), 2):
            if(self.header[i] == position and self.header[i+1] == 0): # Going to use header that was delated
                place = i
                self.header[i+1] = record.size()
                return self._insert_new_record(record, place, True)
            elif(self.header[i] > position):
                place = i
                self.header.insert(i, position)
                self.header.insert(i+1, record.size())
                return self._insert_new_record(record, place)
        if(place == -1):
            place = len(self.header)
            self.header.append(position)
            self.header.append(record.size())
            return self._insert_new_record(record, place)

    def update_record(self, record, desc):
        tmp_record = copy.copy(record)
        tmp_record.description = desc
        pos = record.rowid.pos*2
        can_store = False
        if(pos+2 >= len(self.header)):
            can_store =((self.header[pos+1] + (self.records_size() - (self.header[pos]+self.header[pos+1]))) >= tmp_record.size())
        else:
            can_store = ((self.header[pos+1]+(self.header[pos+2]-self.header[pos+1])) >= tmp_record.size())
        #Check for space between records
        if(can_store):
            record.description = desc
            self.header[pos+1] = record.size()
            self._dirty = True
            return True
        else:
            self.delete_record(record)
            return None

    def delete_record(self, record):
        pos = record.rowid.pos
        self.header[pos*2+1] = 0 #set record removed size to 0 to mark it was removed
        self.records[pos].deleted = True
        self._dirty = True
        return True

    def search_by(self, value, field):
        found_records = []
        for record in self.records:
            if(field == 'code'):
                if(record.code == value and not record.deleted):
                    return [record]
            elif(field == 'description'):
                if(record.description == value and not record.deleted):
                    found_records.append(record)
        return found_records

    def get_record_by_pos(self, position):
        """
        Get specific record by its position
        """
        return self.records[position]

    @classmethod
    def from_bytes(cls, address, data=None, count_record=0):
        """
        Creates a new TableDatablock in memory from a string of bytes
        """
        if(count_record == 0 and data is None):
            return cls(address=address, count_record=count_record, type=1,
                       header=[], records=[])

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
            if(header[i+1] != 0):
                info = struct.unpack_from('I%ss' % (header[i+1]-4), record_str, header[i])
                rowid = Rowid(dblock=address, pos=int(math.ceil(i/2.0)))
                desc = re.sub(r'[^\w]', '', info[1].decode())
                records.append(Record(code=info[0], description=desc, rowid=rowid))
            else:
                rowid = Rowid(dblock=address, pos=int(math.ceil(i/2.0)))
                records.append(Record(code=0, description='', rowid=rowid, deleted=True))
        return records

    def _insert_new_record(self, record, place, reuse=False):
        if(record.rowid is None):
            record.rowid = Rowid(dblock=self.address, pos=int(math.ceil(place/2.0)))
        if(reuse):
            self.records[place] = record
        else:
            self.records.insert(place, record)
        self._dirty = True
        self.count_record = len(self.records)
        return record
