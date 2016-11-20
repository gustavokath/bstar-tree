import attr
from buffer import Buffer
from record import Record
from btree import BTree


@attr.s
class Table:
    BTREE_ROOT_DEFAULT = 16300
    buffer = attr.ib(validator=attr.validators.instance_of(Buffer))
    btree = attr.ib(default=None)

    @classmethod
    def init(cls, datafile):
        buffer = Buffer.init(datafile)
        try:
            config_datablock = buffer.get_datablock(int(buffer.datafile.NUM_DATABLOCKS)-1)
            btree_root = BTree(root=config_datablock.btree_root, buffer=buffer)
        except(EnvironmentError):
            btree_root = None
        return cls(buffer=buffer, btree=btree_root)

    def insert(self, code, desc):
        """
        Inserts code and desc into table
        """
        if(self.btree is None):
            new_config = self.buffer.new_datablock(4, self.buffer.datafile.NUM_DATABLOCKS-1)
            self.btree = BTree(root=self.BTREE_ROOT_DEFAULT, buffer=self.buffer)
            self.btree.init()

        new_record = Record(code=code, description=desc)
        #Search if code already exists
        if(self.btree.has_key(code)):
            print('Record with code %s already exists' % code)
            return None

        dblock, position = self.buffer.search_dblock_with_free_space(new_record.size()+4, 1)
        new_record = dblock.write_data(new_record, position)
        self.btree.insert(new_record.code, new_record.rowid)
        print('Record Inserted')
        pass

    def select_code(self, code):
        """
        Finds record with code
        Uses btree for index
        """
        if(self.btree is None):
            print('[]')
            return None

        rowid = self.btree.find_key(code)
        if(rowid is None):
            print('[]')
            return None

        dblock = self.buffer.get_datablock(rowid.dblock)
        print(dblock.get_record_by_pos(rowid.pos))
        pass

    def select_desc(self, desc):
        """
        Finds record by description
        Can't use btree
        """
        records = self.buffer.linear_search_record(1, desc, 'description')
        print(records)
        pass

    def update(self, code, desc):
        """
        Updates record code with new description desc
        Finds record through select_code()
        """
        if(self.btree is None):
            print('[]')
            return None

        rowid = self.btree.find_key(code)
        if(rowid is None):
            print('Record not found')
            return None

        dblock = self.buffer.get_datablock(rowid.dblock)
        record = dblock.get_record_by_pos(rowid.pos)
        result = dblock.update_record(record, desc)
        if(result):
            print('Record Updated')
            return None

        update_record = record
        update_record.description = desc
        update_record.rowid = None
        dblock, position = self.buffer.search_dblock_with_free_space(update_record.size()+4, 1)
        record = dblock.write_data(update_record, position)
        self.btree.update(record.code, record.rowid)
        print('Record Updated')
        pass

    def delete(self, code):
        """
        Deletes record by code
        Finds record through select_code()
        """
        if(self.btree is None):
            print('[]')
            return None

        rowid = self.btree.find_key(code)
        if(rowid is None):
            print('Record not found')
            return None

        dblock = self.buffer.get_datablock(rowid.dblock)
        record = dblock.get_record_by_pos(rowid.pos)
        dblock.delete_record(record)
        self.btree.delete(code)
        print('Record Removed')
        pass

    def exit(self):
        self.buffer.flush()
        pass
