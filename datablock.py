import attr


@attr.s
class Datablock:
    data = attr.ib()
    address = attr.ib()
    DATABLOCK_SIZE = 2 * 1024 * 8

    @classmethod
    def from_bytes(cls, address, data):
        """
        Creates a new Datablock in memory from a string of bytes
        """
        return cls(data=data, address=address)
