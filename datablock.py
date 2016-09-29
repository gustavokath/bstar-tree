import attr


@attr.s
class Datablock:
    data = attr.ib()
    address = attr.ib()
    dirty = attr.ib(default=False)
    DATABLOCK_SIZE = 2 * 1024 * 8

    def set_data(self, data):
        self.data = data
        self.dirty = True

    @classmethod
    def from_bytes(cls, address, data):
        """
        Creates a new Datablock in memory from a string of bytes
        """
        return cls(data=data, address=address)
