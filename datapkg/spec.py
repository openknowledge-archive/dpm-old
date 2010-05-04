import os
import urlparse

class Spec(object):
    '''A "spec" is a string identifying a package.
    
    It therefore combines index/repository information with an identifier for
    that package within the index. It is directly based on URIs.

    Examples:
        ckan://{package-name}
        file://{index-path}/{package-name}

    Issues: file specs are ambiguous as to division into index path and package
    name (if we were allow names to be paths)
    '''
    def __init__(self, scheme='file', netloc='', path=''):
        self.scheme = scheme
        self.netloc = netloc
        self.path = path

    @classmethod
    def parse_spec(self, spec_str, all_index=False):
        '''
        @params spec_str: the spec string.
        @params all_index: this spec_str is just an index (useful for file
        specs)
        '''
        scheme, netloc, path, query, fragment = urlparse.urlsplit(spec_str)
        # case where we just provide a path ...
        if scheme == '':
            scheme = 'file'
        if scheme == 'file':
            # correct for non-absolute pathes
            path = os.path.abspath(path)
            # for file netloc is everything up to last name
            if all_index:
                netloc = os.path.join(netloc, path)
                path = ''
            else:
                netloc = os.path.join(netloc, os.path.dirname(path))
                path = os.path.basename(path)
        if scheme == 'ckan':
            # python >= 2.6.5 changes behaviour of urlsplit for novel url
            # schemes to be rfc compliant
            # http://bugs.python.org/issue7904
            # urlparse.urlsplit(ckan://ckan) gives:
            # python < 2.6.5
            # SplitResult(scheme='ckan', netloc='', path='ckan', query='', fragment='')
            # python >= 2.5.5
            # SplitResult(scheme='ckan', netloc='ckan', path='', query='', fragment='')
            if netloc != '': # python >= 2.6.5
                path = netloc + '/' + path if path else netloc
                netloc = ''
            # after urlsplit of ckan://... have path = //... for python < 2.6.5
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
    
    def __str__(self):
        return '<Spec %s>' % (self.scheme + '://' + self.netloc + '/' +
                self.path)

