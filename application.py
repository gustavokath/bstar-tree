import struct
from btree import BTree
from datafile import Datafile
from table_datablock import TableDatablock
from node_datablock import NodeDatablock
from leaf_datablock import LeafDatablock
from table import Table
import traceback
import sys
import random
import uuid

def parse_input(cmd, table):
    cmd = cmd.split('(')
    if len(cmd) > 1:
        cmd[1] = cmd[1][:-1]
    if cmd[0] == 'insert':
        return parse_insert(cmd[1], table)
    elif cmd[0] == 'select':
        return parse_select(cmd[1], table)
    elif cmd[0] == 'update':
        return parse_update(cmd[1], table)
    elif cmd[0] == 'delete':
        return parse_delete(cmd[1], table)
    elif cmd[0] == 'btree':
        return parse_btree(table)
    elif cmd[0] == 'wipe':
        return parse_wipe(table)

def parse_wipe(table):
    """
    Wipes the table
    """
    datafile = Datafile(filename="test")
    print("Creating new datafile (and overwriting any existing files!)")
    datafile.create_new()
    table.refresh(datafile)
    print("Datafile created")
    return True

def parse_insert(values, table):
    values = values.split(',')
    if len(values) == 1 :
        try:
            count = int(values[0])
            for _ in range(0, count):
                code = random.randint(0, 4294967295)
                desc = str(uuid.uuid1())
                desc = desc.replace('-','')
                table.insert(code, desc)
            return True
        except ValueError:
            print('Error: Expected parameter \"%s\" to be an integer' % values[0])
            return False
    elif(len(values) == 2):
        try:
            code = int(values[0])
            desc = values[1].strip()
            table.insert(code, desc)
            return True
        except ValueError:
            print('Error: Expected parameter \"%s\" to be an integer' % values[0])
            return False
    else:
        print('Invalid insert command')
        print('Expected 1 or 2 values, %s received' % len(values))
        return False


def parse_select(values, table):
    try:
        code = int(values)
        table.select_code(code)
    except ValueError:
        desc = values
        table.select_desc(desc)

def parse_update(values, table):
    values = values.split(',')
    if len(values) != 2:
        print('Expected 2 parameters, %s received' % len(values))
        return False

    try:
        code = int(values[0])
        desc = values[1].strip()
        table.update(code, desc)
        return True
    except ValueError:
        print('Error: Expected code \"%s\" to be an integer' % values[0])
        return False

def parse_delete(value, table):
    try:
        code = int(value)
        table.delete(code)
        return True
    except ValueError:
        print('Error: Expected code \"%s\" to be an integer' % values[0])
        return False

def parse_btree(table):
    if table.btree is None:
        print('BTree not created yet')
        return None

    table.btree.pretty_print()


if __name__ == "__main__":
    datafile = Datafile(filename="test")
    #datafile.create_new()
    table = Table.init(datafile)

    print('SGBD started')
    finish = False
    while not finish:
        cmd = input('$ ')

        if cmd == 'exit':
            finish = True
            print('Closing SGBD...')
            table.exit()
        else:
            parse_input(cmd, table)





    #table_data = struct.pack('BHHHHHHHI8sI16sI1996s',1,2,0,12,12,8,32,9,1,b'Paolinha',2,b'Test',3,b'longe')
    #dblock = TableDatablock.from_bytes(0, table_data, 3)
    #datafile.write_datablock(dblock)


    #leaf_data = struct.pack('BHHHHHII%ss' % 2028, 3, 2, 0, 1, 2, 3, 4, 5, b'\x00')
    #leaf_dblock = LeafDatablock.from_bytes(200, leaf_data, 2)
    #datafile.write_datablock(leaf_dblock)
