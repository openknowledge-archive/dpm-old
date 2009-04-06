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

    def init_on_load(self, metadata=None, **kwargs):
        if metadata:
            self.metadata = metadata
        else:
            self.metadata = datapkg.metadata.Metadata()
            self.metadata['name'] = self.name
        # TODO: most of these attributes should run off metadata
        self.download_url = None
        for k,v in kwargs.items():
            setattr(self, k, v)

    def _normalize_name(self, name):
        new_name = name.lower()
        regex = r'^[\w-]+$'
        if not re.match(regex, new_name):
            msg = 'Invalid package name: %s' % name
            raise ValueError(msg)
        return unicode(new_name)

    def create_file_structure(self, base_path='', template='default'):
        '''Create a skeleton data package on disk.
        '''
        # TODO: import PasteScript direct and use
        # use no-interactive to avoid querying on vars
        cmd = 'paster create --no-interactive --template=datapkg-%s ' % template
        if base_path:
            cmd += '--output-dir %s ' % base_path
        cmd += self.name
        dist_path = os.path.join(os.path.abspath(base_path), self.name)
        # TODO: catch stdout and only print if error
        import commands
        # os.system(cmd)
        status, output = datapkg.util.getstatusoutput(cmd)
        if status:
            msg = 'Error on attempt to create file structure:\n\n%s' % output
            raise DatapkgException(msg)
        return dist_path

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

    def is_python_package(self, path):
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

    def unpack(self, dist_filename, extract_dir):
        if os.path.isfile(dist_filename) and not dist_filename.endswith('.py'):
            from setuptools.archive_util import unpack_archive
            unpack_archive(dist_filename, extract_dir)
            return extract_dir
        elif os.path.isdir(dist_filename):
            return os.path.abspath(dist_filename)

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
        if not self.is_python_package(dist_path):
            dist_path = self.unpack(dist_path, extract_dir)
            if not self.is_python_package(dist_path):
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
        self.installed_path = pydist.install(install_dir, tmpdir, zip_safe)
    
    @classmethod
    def from_path(self, path):
        '''Load a L{Package} object from a path to a package distribution.'''
        import datapkg.pypkgtools
        pydist = datapkg.pypkgtools.load_distribution(path)
        import datapkg.metadata as M
        metadata = M.MetadataConverter.from_distutils(pydist.metadata)
        pkg = Package(pydist.metadata.name, installed_path=unicode(path),
                metadata=metadata)
        return pkg

    def stream(self, path):
        # TODO: should move to using underlying pydist here ...
        import sys
        sys.path.insert(0, self.installed_path)
        import pkg_resources
        return pkg_resources.resource_stream(self.name, path)


class PackageMaker(object):
    '''Helper class for making Packages.
    '''

    def make_from_python_distribution():
        pass

    def make_from_url():
        pass

    @classmethod
    def info_from_path(self, path):
        # will remove any trailing slash
        path = os.path.normpath(path)
        dir = os.path.dirname(path)
        name = os.path.basename(path)
        return dir, name

    @classmethod
    def create_on_disk(self, path, template='default'):
        dir, name = self.info_from_path(path)
        pkg = Package(name)
        pkg.create_file_structure(dir, template)
        return pkg


import datapkg.db as db
db.mapper(Package, db.package_table, extension=db.ReconstituteExtension())

