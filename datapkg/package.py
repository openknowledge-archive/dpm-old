import os
import shutil
from StringIO import StringIO
import urllib
import re
import distutils.dist

import datapkg.util
import datapkg.metadata
import datapkg.pypkgtools
from datapkg import DatapkgException

class Package(object):

    def __init__(self, name=None, metadata=None, **kwargs):
        if name:
            self.name = self._normalize_name(name)
        else:
            self.name = None
        self.init_on_load(metadata, **kwargs)

    # separated out from __init__ for the benefit of sqlalchemy
    def init_on_load(self, metadata=None, **kwargs):
        if metadata:
            self.metadata = metadata
        else:
            self.metadata = datapkg.metadata.Metadata()
            self.metadata['name'] = self.name
        # path to distribution on disk associated to package (if any)
        self.installed_path = None
        # TODO: most of these attributes should run off metadata
        self.download_url = None
        for k,v in kwargs.items():
            setattr(self, k, v)

    def _path_set(self, v):
        self.installed_path = v
    # TODO: rename installed path to path
    path = property(lambda: self.installed_path, _path_set)

    def _normalize_name(self, name):
        new_name = name.lower()
        regex = r'^[\w-]+$'
        if not re.match(regex, new_name):
            msg = 'Invalid package name: %s' % name
            raise ValueError(msg)
        return unicode(new_name)

    def download(self, tmpdir):
        filepath = self.pi.download(self.download_url, tmpdir)
        # if a local file/dir will not actually move it to tmpdir but will just return link
        # Make sure the file has been downloaded to the temp dir.
        if os.path.dirname(filepath) != tmpdir:
            basename = os.path.basename(filepath)
            dst = os.path.join(tmpdir, basename)
            if os.path.isdir(filepath):
                # TODO: if dst already exists check if the same in which case
                # we can avoid this
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(filepath, dst)
            else:
                from setuptools.command.easy_install import samefile
                if not samefile(filepath, dst):
                    shutil.copy2(filepath, dst)
            filepath=dst
        return filepath

    def unpack(self, dist_filename, extract_dir):
        if os.path.isfile(dist_filename) and not dist_filename.endswith('.py'):
            from setuptools.archive_util import unpack_archive
            unpack_archive(dist_filename, extract_dir)
            return extract_dir
        elif os.path.isdir(dist_filename):
            return os.path.abspath(dist_filename)

    def install(self, *args, **kwargs):
        '''Dispatch to same method on default L{Distribution}.'''
        return self.dist.install(*args, **kwargs)

    def write(self, *args, **kwargs):
        '''Dispatch to same method on default L{Distribution}.'''
        return self.dist.write(*args, **kwargs)

    def stream(self, *args, **kwargs):
        '''Dispatch to same method on default L{Distribution}.'''
        return self.dist.stream(*args, **kwargs)

    @classmethod
    def _default_distribution(self):
        import datapkg.distribution
        modpath, klassname = datapkg.distribution.default_distribution.split(':')
        mod = __import__(modpath, fromlist=['anyoldthing'])
        klass = getattr(mod, klassname)
        return klass
    
    def _dist_get(self):
        '''Get a L{Distribution} associated with this package.'''
        # TODO: cache the attribute
        klass = self._default_distribution()
        dist = klass(self)
        return dist

    dist = property(_dist_get)

    @classmethod
    def info_from_path(self, path):
        # will remove any trailing slash
        path = os.path.normpath(path)
        dir = os.path.dirname(path)
        name = os.path.basename(path)
        return dir, name

    @classmethod
    def create_on_disk(self, path, *args, **kwargs):
        '''Helper method to create distribution at path.

        Assumes path gives both package name (last part of path) and path to
        create at.
        
        Type of distribution to use determined by: `datapkg.distribution.default_distribution`

        args, kwargs as appropriate for write method on default distribution
        '''
        dir, name = self.info_from_path(path)
        pkg = Package(name)
        pkg.installed_path = path
        pkg.dist.write(*args, **kwargs)
        return pkg

    @classmethod
    def from_path(self, path):
        '''Load a L{Package} object from a path to a package distribution
        (assumed to be of type `default_distribution`).'''
        klass = self._default_distribution()
        dist = klass.from_path(path)
        return dist.package

    
