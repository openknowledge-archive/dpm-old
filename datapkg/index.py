import logging
import distutils.dist

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datapkg.package import Package
from datapkg.db import dbmetadata
Session = sessionmaker()

logger = logging.getLogger('datapkg.index')

class IndexBase(object):
    pass

class Index(IndexBase):
    '''Database-based index.
    '''
    def __init__(self, dburi):
        self.dburi = dburi
        self.engine = create_engine(self.dburi)
        Session.configure(bind=self.engine)
        self.session = Session()

    def init(self):
        dbmetadata.create_all(bind=self.engine)

    # TODO: DEPRECATE or limit number of results
    def list(self):
        return self.session.query(Package).all()

    def register(self, pkg):
        self.session.save(pkg)
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
    
    def search(self, name):
        q = self.session.query(Package).filter(
                Package.name.ilike('%' + query + '%')
                )
        q = q.limit(100)
        pkgs = q.all()
        return pkgs


# Todo: Tests on these ckan- functions.
class CkanIndex(IndexBase):
    default_rest_api = 'http://ckan.net/rest/api'

    def __init__(self, rest_api_url=None, api_key=None):
        self.status_info = ''
        if rest_api_url:
            self.rest_api_url = rest_api_url
        else:
            rest_api_url = self.default_rest_api
        if self.rest_api_url.endswith('/'):
            self.rest_api_url = self.rest_api_url[:-1]
        from ckanclient import CkanClient
        service_kwds = {}
        service_kwds['base_location'] = self.rest_api_url
        if api_key:
            service_kwds['api_key'] = api_key
        self._print("datapkg: CKAN config: %s" % service_kwds )
        self.ckan = CkanClient(**service_kwds)

    def init(self):
        # since remote, no initialization needed
        pass

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

    def get(self, pkg_name):
        # TODO: convert to return a package object
        self.ckan.package_entity_get(pkg_name)
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

    def register(self, pkg):
        pkg_dict = self.cvt_pkg_metadata(pkg)
        self.ckan.package_register_post(pkg_dict)
        self.print_status()

    def update(self, pkg):
        pkg_dict = self.cvt_pkg_metadata(pkg)
        self.ckan.package_entity_put(pkg_dict)
        self.print_status()

    def cvt_to_pkg(self, ckan_pkg_dict):
        name = ckan_pkg_dict.get('name', None)
        metadata = distutils.dist.DistributionMetadata()
        for key, value in ckan_pkg_dict.items():
            setkey = key
            tval = value
            if key == 'tags':
                setkey = 'keywords'
            elif key == 'title':
                setkey = 'description'
            elif key == 'notes':
                setkey = 'long_description'
            setattr(metadata, setkey, tval)
        pkg = Package(name=name, metadata=metadata)
        return pkg

    def cvt_pkg_metadata(self, pkg):
        data = pkg.metadata
        name = pkg.name
        title = data.get_description()
        if title == 'UNKNOWN': title = ''
        url = data.get_url()
        if url == 'UNKNOWN': url = ''
        notes = data.get_long_description()
        if notes == 'UNKNOWN': notes = ''
        download_url = data.get_download_url()
        if download_url == 'UNKNOWN': download_url = ''
        tags = " ".join(data.get_keywords()).split(' ')
        pkg_metadata = {
            'name': name,
            'title': title,
            'url': url,
            'download_url': download_url,
            'notes': notes,
            'tags': tags,
        }
        #self._print("datapkg: Loaded package metadata: %s" % pkg_metadata)
        return pkg_metadata

    def print_status(self):
        if self.ckan.last_status == None:
            if self.ckan.last_url_error:
                self._print("Network error: %s" % self.ckan.last_url_error.reason[1])
        elif self.ckan.last_status == 200:
            pass #self._print("Datapkg operation was a success.")
        elif self.ckan.last_status == 400:
            self._print("Bad request (400). Please check the submission.")
        elif self.ckan.last_status == 403:
            self._print("Operation not authorised (403). Check the API key.")
        elif self.ckan.last_status == 404:
            self._print("Resource not found (404). Please check names and locations.")
        elif self.ckan.last_status == 409:
            self._print("Package already registered (409). Update with 'ckanupdate'?")
        elif self.ckan.last_status == 500:
            self._print("Server error (500). Unable to service request. Seek help")
        else:
            self._print("System error (%s). Seek help." %  self.ckan.last_status)

