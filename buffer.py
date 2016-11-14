import attr
from datafile import Datafile
BUFFER_SIZE = 256


@attr.s
class Buffer:
    datafile = attr.ib()
    _buff = attr.ib(default=[])
    _last = attr.ib(default=0)
    _next = attr.ib(default=0)

    @classmethod
    def init(cls, datafile):
        """
        Creates a new Datablock in memory from a string of bytes
        """
        return cls(datafile=datafile)

    def flush(self):
        for i in range(0, self._last):
            dblock = self._buff[i]
            if dblock.dirty:
                self.datafile.write_datablock(dblock)

    def new_datablock(self, datablock_type, address):
        dblock = self.datafile.new_datablock(datablock_type, address)
        self._write_to_buffer(dblock)
        return dblock

    def get_datablock(self, address):
        # if it's in cache, return it
        for i in range(0, self._last):
            if self._buff[i].address == address:
                return self._buff[i]

        # if not, try to write it to the cache
        dblock = self.datafile.get_datablock(address)
        if(not dblock):
            raise Exception('Invalid datablock')
        self._write_to_buffer(dblock)
        return dblock

    def search_dblock_with_free_space(self, free_space, datablock_type):
        """
        Load in the buffer the first data block with the space needed
        """
        #First check dablocks in buffer
        for i in range(0, self._last):
            dblock = self._buff[i]
            space = self.get_datablock_free_space(dblock, free_space, datablock_type)
            if(space != -1):
                return dblock, space

        #Check in datafile
        for i in range(0, int(self.datafile.NUM_DATABLOCKS)):
            try:
                dblock = self.get_datablock(i)
            except:
                dblock = self.new_datablock(datablock_type, i)
            space = self.get_datablock_free_space(dblock, free_space, datablock_type)
            if(space != -1):
                return dblock, space


    def get_datablock_free_space(self, dblock, free_space, datablock_type):
        if(dblock.type == datablock_type):
            space = dblock.free_contiguous_space(free_space)
            return space
        return -1

    def _write_to_buffer(self, dblock):
        # find the next empty cell
        if self._last < BUFFER_SIZE:  # there's room in the buffer
            self._buff.append(dblock)
            self._last += 1
        else:  # if none is found, write over the oldest one
            # check if we need to write back
            old = self._buff[self._next]
            # if _next is dirty
            if old._dirty:
                # write back
                self.datafile.write_datablock(old)

            # write to the first in
            self._buff[self._next] = dblock

            # set the pointer to the next oldest
            if self._next >= BUFFER_SIZE - 1:
                self._next = 0
            else:
                self._next += 1
