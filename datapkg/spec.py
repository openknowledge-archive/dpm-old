import os
import urlparse

class Spec(object):
    def __init__(self, scheme='file', netloc='', path=''):
        self.scheme = scheme
        self.netloc = netloc
        self.path = path

    @classmethod
    def parse_spec(self, spec_str=None):
        '''
        @params spec: if None default to file://
        '''
        if spec_str is None:
            spec_str = 'file://'
        scheme, netloc, path, query, fragment = urlparse.urlsplit(spec_str)
        # case where we just provide a path ...
        if scheme == '':
            scheme = 'file'
        if scheme == 'file':
            # for file netloc is everything up to last name
            netloc = os.path.join(netloc, os.path.dirname(path))
        if scheme == 'ckan':
            # deal with preceding slashes in ckan://...
            while path.startswith('/'):
                path = path[1:]
            netloc = '/'.join(path.split('/')[:-1])
            # we have a path but did not put http:// ...
            if netloc and not netloc.startswith('http'):
                netloc = 'http://' + netloc
            path = path.split('/')[-1]
        spec = Spec(scheme, netloc, path)
        return spec

    def index_from_spec(self, config=None):
        '''Load an `Index` from a spec.

        @return: `Index` and path

        schemes = [
            'file',
            'ckan',
            'db',
            ]
        '''
        import datapkg.index
        if self.scheme == 'file':
            index = datapkg.index.FileIndex(self.netloc)
        elif self.scheme == 'ckan':
            if self.netloc:
                ckan_url = self.netloc
            else:
                ckan_url = config.get('DEFAULT', 'ckan.url')
            if config:
                api_key = config.get('DEFAULT', 'ckan.api_key')
            index = datapkg.index.CkanIndex(
                    rest_api_url=ckan_url,
                    api_key=api_key)
        else:
            msg = 'Scheme "%s" not recognized' % self.scheme
            raise Exception(msg)
        return index, self.path

