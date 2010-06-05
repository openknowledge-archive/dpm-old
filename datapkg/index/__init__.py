'''Code for talking to various types of datapkg Package Indexes (in-memory,
filesystem, database, CKAN).
'''
from base import SimpleIndex, FileIndex
from db import DbIndex, Index
from ckan import CkanIndex

