from btree import BTree
from datafile import Datafile
from datablock import Datablock


if __name__ == "__main__":
    datafile = Datafile(filename="test")
    # datafile.create_new()
    print(datafile.get_datablock(4))

    dblock = Datablock(data=b'\x42\x42', address=4)
    datafile.write_datablock(dblock)
    print(datafile.get_datablock(4))
    print('B*')
