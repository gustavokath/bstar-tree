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
            dblock = buffer.get_datablock(self.BTREE_ROOT_DEFAULT)
            btree_root = BTree(root=self.BTREE_ROOT_DEFAULT, buffer=self.buffer)
        except:
            btree_root = None
        return cls(buffer=buffer, btree=btree_root)

    def insert(self, code, desc):
        """
        Inserts code and desc into table
        """
        if(self.btree is None):
            self.btree = BTree(root=self.BTREE_ROOT_DEFAULT, buffer=self.buffer)
            self.btree.init()

        new_record = Record(code=code, description=desc)
        #Search if code already exists
        if(self.btree.has_key(code)):
            print('Record with code %s already exists' % code)
            return None

        dblock, position = self.buffer.search_dblock_with_free_space(new_record.size()+4, 1)
        dblock.write_data(new_record, position)
        print('Record Inserted')
        pass

    def select_code(self, code):
        """
        Finds record with code
        Uses btree for index
        """
        #Without btree
        records = self.buffer.linear_search_record(1, code, 'code', True)
        print(records)
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
        #Without btree
        records = self.buffer.linear_search_record(1, code, 'code', True)
        if(records is None):
            print('Record not found')
            return None
        record = records[0]
        dblock = self.buffer.get_datablock(record.rowid.dblock)
        result = dblock.update_record(record, desc)
        if(result):
            print('Record Updated')
            return None

        update_record = record
        update_record.description = desc
        update_record.rowid = None
        dblock, position = self.buffer.search_dblock_with_free_space(update_record.size()+4, 1)
        dblock.write_data(update_record, position)
        print('Record Updated')
        pass

    def delete(self, code):
        """
        Deletes record by code
        Finds record through select_code()
        """
        records = self.buffer.linear_search_record(1, code, 'code', True)
        if(records is None):
            print('Record not found')
            return None
        record = records[0]
        dblock = self.buffer.get_datablock(record.rowid.dblock)
        dblock.delete_record(record)
        print('Record Removed')
        pass

    def exit(self):
        self.buffer.flush()
        pass
