import os
import shutil
from StringIO import StringIO
import urllib
import re
import distutils.dist

import dpm.metadata
from dpm import DatapkgException

def normalize_name(name):
    new_name = name.lower()
    regex = r'^[\w-]+$'
    if not re.match(regex, new_name):
        msg = 'Invalid package name: %s' % name
        raise ValueError(msg)
    return unicode(new_name)

class Manifest(dict):
    '''A package manifest, i.e. a list of resources the package provides.

    At present a simple dictionary keyed by file pathes.

    # TODO: use an ordered dictionary (waiting until available in standard
    # python distribution.)
    '''
    pass


## TODO: do we want to normalize name?
class Package(object):
    '''A knowledge (data or content) 'package'.

    It combines metadata with a manifest listing the material contained in this
    package.

    If it has an associated distribution then this material will be directly
    accessible. 
    '''
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)

    def init_on_load(self, **kwargs):
        '''Additional __init__ method.
        
        Separated out from __init__ for the benefit of sqlalchemy
        '''
        # TODO: rename to something like path_on_disk
        # path to distribution on disk associated to package (if any)
        self.installed_path = None
        self.manifest = Manifest()
        for k,v in kwargs.items():
            setattr(self, k, v)
        for k in dpm.metadata.Metadata.key_list:
            if not hasattr(self, k):
                setattr(self, k, dpm.metadata.Metadata.defaults.get(k, u''))

    def _get_metadata(self):
        return dpm.metadata.Metadata([ (k,getattr(self,k)) for k in
            dpm.metadata.Metadata.key_list ])
    
    metadata = property(_get_metadata)

    manager_metadata_keylist = ['installed_path']
    def _get_manager_metadata(self):
        out = [ (k,getattr(self,k)) for k in
             self.manager_metadata_keylist]
        return dict(out)
    manager_metadata = property(_get_manager_metadata)

    def update_metadata(self, metadata):
        for k,v in metadata.items():
            setattr(self, k, v)

    def _path_set(self, v):
        self.installed_path = v
    # TODO: rename installed path to path
    path = property(lambda self: self.installed_path, _path_set)

# TODO: remove (out of date as of 2010-04-09)
#     def download(self, tmpdir):
#         filepath = self.pi.download(self.download_url, tmpdir)
#         # if a local file/dir will not actually move it to tmpdir but will just return link
#         # Make sure the file has been downloaded to the temp dir.
#         if os.path.dirname(filepath) != tmpdir:
#             basename = os.path.basename(filepath)
#             dst = os.path.join(tmpdir, basename)
#             if os.path.isdir(filepath):
#                 # TODO: if dst already exists check if the same in which case
#                 # we can avoid this
#                 if os.path.exists(dst):
#                     shutil.rmtree(dst)
#                 shutil.copytree(filepath, dst)
#             else:
#                 from setuptools.command.easy_install import samefile
#                 if not samefile(filepath, dst):
#                     shutil.copy2(filepath, dst)
#             filepath=dst
#         return filepath
# 
#     def unpack(self, dist_filename, extract_dir):
#         if os.path.isfile(dist_filename) and not dist_filename.endswith('.py'):
#             from setuptools.archive_util import unpack_archive
#             unpack_archive(dist_filename, extract_dir)
#             return extract_dir
#         elif os.path.isdir(dist_filename):
#             return os.path.abspath(dist_filename)

    def install(self, *args, **kwargs):
        '''Dispatch to same method on default L{Distribution}.'''
        return self.dist.install(*args, **kwargs)

    # TODO: deprecate this
    def write(self, *args, **kwargs):
        '''Dispatch to same method on default L{Distribution}.'''
        return self.dist.write(*args, **kwargs)

    def stream(self, *args, **kwargs):
        '''Dispatch to same method on default L{Distribution}.'''
        return self.dist.stream(*args, **kwargs)

    def _dist_get(self):
        '''Get a L{Distribution} associated with this package.'''
        import dpm.distribution
        klass = dpm.distribution.default_distribution()
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
    def create_on_disk(self, path, **kwargs):
        '''Helper method to create distribution at path.

        Assumes path gives both package name (last part of path) and path to
        create at.
        
        Type of distribution to use determined by: `dpm.distribution.default_distribution`

        args, kwargs as appropriate for write method on default distribution
        '''
        dir, name = self.info_from_path(path)
        pkg = Package(name=name)
        pkg.installed_path = path
        pkg.dist.write(path, **kwargs)
        return pkg

    @classmethod
    def load(self, path):
        '''Load a L{Package} object from a path to a package distribution.'''
        import dpm.distribution
        dist = dpm.distribution.load(path)
        # TODO: should we be recording the distribution type or something for
        # future stuff ...
        return dist.package

    def __str__(self):
        repr = 'Package'
        for key in dpm.metadata.Metadata.key_list:
            repr += ' %s: %s' % (key, getattr(self,key))
        return repr
    
    def pretty_print(self):
        repr = ''
        for key in dpm.metadata.Metadata.key_list:
            repr += '%s: %s\n' % (key, getattr(self,key))
        return repr

