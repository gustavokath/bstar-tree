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

    def get_datablock(self, dblock):
        with open('data/' + self.filename, 'rb') as f:
            f.seek(dblock * 2)  # Round up to 2B
            data = f.read(2)  # Read two bytes
            print(data)
            return Datablock.from_bytes(data)

    def write_datablock(self, dblock):
        with open('data/' + self.filename, 'wb+') as f:
            f.seek(dblock.address * 2)
            f.write(dblock.data)
