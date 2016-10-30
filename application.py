import struct
from btree import BTree
from datafile import Datafile
from datablock import Datablock


if __name__ == "__main__":
    datafile = Datafile(filename="test")
    #datafile.create_new()
    print(datafile.get_datablock(4))

    aux = struct.pack('cHHHHH2037s', b'1', 2,0,1,1,2, b'B')

    dblock = Datablock(data=aux, address=4)
    datafile.write_datablock(dblock)
    print(datafile.get_datablock(4))
    print('B*')
