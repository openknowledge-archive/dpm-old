import os
import logging
import distutils.dist

from datapkg import DatapkgException
import datapkg.metadata
from datapkg.package import Package

logger = logging.getLogger('datapkg.index')

class IndexBase(object):
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

    ourindex = datapkg.index.SimpleIndex()
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
        ourindex = datapkg.index.SimpleIndex()
        for root, dirs, files in os.walk(self.index_path):
            if 'setup.py' in files or 'metadata.txt' in files:
                try:
                    pkg = Package.load(root)
                    ourindex.register(pkg)
                except Exception, inst:
                    logger.warn('Failed to load package at %s because: %s' % (root,
                        inst))
        return ourindex

    def register(self, package):
        import datapkg.distribution
        pkg_path = os.path.join(self.index_path, package.name)
        dist = datapkg.distribution.IniBasedDistribution(package)
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
        return '<datapkg.index.FileIndex %s>' % self.index_path

class DbIndex(IndexBase):
    '''Database-based index.
    '''
    def __init__(self, dburi):
        # import here as we do not want to require sqlalchemy
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        self.dburi = dburi
        self.engine = create_engine(self.dburi)
        print self.engine
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def init(self):
        from datapkg.db import dbmetadata
        dbmetadata.create_all(bind=self.engine)

    # TODO: DEPRECATE or limit number of results
    def list(self):
        return self.session.query(Package).all()

    def register(self, package):
        self.session.add(package)
        self.session.commit()

    def update(self, package):
        self.session.merge(package)
        self.session.commit()

    def has(self, pkg_name):
        num = self.session.query(Package).filter_by(name=pkg_name).count()
        return num > 0

    def get(self, pkg_name):
        pkg = self.session.query(Package).filter_by(name=pkg_name).first()
        # no package may exist with that name
        if pkg:
            self.session.update(pkg)
        return pkg
    
    def search(self, query):
        q = self.session.query(Package).filter(
                Package.name.ilike(u'%' + query + u'%')
                )
        q = q.limit(100)
        pkgs = q.all()
        return pkgs

# TODO: 2009-07-31 remove at some point
# for backwards compatibility
Index = DbIndex

# Todo: Tests on these ckan- functions.
class CkanIndex(IndexBase):

    def __init__(self, rest_api_url, api_key=None):
        self.status_info = ''
        self.rest_api_url = rest_api_url
        if self.rest_api_url.endswith('/'):
            self.rest_api_url = self.rest_api_url[:-1]
        from ckanclient import CkanClient
        service_kwds = {}
        service_kwds['base_location'] = self.rest_api_url
        if api_key:
            service_kwds['api_key'] = api_key
        self._print("datapkg: CKAN config: %s" % service_kwds )
        self.ckan = CkanClient(**service_kwds)

    def _print(self, msg):
        self.status_info += msg + '\n'
        logger.debug(msg)

    def list(self):
        self.ckan.package_register_get()
        self.print_status()
        if self.ckan.last_status == 200:
            if self.ckan.last_message != None:
                pkgs = [ self.cvt_to_pkg({'name': x})
                            for x in self.ckan.last_message ]
                return pkgs
            else:
                self._print("No response data. Check the resource location.")
                # TODO: convert to CKAN exception
        raise Exception(self.status_info)

    def search(self, query):
        # TODO: think this automatically limits results to 20 or so
        for pkg_name in self.ckan.package_search(query)['results']:
            yield self.get(pkg_name)
    
    def has(self, name):
        try:
            out = self.get(name)
            return True
        except Exception, inst:
            if self.ckan.last_status == 404:
                return False
            else:
                raise

    def get(self, name):
        # TODO: convert to return a package object
        self.ckan.package_entity_get(name)
        self.print_status()
        if self.ckan.last_status == 200:
            if self.ckan.last_message != None:
                package_dict = self.ckan.last_message
                pkg = self.cvt_to_pkg(package_dict)
                return pkg
            else:
                return None
        else:
            raise Exception(self.status_info)

    def register(self, package):
        package_dict = package.metadata
        package_dict = dict(package_dict)
        # package_dict['tags'] = []
        self.ckan.package_register_post(package_dict)
        self.print_status()
        if self.ckan.last_status != 200:
            raise Exception(self.status_info)

    def update(self, package):
        package_dict = dict(package.metadata)
        self.ckan.package_entity_put(package_dict)
        self.print_status()
        print package_dict['name']
        if self.ckan.last_status != 200:
            raise Exception(self.status_info)

    def cvt_to_pkg(self, ckan_pkg_dict):
        name = ckan_pkg_dict.get('name', None)
        metadata = datapkg.metadata.Metadata(ckan_pkg_dict)
        pkg = Package()
        pkg.update_metadata(metadata)
        return pkg

    def print_status(self):
        if self.ckan.last_status == None:
            if self.ckan.last_url_error:
                print self.ckan.last_url_error
                self._print("Network error: %s" % self.ckan.last_url_error.reason[1])
        elif self.ckan.last_status == 200:
            pass #self._print("Datapkg operation was a success.")
        elif self.ckan.last_status == 400:
            self._print("Bad request (400). Please check the submission.")
            self._print(str(self.ckan.last_message))
        elif self.ckan.last_status == 403:
            self._print("Operation not authorised (403). Check the API key.")
        elif self.ckan.last_status == 404:
            self._print("Resource not found (404). Please check names and locations.")
        elif self.ckan.last_status == 409:
            self._print("Package already registered or failed to validate (409). Update with 'update'?")
            self._print(str(self.ckan.last_message))
        elif self.ckan.last_status == 500:
            self._print("Server error (500). Unable to service request. Seek help")
            self._print(str(self.ckan.last_message))
        else:
            self._print("System error (%s). Seek help." %  self.ckan.last_status)

