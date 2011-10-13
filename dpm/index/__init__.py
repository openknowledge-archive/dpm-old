'''Code for talking to various types of dpm Package Indexes (in-memory,
filesystem, database, CKAN).
'''
import pkg_resources

from base import IndexBase


def get_index(index_name):
    '''Get Index class corresponding to the provided `index_name`.

    :param index_name: index name as specified by entry point name (setup.py
        entry_points) used to specify this index.
    '''
    # TODO: could speed this up by caching a dictionary of Index classes at
    # module level
    for entry_point in pkg_resources.iter_entry_points('dpm.index'):
        if entry_point.name == index_name:
            cls = entry_point.load()
            return cls

# TODO: would be nice for this to be a property named default_index
def get_default_index():
    from db import DbIndexSqlite
    idx = DbIndexSqlite()
    idx.init()
    return idx

