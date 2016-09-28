from btree import BTree
from datafile import Datafile


if __name__ == "__main__":
    datafile = Datafile(filename="test")
    datafile.create_new()
    print('B*')
