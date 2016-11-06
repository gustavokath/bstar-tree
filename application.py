import struct
from btree import BTree
from datafile import Datafile
from table_datablock import TableDatablock
from node_datablock import NodeDatablock
from leaf_datablock import LeafDatablock


if __name__ == "__main__":
    datafile = Datafile(filename="test")
    # datafile.create_new()
    #print(datafile.get_datablock(100))

    table_data = struct.pack('BHHHHHI8sI2020s', 1, 2,0,12,12,9,1,b'Paolinha',2,b'Teste')
    dblock = TableDatablock.from_bytes(4, table_data, 2)
    datafile.write_datablock(dblock)
    print(datafile.get_datablock(dblock.address))


    node_data = struct.pack('BHHHIIH2030s', 2, 2,0,1,1,2,2,b'A')
    node_dblock = NodeDatablock.from_bytes(100, node_data, 2)
    datafile.write_datablock(node_dblock)
    print(datafile.get_datablock(100))

    leaf_data = struct.pack('BHHHHHII%ss' % 2028, 3, 2, 0, 1, 2, 3, 4, 5, b'\x00')
    leaf_dblock = LeafDatablock.from_bytes(200, leaf_data, 2)
    datafile.write_datablock(leaf_dblock)
    print(datafile.get_datablock(200))

    print('B*')
