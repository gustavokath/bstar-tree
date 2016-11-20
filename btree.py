import attr
from buffer import Buffer
from rowid import Rowid
from leaf_datablock import LeafDatablock
from node_datablock import NodeDatablock

@attr.s
class BTree:
    root = attr.ib() #Store first datablock address
    buffer = attr.ib()

    def init(self):
        return self.buffer.new_datablock(3, self.root)

    def pretty_print(self, curr_dblock=None):
        if(curr_dblock is None):
            curr_dblock = self.buffer.get_datablock(self.root)


        if(isinstance(curr_dblock, NodeDatablock)):
            print(curr_dblock)
            for next_addr in curr_dblock.nexts:
                next_dblock = self.buffer.get_datablock(next_addr)
                self.pretty_print(next_dblock)

        if(isinstance(curr_dblock, LeafDatablock)):
            print(curr_dblock)

    def has_key(self, key_value):
        result = self.find_key(key_value)
        if(result is None):
            return False
        return True

    def find_key(self, key_value):
        next_addr = self.root
        while(next_addr is not None):
            next_dblock = self.buffer.get_datablock(next_addr)
            next_addr = next_dblock.find_key(key_value)
            if(isinstance(next_addr, Rowid)):
                return next_addr
        return None

    def insert(self, key_value, rowid, curr_dblock=None):

        
        if(curr_dblock is None):

            curr_dblock = self.buffer.get_datablock(self.root)

        if(isinstance(curr_dblock, NodeDatablock)):

            next_addr = curr_dblock.find_key(key_value)
            next_dblock = self.buffer.get_datablock(next_addr)
            result = self.insert(key_value, rowid, next_dblock)
            if(result is None):
                return None

            if(curr_dblock.can_insert()):
                curr_dblock.insert(result[1].keys[0], result[0].address, result[1].address)


                return None


            splited_data = curr_dblock.insert_and_split(result[1].keys[0], result[0].address, result[1].address)
            splited_dblocks = self.split_during_insert(splited_data ,curr_dblock, 2)
            if(curr_dblock.address == self.root):
                self.new_root(splited_dblocks[0], splited_dblocks[1])
            return splited_dblocks

        #IF current datablock is LeafDatablock
        if(curr_dblock.can_insert()):
            curr_dblock.insert(key_value, rowid)


            return None


        splited_data = curr_dblock.insert_and_split(key_value, rowid)
        splited_dblocks = self.split_during_insert(splited_data ,curr_dblock, 3)
        if(curr_dblock.address == self.root):
            self.new_root(splited_dblocks[0], splited_dblocks[1])

        return splited_dblocks


    def split_during_insert(self, splited_data, src_dblock, datablock_type):
        next_free_addr = self.buffer.get_next_empty_datablock()
        new_leaf = self.buffer.new_datablock(datablock_type, next_free_addr)
        new_leaf.update_data(splited_data[2], splited_data[3])

        src_dblock.update_data(splited_data[0], splited_data[1])
        return src_dblock, new_leaf

    def update(self, key_value, rowid):
        next_addr = self.root
        while(next_addr is not None):
            next_dblock = self.buffer.get_datablock(next_addr)
            if(isinstance(next_dblock, LeafDatablock)):
                next_dblock.update_rowid(key_value, rowid)
                return
            next_addr = next_dblock.find_key(key_value)
        return None

    def delete(self, key_value):
        next_addr = self.root
        while(next_addr is not None):
            next_dblock = self.buffer.get_datablock(next_addr)
            if(isinstance(next_dblock, LeafDatablock)):
                next_dblock.delete(key_value)
                return
            next_addr = next_dblock.find_key(key_value)


    def new_root(self, left_dblock, right_dblock):
        next_free_addr = self.buffer.get_next_empty_datablock()
        new_root = self.buffer.new_datablock(2, next_free_addr)
        new_root.update_data([right_dblock.keys[0]], [left_dblock.address, right_dblock.address])


        config_dblock = self.buffer.get_datablock(self.buffer.datafile.NUM_DATABLOCKS-1)
        config_dblock.update_btree_root(new_root.address)
        self.root = new_root.address
