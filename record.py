import attr
from rowid import Rowid

def len_less_than_200(instance, attribute, value):
    if type(value) is not str:
        raise TypeError("Description must be a string")
    if len(value) > 200:
        raise ValueError("Description must be less than 200 chars long!")


@attr.s
class Record:
    code = attr.ib(validator=attr.validators.instance_of(int))
    description = attr.ib(validator=len_less_than_200)
    # WARNING: must call attr.validate(description) on EVERY update
    rowid = attr.ib(validator=attr.validators.instance_of(Rowid))