import attr
from datablock import Datablock


@attr.s
class Datafile:
    filename = attr.ib()
    filesize = 32 * 1024 * 1014
    NUM_DATABLOCKS = filesize / Datablock.DATABLOCK_SIZE

    def create_new(self):
        with open('data/' + self.filename, 'wb') as f:
            for _ in range(0, self.filesize):
                f.write(b'\0')

    def get_datablock(self, address):
        with open('data/' + self.filename, 'rb') as f:
            raw_address = address * Datablock.DATABLOCK_SIZE  # Round up to 2KB
            f.seek(raw_address)
            data = f.read(Datablock.DATABLOCK_SIZE)  # Read 2KB
            return Datablock.from_bytes(address, data)

    def write_datablock(self, dblock):
        with open('data/' + self.filename, 'wb+') as f:
            f.seek(dblock.address * Datablock.DATABLOCK_SIZE)
            if dblock.deleted:
                for _ in range(0, Datablock.DATABLOCK_SIZE):
                    f.write(b'\0')
            else:
                f.write(dblock.data)

    def next_available_datablock(self):
        for dblock in self.datablocks:
            if dblock.empty():
                return dblock

    def datablocks(self):
        addr = 0
        while addr < self.NUM_DATABLOCKS:
            yield self.get_datablock(addr)
            addr += 1
