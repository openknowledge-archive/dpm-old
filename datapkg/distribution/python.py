import os

from datapkg.package import Package
import datapkg.metadata as M
from base import DistributionBase

class PythonDistribution(DistributionBase):
    '''Datapkg distribution based on python distribution format (based on
    setuptools).

    File layout::

        {dist-path}/setup.py
            # as per standard python approach main 'metadata' goes in python
            # setup.py file with key/value arguments to setup method.

        {dist-path}/MANIFEST.in
            # manifest template specifying rules for what files to include in
            # the distribution. For details see:
            # http://docs.python.org/distutils/sourcedist.html#the-manifest-in-template
            # NB: If you want to explicitly list every file you can create a
            # MANIFEST file.

        {dist-path}/{pkgname}/...

            # Data (and code) files. For python to pick up files correctly
            # they should be in subdirectory named after the package or
            # subdirectories thereof (e.g. {pkgname}/data
    '''

    # TODO: write should write out package metadata ...
    def write(self, path, template='default'):
        '''See parent.

        @param template: paster template to use
        '''
        dest = path
        if os.path.exists(path):
            raise Exception('Destination path already exists: %s' % dest)
        # python has package dir inside distribution dir
        pkgdir = os.path.join(dest, self.package.name)
        os.makedirs(pkgdir)
        fo = open(os.path.join(pkgdir, '__init__.py'), 'w')
        fo.write('')
        fo.close()
        setuppy = '''from setuptools import setup, find_packages

setup(
    name='%(name)s',
    version=0.1,
    # Name of License for your project
    # Suitable open licenses can be found at http://www.opendefinition.org/licenses/
    license='',

    # Title or one-line description of the package
    description='',

    # URL of project/package homepage
    url='',

    # Download url for this package if it has a specific location
    # download_url='',

    # Comma-separated keywords/tags
    keywords='',

    # Notes or multi-line description for your project (in markdown)
    long_description="""\n""",

    author='',
    author_email='',

    ###########################
    ## Ignore from here onwards

    packages=find_packages(),
    include_package_data=True,
    # do not zip up the package into an 'Egg'
    zip_safe=False,
)

'''
        manifest = '''# Follows python MANIFEST.in syntax. See datapkg man for more details
recursive-include %s *.txt *.csv *.js *.dat
''' % self.package.name
        manifestpath = os.path.join(dest, 'MANIFEST.in')
        setuppypath = os.path.join(dest, 'setup.py')
        fo = open(manifestpath, 'w')
        fo.write(manifest)
        fo = open(setuppypath, 'w')
        fo.write(setuppy % self.package.metadata)
        return dest

    @classmethod
    def load(self, path):
        '''Load a L{Package} object from a path to a package distribution.'''
        import datapkg.pypkgtools
        pydist = datapkg.pypkgtools.load_distribution(path)
        metadata = M.MetadataConverter.from_distutils(pydist.metadata)
        pkg = Package(name=pydist.metadata.name, installed_path=unicode(path))
        pkg.update_metadata(metadata)
        pkg.manifest = dict([ (x,None) for x in pydist.filelist])
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
        import datapkg.pypkgtools
        pydist = datapkg.pypkgtools.load_distribution(pkg_path)
        installed_path = pydist.install(install_dir, tmpdir, zip_safe)
        self.package.installed_path = installed_path
    
    def stream(self, path):
        # TODO: should move to using underlying pydist here ...
        import sys
        sys.path.insert(0, self.package.installed_path)
        import pkg_resources
        return pkg_resources.resource_stream(self.package.name, path)



