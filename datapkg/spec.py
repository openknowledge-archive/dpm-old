import os
import urlparse
import urllib

from datapkg import CONFIG

class Spec(object):
    '''A "spec" is a string identifying a package within a package index
    (or, sometimes, just the index).
    
    It therefore combines index/repository information with an identifier for
    that package within the index. It is directly based on URIs.

    Spec strings start with as 'scheme' part identifying the type of index and
    then have additional information used to specify the package (and perhaps
    the index). For example, for the 3 types of index currently available::

        ckan://{package-name}
        file://{index-path}/{package-name}
        db://{packag-name} 
    
    Examples::

        ckan://datapkgdemo # datapkgdemo package in the CKAN index
        file:///some/path/on/disk
        file://. # current directory
        file://./xyz # relative path xyz from the current directory
        db://datapkgdemo # datapkgdemo in the (local) database index

    For the convenience of users we also support a default index (set in the
    config file). This allows one to simply use the package identifier for the
    spec, e.g.::

        datapkgdemo
    '''
    '''
    Issues
    ======
    
      * file specs are ambiguous as to division into index path and package
        name (if we were allow names to be paths)
    '''
    def __init__(self, scheme='file', netloc='', path=''):
        self.scheme = scheme
        self.netloc = netloc
        self.path = path

    @classmethod
    def parse_spec(self, spec_str, all_index=False):
        '''Parse a a string into a `Spec`.

        :param spec_str: the spec string.
        :param all_index: this spec_str is just an index (useful for file
        specs)
        '''
        scheme, netloc, path, query, fragment = urlparse.urlsplit(spec_str)
        # case where we just provide a path ...
        if scheme == '':
            # default scheme
            scheme = CONFIG.get('datapkg', 'index.default')

        if scheme == 'file':
            if '://' in spec_str:
                path = spec_str.split('://')[1]
            path = urllib.url2pathname(path)
            path = path.replace('/', os.sep)
            path = os.path.abspath(path)
            # for file netloc is everything up to last name
            if all_index:
                netloc = path
                path = ''
            else:
                netloc = os.path.join(os.path.dirname(path))
                path = os.path.basename(path)
        elif scheme in ('ckan', 'db', 'egg'):
            # python >= 2.6.5 changes behaviour of urlsplit for novel url
            # schemes to be rfc compliant
            # http://bugs.python.org/issue7904
            # urlparse.urlsplit(ckan://ckan) gives:
            # python < 2.6.5
            # SplitResult(scheme='ckan', netloc='', path='ckan', query='', fragment='')
            # python >= 2.5.5
            # SplitResult(scheme='ckan', netloc='ckan', path='', query='', fragment='')
            if netloc != '': # python >= 2.6.5
                path = netloc + path if path else netloc
                netloc = ''
            # after urlsplit of ckan://... have path = //... for python < 2.6.5
            while path.startswith('/'):
                path = path[1:]
            netloc = '/'.join(path.split('/')[:-1])
            path = path.split('/')[-1]
            if scheme == 'ckan':
                # we have a path but did not put http:// ...
                if netloc and not netloc.startswith('http'):
                    netloc = 'http://' + netloc
            elif scheme == 'db':
                if netloc and not netloc.startswith('file'):
                    netloc = 'file://' + netloc
            elif scheme == 'egg':
                if path and not netloc:
                    netloc, path = path, ''
                netloc = netloc.strip("/")
                path = path.lstrip("/")
        spec = Spec(scheme, netloc, path)
        return spec

    def index_from_spec(self):
        '''Load an `Index` from a spec.

        :return: `Index` and path
        '''
        import datapkg.index
        index_name = self.scheme
        index_class = datapkg.index.get_index(self.scheme)
        if index_class is None:
            msg = 'Scheme "%s" not recognized' % self.scheme
            raise Exception(msg)
        if self.netloc:
            index = index_class(self.netloc)
        else:
            index = index_class()
        return index, self.path
    
    def __str__(self):
        return '<Spec %s>' % (self.scheme + '://' + self.netloc + '/' +
                self.path)

