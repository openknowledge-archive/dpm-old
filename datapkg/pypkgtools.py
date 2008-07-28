'''

General Remarks on Setuptools Etc
=================================

PkgResources and Setuptools can be difficult for the uninitiated to grapple
with.

Things are also made a little confusingly by different objects having the same
or similar names. For example a pkg_resources Distribution object is very
different from a setuptools.core.Distribution object (which is like the
distutils one).

Also rather confusingly PkgResources ends up making its metadata objects into
providers (i.e. a provider *has* metadata but simultaneously metadata isa
provider ...).

Similarly, behind the scenes in pkg_resources a Distribution delegates all main
functionality to its associated provider/metadata object. Furthermore, a
metadata object is not actually metadata itself but a pointer to a collection
of metadata directories and files.
'''
import setuptools
import setuptools.dist
import zipimport, os
import StringIO

class PyPkgTools(object):

    def load_metadata(self, pkg_path):
        '''Get metadata from a setup.py file.'''
        setuppy = os.path.join(pkg_path, 'setup.py')
        if os.path.exists(setuppy):
            import distutils.core
            dist = distutils.core.run_setup(setuppy, stop_after='init')
            return dist.metadata

    def parse_pkg_info(self, fileobj):
        '''Parse PKG-INFO fileobj and return DistributionMetadata object.
        
        task is to invert distutils.dist.DistributionMetadata.write_pkg_file
        '''
        # partially based on
        # http://mail.python.org/pipermail/distutils-sig/2007-June/007783.html
        from distutils.dist import DistributionMetadata
        metadata = DistributionMetadata()
        fields = metadata._METHOD_BASENAMES

        import rfc822
        messages=rfc822.Message(fileobj)
        print messages.items()
        for field in fields:
            if field in ['home_page','author_email']:
                prop=field.replace('_','-')
            else:
                prop=field
            value=messages.getheader(prop)
            # TODO: do this properly
            # need to invert metadata._write_list
            setattr(metadata, field, value)
        return metadata

    def read_pkg_name(self, path):
        metadata = self.load_metadata(path)
        return metadata.name


import pkg_resources
class DistributionOnDisk(object):
    '''Wrap a standard Python distribution on disk.

    In essence this is a wrapper around pkg_resources.Distribution object.

    To get at basic metadata (i.e. what is found in PKG-INFO) call .metadata.
    '''

    def __init__(self, dist_path):
        self.dist_path = dist_path
        self.pkgr_metadata = self._load_pkgr_metadata()
        self.pkgr_dist = pkg_resources.Distribution.from_filename(self.dist_path,
                metadata=self.pkgr_metadata)
        self.metadata = self._get_metadata(self.pkgr_metadata)

    def _load_pkgr_metadata(self):
        # 3 options:
        # A.1: built distribution zipped
        # A.2: built distbn unzipped
        # B: a development/unbuilt distribution
        # Issue with B is that we do need egg-info directory to exist
        # (seemingly cannot just work off setup.py ...)

        built_egg_info = os.path.join(self.dist_path, 'EGG-INFO')
        if not os.path.isdir(self.dist_path): # A.1
            metadata_finder = pkg_resources.EggMetadata(zipimport.zipimporter(self.dist_path))
        elif os.path.exists(built_egg_info): # A.2
            metadata_finder = pkg_resources.PathMetadata(self.dist_path, built_egg_info)
        else:
            egginfos = filter(lambda x: x.endswith('.egg-info'),
                    os.listdir(self.dist_path))
            if not len(egginfos) > 0:
                msg = 'Cannot load Distribution as no *.egg-info file found at %s' % self.dist_path
                raise ValueError(msg)
            # take first one
            egg_info = os.path.join(self.dist_path, egginfos[0])
            metadata_finder = pkg_resources.PathMetadata(self.dist_path, egg_info)
            # dist = Distribution(self.dist_path, metadata=metadata)
        return  metadata_finder

    def _get_metadata(self, pkgr_metadata):
        toolset = PyPkgTools()
        pkg_info = StringIO.StringIO(pkgr_metadata.get_metadata('PKG-INFO'))
        return toolset.parse_pkg_info(pkg_info)

    def listdir(self, path):
        return self.pkgr_dist.resource_listdir(path)

