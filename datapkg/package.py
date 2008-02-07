import os
from StringIO import StringIO
import urllib
from zipfile import ZipFile


class Package(object):

    def __init__(self, name, **kwargs):
        self.type = 'datapkg'
        self.installed = False
        self.installed_format = 'plain'
        self.name = name
        for k,v in kwargs.items():
            setattr(self, k, v)

    def install(self, cache_path=None):
        # TODO support other download types than zip

        # it is a url so use posixpath
        # import posixpath
        # fn = posixpath.basename(self.download_url)
        fn = self.name
        fp = os.path.join(cache_path, fn)
        urllib.urlretrieve(self.download_url, fp)
        self.installed = True
        self.installed_path = fp
        self.installed_format = 'zip'

    def resource_stream(self, path):
        if self.installed_format == 'plain':
            fp = os.path.join(self.installed_path, path) 
            return file(fp)
        elif self.installed_format == 'zip':
            zf = ZipFile(self.installed_path)
            return StringIO(zf.read(path))
        else:
            msg = 'Installed format %s not supported' % self.installed_format
            raise Exception(msg)


class PackagePython(Package):

    def __init__(self, name, **kwargs):
        super(PackagePython, self).__init__(name, **kwargs)
        self.type = 'python'

    def install(self, cache_path=None):
        # TODO: use setuptools package ...
        import os
        cmd = 'easy_install %s' % self.name
        os.system(cmd)

    def resource_stream(self, path):
        import pkg_resources
        return pkg_resources.resource_stream(self.name, path)


