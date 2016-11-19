import attr
import struct
from datablock import Datablock
from table_datablock import TableDatablock
from node_datablock import NodeDatablock
from leaf_datablock import LeafDatablock
from config_datablock import ConfigDatablock


@attr.s
class Datafile:
    filename = attr.ib()
    filesize = 32 * 1024 * 1024
    NUM_DATABLOCKS = filesize / Datablock.DATABLOCK_SIZE

    def create_new(self):
        file_path = 'data/' + self.filename
        #if not exists(file_path):
        with open(file_path, 'wb+') as f:
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
                return NodeDatablock.from_bytes(address, data, datablock_info[1]) # TODO: Create NodeDataBlock
            elif datablock_type == 3:
                return LeafDatablock.from_bytes(address, data, datablock_info[1]) # TODO: Create LeafDataBlock
            elif datablock_type == 4:
                return ConfigDatablock.from_bytes(address, data, datablock_info[1]) # TODO: Create LeafDataBlock
            else:
                return False

    def write_datablock(self, dblock):
        with open('data/' + self.filename, 'rb+') as f:
            f.seek(int(dblock.address) * int(Datablock.DATABLOCK_SIZE))
            if dblock.deleted:
                for _ in range(0, int(Datablock.DATABLOCK_SIZE)):
                    f.write(b'\0')
            else:
                f.write(dblock.get_data())

    def next_available_datablock(self, address=0):
        for addr in range(address, int(self.NUM_DATABLOCKS)):
            dblock = self.get_datablock(addr)
            if(not dblock):
                return addr

    def datablocks(self):
        for addr in range(0, int(self.NUM_DATABLOCKS)):
            yield self.get_datablock(addr), addr

    def node_datablocks(self):
        for dblock in self.datablocks:
            if type(dblock) is NodeDatablock:
                yield dblock

    def new_datablock(self, datablock_type, address):
        if datablock_type == 1:
            return TableDatablock.from_bytes(address) # Create Datablock
        elif datablock_type == 2:
            return NodeDatablock.from_bytes(address)
        elif datablock_type == 3:
            return LeafDatablock.from_bytes(address)
        elif datablock_type == 4:
            return ConfigDatablock.from_bytes(address)
        else:
            return Datablock.from_bytes(address)
