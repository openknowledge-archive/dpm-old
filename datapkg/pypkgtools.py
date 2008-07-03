import setuptools
import setuptools.dist
import zipimport, os
from pkg_resources import PathMetadata, EggMetadata
from pkg_resources import Distribution

class PyPkgTools(object):

    def load_metadata(self, pkg_path):
        setuppy = os.path.join(pkg_path, 'setup.py')
        if os.path.exists(setuppy):
            import distutils.core
            dist = distutils.core.run_setup(setuppy, stop_after='init')
            return dist.metadata

        # must be an egg distribution
        # Follows setuptools.command.easy_install.easy_install.egg_distribution.
        if os.path.isdir(pkg_path):
            metadata_finder = PathMetadata(pkg_path,os.path.join(pkg_path,'EGG-INFO'))
        else:
            metadata_finder = EggMetadata(zipimport.zipimporter(pkg_path))
        # dist = Distribution.from_filename(egg_path,metadata=metadata_finder)
        pkg_info = StringIO.StringIO(metadata_finder.get_metadata('PKG-INFO'))

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



