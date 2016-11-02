import attr
from buffer import Buffer


def len_less_than_200(instance, attribute, value):
    if len(value) > 200:
        raise ValueError("Description must be less than 200 chars long!")

@attr.s
class Table:
    code = attr.ib()
    description = attr.ib(validator=len_less_than_200)
    # WARNING: must call attr.validate(description) on EVERY update

    def insert(self, code, desc):
        """
        Inserts code and desc into table
        """
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