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
