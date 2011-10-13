from base import *


# Todo: Tests on these ckan- functions.
class CkanIndex(IndexBase):
    '''CKAN index.

    Where parameters not provided look them up in config.

    :param url: url for ckan API.
    :param api_key: API key.
    '''
    def __init__(self, url=None, api_key=None):
        self.status_info = ''
        if url is not None:
            self.url = url
        else:
            self.url = dpm.CONFIG.get('index:ckan', 'ckan.url')
        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = dpm.CONFIG.dictget('index:ckan', 'ckan.api_key', None)
        if self.url.endswith('/'):
            self.url = self.url[:-1]
        from ckanclient import CkanClient
        service_kwds = {}
        service_kwds['base_location'] = self.url
        service_kwds['api_key'] = self.api_key
        self._print("dpm: CKAN config: %s" % service_kwds )
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
        assert name, 'You need to specify the name of the dataset to get'
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
        # HACK - CKAN does not like id field or relationships field atm
        if 'id' in package_dict:
            del package_dict['id']
        if 'relationships' in package_dict:
            del package_dict['relationships']
        # package_dict['tags'] = []
        self.ckan.package_register_post(package_dict)
        self.print_status()
        if self.ckan.last_status not in [200,201]:
            raise Exception(self.status_info)

    def update(self, package):
        package_dict = dict(package.metadata)
        # HACK - CKAN does not like id field or relationships field atm
        if 'id' in package_dict:
            del package_dict['id']
        if 'relationships' in package_dict:
            del package_dict['relationships']
        self.ckan.package_entity_put(package_dict)
        self.print_status()
        print package_dict['name']
        if self.ckan.last_status != 200:
            raise Exception(self.status_info)

    def cvt_to_pkg(self, ckan_pkg_dict):
        name = ckan_pkg_dict.get('name', None)
        metadata = dpm.metadata.Metadata(ckan_pkg_dict)
        pkg = Package()
        pkg.update_metadata(metadata)
        return pkg

    def print_status(self):
        if self.ckan.last_status == None:
            if self.ckan.last_url_error:
                print self.ckan.last_url_error
                self._print("Network error: %s" % self.ckan.last_url_error.reason[1])
        elif self.ckan.last_status in [200,201]: # 201 for create requests
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

