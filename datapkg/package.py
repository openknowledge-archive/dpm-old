import os
from StringIO import StringIO
import urllib
from zipfile import ZipFile

class BasePackage(object):
    type = 'none'

    def __init__(self, name, **kwargs):
        self.name = name
        self.version = '0.0'
        self.installed = False
        for k,v in kwargs.items():
            setattr(self, k, v)

    def install(self, cache_path=None):
        raise NotImplementedError()

    def resource_stream(self, path):
        raise NotImplementedError()


class PackagePlain(BasePackage):
    type = 'plain'

    def install(self, cache_path=None):
        '''
        TODO support other download types than zip

        Maybe can use distutils.install_data here?
        '''

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

import os
import shutil
import setuptools.package_index as pi
import setuptools.command.easy_install
import setuptools.archive_util
class PackageFull(BasePackage):
    type = 'full'
    def __init__(self, name, **kwargs):
        super(PackageFull, self).__init__(name, **kwargs)
        self.pi = pi.PackageIndex('http://random.url/')
        import setuptools.dist
        tdist = setuptools.dist.Distribution()
        self.easy_install = setuptools.command.easy_install.easy_install(tdist)

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
        dist_filename = path
        setup_base = path
        # taken from easy_install.install_item
        # could just have tried to install
        # install_needed = True
        # deps = False
        # self.easy_install.install_item(None, path, tmpdir,
        #        deps, install_needed)
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
    
    def make_into_python_package(self, path):
        fo = open(os.path.join(path, 'setup.py'), 'w')
        setup_dot_py = \
'''from setuptools import setup

setup(
    name='%s',
    version='%s',
    )

''' % ( self.name, self.version)
        fo.write(setup_dot_py)
        fo.close()

        manifest = os.path.join(path, 'MANIFEST.in')
        if not os.path.exists(manifest):
            fo = open(manifest, 'w')
            fo.write('recursive-include * *\n')
            fo.write('include *.*\n')
            # TODO: exclude stuff such build?
            fo.close()

    def install(self, install_dir, cached_path=None):
        import distutils.errors
        import tempfile
        # TODO: cleanup ...
        tmpdir = tempfile.mkdtemp('datapkg-')
        extract_dir = tempfile.mkdtemp('datapkg-')
        if not cached_path:
            cached_path = self.download(tmpdir)

        if not self.is_python_package(cached_path):
            setup_base = self.unpack(cached_path, extract_dir)
            if not self.is_python_package(setup_base):
                self.make_into_python_package(setup_base)
        else:
            setup_base = cached_path

        # emulate
        # cmd = 'easy_install --multi-version --install-dir %s %s' % (install_dir, setup_base)
        # os.system(cmd)
        self.easy_install.install_dir = install_dir
        self.easy_install.multi_version = True
        # hack to make finalize_options happy
        self.easy_install.args = True
        self.easy_install.finalize_options()
        install_needed = True
        deps = False
        self.easy_install.install_item(None, setup_base, tmpdir,
            deps, install_needed)
        # except setuptools.archive_util.UnrecognizedFormat:
        #    raise 'You have not provided a recognized file format.'


class PackagePython(BasePackage):

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


