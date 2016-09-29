import attr
from datafile import Datafile
BUFFER_SIZE = 256


@attr.s
class Buffer:
    _buff = attr.ib(default=attr.Factory(list))
    datafile = attr.ib()
    _last = attr.ib(default=0)
    _next = attr.ib(default=0)

    def flush(self):
        for i in range(0, self._last):
            dblock = self._buff[i]
            if dblock.dirty:
                self.datafile.write_datablock(dblock)

    def get_datablock(self, address):
        # if it's in cache, return it
        for i in range(0, self._last):
            if self._buff[i].address == address:
                return self._buff[i]

        # if not, try to write it to the cache
        dblock = self.datafile.get_datablock(address)
        self._write_to_buffer(dblock)
        return dblock

    def _write_to_buffer(self, dblock):
        # find the next empty cell
        if self._last < BUFFER_SIZE:  # there's room in the buffer
            self._buff[self._last] = dblock
            self._last += 1
        else:  # if none is found, write over the oldest one
            # check if we need to write back
            old = self._buff[self._next]
            # if _next is dirty
            if old.dirty:
                # write back
                self.datafile.write_datablock(old)

            # write to the first in
            self._buff[self._next] = dblock

            # set the pointer to the next oldest
            if self._next >= BUFFER_SIZE - 1:
                self._next = 0
            else:
                self._next += 1
