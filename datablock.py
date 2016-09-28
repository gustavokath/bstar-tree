import attr


@attr.s
class Datablock:
    data = attr.ib()
    address = attr.ib()
    DATABLOCK_SIZE = 2 * 1024 * 8

    def from_bytes(address, data):
        """
        Creates a new Datablock in memory from a string of bytes
        TODO: Implementation
        """
        return Datablock(data=data, address=address)
