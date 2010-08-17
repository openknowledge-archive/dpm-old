'''Code for talking to various types of datapkg Package Indexes (in-memory,
filesystem, database, CKAN).
'''
from base import SimpleIndex, FileIndex
from db import DbIndexSqlite, DbIndexSqlalchemy
from ckan import CkanIndex
from egg import EggIndex

# TODO: would be nice for this to be a property named default_index
def get_default_index():
    idx = DbIndexSqlite()
    idx.init()
    return idx


