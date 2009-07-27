'''A `Distribution` is a serialization of a `Package` to disk.
''' 
import os

from datapkg import DatapkgException
from datapkg.package import Package
import datapkg.util

default_distribution = 'datapkg.distribution:PythonDistribution'

class DistributionBase(object):
    # distribution_type = None

    def __init__(self, package=None):
        self.package = package

#     def make_from_python_distribution():
#         pass
# 
#     def make_from_url():
#         pass


class PythonDistribution(DistributionBase):

    def write(self, template='default'):
        '''Write this distribution to disk at self.package.installed_path.
        '''
        # TODO: import PasteScript direct and use
        # use no-interactive to avoid querying on vars
        cmd = 'paster create --no-interactive --template=datapkg-%s ' % template
        base_path, xxx = Package.info_from_path(self.package.installed_path)
        if base_path:
            cmd += '--output-dir %s ' % base_path
        cmd += self.package.name
        # TODO: catch stdout and only print if error
        import commands
        # os.system(cmd)
        status, output = datapkg.util.getstatusoutput(cmd)
        if status:
            msg = 'Error on attempt to create file structure:\n\n%s' % output
            raise DatapkgException(msg)
        return self.package.installed_path

    @classmethod
    def from_path(self, path):
        '''Load a L{Package} object from a path to a package distribution.'''
        import datapkg.pypkgtools
        pydist = datapkg.pypkgtools.load_distribution(path)
        import datapkg.metadata as M
        metadata = M.MetadataConverter.from_distutils(pydist.metadata)
        pkg = Package(pydist.metadata.name, installed_path=unicode(path),
                metadata=metadata)
        dist = self(pkg)
        return dist

    def is_python_distribution(self, path):
        # taken from easy_install.install_item
        # could just have tried to install and caught exception
        dist_filename = path
        setup_base = path
        if dist_filename.lower().endswith('.egg'):
            return True
        elif dist_filename.lower().endswith('.exe'):
            return True
        setup_script = os.path.join(setup_base, 'setup.py')
        if os.path.exists(setup_script):
            return True
        return False

    def make_python_distribution(self, base_path, package_files):
        dist_path = self.create_file_structure(base_path)
        pypkg_inside_pkg_dir = os.path.join(dist_path, self.name)
        if os.path.isdir(package_files):
            for fn in os.listdir(package_files):
                path = os.path.join(package_files, fn)
                # TODO: move rather than copy?
                if os.path.isdir(path):
                    shutil.copytree(path, pypkg_inside_pkg_dir)
                else:
                    shutil.copy(path, pypkg_inside_pkg_dir)
        else:
            shutil.copy(package_files, pypkg_inside_pkg_dir)
        return dist_path

    def install(self, install_dir, local_path_to_package_files=None, **kwargs):
        dist_path = local_path_to_package_files
        import distutils.errors
        import tempfile
        # TODO: cleanup ...
        tmpdir = tempfile.mkdtemp('datapkg-')
        if not local_path_to_package_files:
            if self.download_url:
                dist_path = self.download(tmpdir)
            else:
                msg = 'No package files to install and no download url either'
                raise Exception(msg)

        # support case where what we have is not yet a python package
        extract_dir = os.path.join(tmpdir, 'extract')
        if not self.is_python_distribution(dist_path):
            dist_path = self.unpack(dist_path, extract_dir)
            if not self.is_python_distribution(dist_path):
                # this will create tmpdir/{self.name}
                # so need to be sure that download file not named self.name
                # to ensure no conflict when we do this
                dist_path = self.make_python_distribution(tmpdir, extract_dir)
        else:
            dist_path = local_path_to_package_files
        self.install_python_package(install_dir, dist_path, tmpdir, **kwargs)

    def install_python_package(self, install_dir, pkg_path, tmpdir,
            zip_safe=False):
        pydist = datapkg.pypkgtools.load_distribution(pkg_path)
        installed_path = pydist.install(install_dir, tmpdir, zip_safe)
        self.package.installed_path = installed_path
    
    def stream(self, path):
        # TODO: should move to using underlying pydist here ...
        import sys
        sys.path.insert(0, self.package.installed_path)
        import pkg_resources
        return pkg_resources.resource_stream(self.package.name, path)

