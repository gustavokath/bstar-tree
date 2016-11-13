import struct
from btree import BTree
from datafile import Datafile
from table_datablock import TableDatablock
from node_datablock import NodeDatablock
from leaf_datablock import LeafDatablock
import traceback
import sys
import random
import uuid

def parse_input(cmd):
    cmd = cmd.split('(')
    cmd[1] = cmd[1][:-1]
    if(cmd[0] == 'insert'):
        return parse_input(cmd[1])
    elif(cmd[0] == 'select'):
        return parse_select(cmd[1])
    elif(cmd[0] == 'update'):
        return parse_update(cmd[1])
    elif(cmd[0] == 'delete'):
        return parse_delete(cmd[1])

def parse_insert(values):
    values = values.split(',')
    if(len(values) == 1):
        try:
            count = int(values[0])
            print(count)
            for i in range(0, count):
                code = random.randint(0, 9999999999)
                desc = uuid.uuid1()
            return True
        except ValueError:
            print('Error: Expected parameter \"%s\" to be an integer' % values[0])
            return False
    elif(len(values) == 2):
        try:
            code = int(values[0])
            desc = values[1]
            return True
        except ValueError:
            print('Error: Expected parameter \"%s\" to be an integer' % values[0])
            return False
    else:
        print('Invalid insert command')
        print('Expected 1 or 2 values, %s received' % len(values))
        return False

def parse_select(values):
    try:
        code = int(values)
    except ValueError:
        desc = values

def parse_update(values):
    values = values.split(',')
    if(len(values) != 2):
        print('Expected 2 parameters, %s received' % len(values))
        return False

    try:
        code = int(values[0])
        desc = values[1]
        return True
    except ValueError:
        print('Error: Expected code \"%s\" to be an integer' % values[0])
        return False

def parse_delete(value):
    try:
        code = int(value)
        return True
    except ValueError:
        print('Error: Expected code \"%s\" to be an integer' % values[0])
        return False

if __name__ == "__main__":
    datafile = Datafile(filename="test")
    #datafile.create_new()

    print('SGBD started')
    finish = False
    while(not finish):
        cmd = input('$ ')

        if(cmd == 'exit'):
            finish = True
            print('Closing SGBD...')
        else:
            parse_input(cmd)





    #print(datafile.get_datablock(100))

    #print(struct.calcsize('BHHHHHHHI8sI16sI1996s'))
    #table_data = struct.pack('BHHHHHHHI8sI16sI1996s',1,2,0,12,12,8,32,9,1,b'Paolinha',2,b'Test',3,b'longe')
    #dblock = TableDatablock.from_bytes(0, table_data, 3)
    #datafile.write_datablock(dblock)
    #print(datafile.get_datablock(dblock.address))


    #node_data = struct.pack('BHHHIIH2030s', 2, 2,0,1,1,2,2,b'A')
    #node_dblock = NodeDatablock.from_bytes(100, node_data, 2)
    #datafile.write_datablock(node_dblock)
    #print(datafile.get_datablock(100))

    #leaf_data = struct.pack('BHHHHHII%ss' % 2028, 3, 2, 0, 1, 2, 3, 4, 5, b'\x00')
    #leaf_dblock = LeafDatablock.from_bytes(200, leaf_data, 2)
    #datafile.write_datablock(leaf_dblock)
    #print(datafile.get_datablock(200))

    #print('B*')
