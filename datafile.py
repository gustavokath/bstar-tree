import attr
from datablock import Datablock


@attr.s
class Datafile:
    filename = attr.ib()
    filesize = 32 * 1024 * 1014

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
            f.write(dblock.data)
