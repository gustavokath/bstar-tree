import attr


@attr.s
class Datablock:
    data = attr.ib()
    address = attr.ib()

    def from_bytes(bytes):
        """
        Creates a new Datablock in memory from a string of bytes
        TODO: Implementation
        """
        return None
