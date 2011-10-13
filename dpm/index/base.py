import os
import logging
import distutils.dist

from dpm import DatapkgException
import dpm.metadata
from dpm.package import Package

logger = logging.getLogger('dpm.index')

class IndexBase(object):
    '''Base class for Index objects, all Index implementations should implement
    the API defined here.
    '''

    def register(self, package):
        '''Register `package` in the Index.'''
        raise NotImplementedError

    def get(self, name):
        '''Get package with name `name`.'''
        raise NotImplementedError
    
    def has(self, name):
        '''Check if package with name `name` is in Index.'''
        raise NotImplementedError

    def list(self):
        '''Return an iterator over all items in the Index'''
        raise NotImplementedError

    def search(self, query):
        '''Return an iterator over search results corresponding to query.'''
        raise NotImplementedError

    def update(self, package):
        '''Update `package` in the Index.'''
        raise NotImplementedError
        
    def __contains__(self, name):
        '''Implement `in` operator using `has` method'''
        return self.has(name)

    def __iter__(self, name):
        '''Implement iteration over the list method'''
        for package in self.list(): yield package

class SimpleIndex(IndexBase):
    '''In memory Index based on a simple dict.'''
    def __init__(self):
        self._dict = {}

    def register(self, package):
        if package.name in self._dict:
            msg = 'Package already registered with name: %s' % package.name
            raise DatapkgException(msg)
        self._dict[package.name] = package

    def get(self, name):
        return self._dict[name]

    def has(self, name):
        return name in self._dict

    def list(self):
        return iter(self._dict.values())

    def search(self, query):
        '''Search packages names using query string.'''
        for name in self._dict:
            if query in name:
                yield self._dict[name]

    def update(self, package): 
        if not package.name in self._dict:
            msg = 'No package registered with name: %s' % package.name
            raise DatapkgException(msg)
        self._dict[package.name] = package


class FileIndex(IndexBase):
    '''Index based on files on disk.
    
    TODO: Could cache in a SimpleIndex

    ourindex = dpm.index.SimpleIndex()
    for root, dirs, files in os.walk(basePath):
        if 'setup.py' in files or 'metadata.txt' in files:
            try:
                pkg = Package.load(root)
                ourindex.register(pkg)
            except Exception, inst:
                logger.warn('Failed to load package at %s because: %s' % (root,
                    inst))
    return ourindex
    '''
    def __init__(self, path):
        self.index_path = path
        # if not os.path.exists(self.index_path):
        #    os.makedirs(self.index_path)

    def _simple_index(self):
        ourindex = SimpleIndex()
        import dpm.distribution
        for root, dirs, files in os.walk(self.index_path):
            try:
                dist = dpm.distribution.load(root)
                pkg = dist.package
                ourindex.register(pkg)
            except Exception, inst:
                logger.warn('Failed to load package at %s because: %s' % (root,
                    inst))
        return ourindex

    def register(self, package):
        import dpm.distribution
        pkg_path = os.path.join(self.index_path, package.name)
        dist = dpm.distribution.default_distribution()(package)
        dist.write(pkg_path)
        return pkg_path

    def get(self, name):
        if not name in self:
            msg = 'No package in %s with name %s. Have you registered/installed it?' % (self, name)
            raise DatapkgException(msg)
        path = os.path.join(self.index_path, name)
        return Package.load(path)

    def has(self, name):
        return name in os.listdir(self.index_path)

    def list(self):
        return self._simple_index().list()

    def search(self, query):
        for pkg in self._simple_index().search(query):
            yield pkg

    def update(self, package): 
        # TODO: do something useful (remove existing and re-register?)
        pass

    def __str__(self):
        return '<dpm.index.FileIndex %s>' % self.index_path

