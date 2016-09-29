import attr
from datafile import Datafile
BUFFER_SIZE = 256


@attr.s
class Buffer:
    _buff = attr.ib(default=attr.Factory(list))
    datafile = attr.ib()
    _last = attr.ib(default=0)
    _next = attr.ib(default=0)

    def get_datablock(self, address):
        # if it's in cache, return it
        for i in range(0, self._last):
            if self._buff[i].address == address:
                return self._buff[i]

        # if not, try to write it to the cache
        # find the next empty cell
        # if none is found, write over the oldest one
