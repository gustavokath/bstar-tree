import attr
from buffer import Buffer
from record import Record


@attr.s
class Table:
    buffer = attr.ib(validator=attr.validators.instance_of(Buffer))

    @classmethod
    def init(cls, datafile):
        return cls(buffer=Buffer.init(datafile))

    def insert(self, code, desc):
        """
        Inserts code and desc into table
        """
        new_record = Record(code=code, description=desc)
        dblock, position = self.buffer.search_dblock_with_free_space(new_record.size()+4, 1)
        dblock.write_data(new_record, position)
        pass

    def insert_random(self, n):
        """
        Inserts n random records into table
        """
        pass

    def select_code(self, code):
        """
        Finds record with code
        Uses btree for index
        """
        pass

    def select_desc(self, desc):
        """
        Finds record by description
        Can't use btree
        """
        pass

    def update(self, code, desc):
        """
        Updates record code with new description desc
        Finds record through select_code()
        """
        pass

    def delete(self, code):
        """
        Deletes record by code
        Finds record through select_code()
        """
        pass
