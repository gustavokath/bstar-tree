import attr
import struct
from datablock import Datablock
from table_datablock import TableDatablock
from knot_datablock import KnotDatablock
from leaf_datablock import LeafDatablock


@attr.s
class Datafile:
    filename = attr.ib()
    filesize = 32 * 1024 * 1024
    NUM_DATABLOCKS = filesize / Datablock.DATABLOCK_SIZE

    def create_new(self):
        file_path = 'data/' + self.filename
        #if not exists(file_path):
        with open(file_path, 'wb') as f:
            for _ in range(0, self.filesize):
                f.write(b'\0')

    def get_datablock(self, address):
        with open('data/' + self.filename, 'rb') as f:
            raw_address = address * Datablock.DATABLOCK_SIZE  # Round up to 2KB
            f.seek(raw_address)
            data = f.read(Datablock.DATABLOCK_SIZE)  # Read 2KB
            datablock_info = struct.unpack('BH%sx' % (Datablock.DATABLOCK_SIZE-4), data) # Get datablock type and number of records
            datablock_type = datablock_info[0]
            if datablock_type == 1:
                return TableDatablock.from_bytes(address, data, datablock_info[1]) # Create Datablock
            elif datablock_type == 2:
                return KnotDatablock.from_bytes(address, data, datablock_info[1]) # TODO: Create NodeDataBlock
            elif datablock_type == 3:
                return LeafDatablock.from_bytes(address, data, datablock_info[1]) # TODO: Create LeafDataBlock
            else:
                return Datablock.from_bytes(address, data, datablock_info[1])

    def write_datablock(self, dblock):
        with open('data/' + self.filename, 'wb+') as f:
            f.seek(dblock.address * Datablock.DATABLOCK_SIZE)
            if dblock.deleted:
                for _ in range(0, Datablock.DATABLOCK_SIZE):
                    f.write(b'\0')
            else:
                f.write(dblock.get_data())

    def next_available_datablock(self):
        for dblock in self.datablocks:
            if dblock.empty():
                return dblock

    def datablocks(self):
        for addr in range(0, self.NUM_DATABLOCKS):
            yield self.get_datablock(addr)

    def node_datablocks(self):
        for dblock in self.datablocks
            if type(dblock) is KnotDatablock:
                yield dblock
