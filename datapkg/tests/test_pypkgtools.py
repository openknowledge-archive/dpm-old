import os
import shutil

from datapkg.pypkgtools import PyPkgTools
from datapkg.tests.base import TestCase
from datapkg.package import Package

class TestPyPkgTools(TestCase):

    pkg_name = 'testpypkgtools'
    base_path = '/tmp/pypkgtools-testing'
    pkg_path = os.path.join(base_path, pkg_name)

    def setUp(self):
        self.pypkgtools = PyPkgTools()
        if os.path.exists(self.base_path):
            shutil.rmtree(self.base_path)
        self.pkg = Package(self.pkg_name)
        self.pkg.create_file_structure(self.base_path)

    def test_load_metadata_from_source(self):
        meta = self.pypkgtools.load_metadata(self.pkg_path)
        assert meta
        assert meta.name == self.pkg_name
        # note that get_* will return something different from direct access
        assert meta.download_url == None, meta.download_url

    def test_parse_pkg_info(self):
        pkg_info_path = os.path.join(self.pkg_path, self.pkg_name + '.egg-info',
                'PKG-INFO')
        meta = self.pypkgtools.parse_pkg_info(file(pkg_info_path))
        assert meta.name == self.pkg_name
        assert meta.version == '0.0.0'

    def test_load_metadata_from_egg(self):
        # TODO
        # how do we find some nice egg on disk?
        # os.system('python setup.py egg_dist')
        pass

    def test_read_pkg_name(self):
        pkg_name = self.pypkgtools.read_pkg_name(self.pkg_path)
        assert pkg_name == self.pkg_name, pkg_name

from datapkg.pypkgtools import DistributionOnDisk
class TestDistributionOnDisk(TestCase):

    def setUp(self):
        self.make_tmpdir()
        import datapkg.package
        self.pkgname = 'abc'
        self.srcdir = os.path.join(self.tmpdir, self.pkgname)
        self.pkg = datapkg.package.PackageMaker.create_on_disk(self.srcdir)
        self.pkg.install(self.tmpdir, self.srcdir)
        self.pkg_path = self.pkg.installed_path

    def test_metadata(self):
        dist = DistributionOnDisk(self.pkg_path)
        assert dist.metadata.name == self.pkgname

    # encountering that weird error on second run of setUp when installing an
    # egg (even though completely torn down)
    def _test_listdir(self):
        dist = DistributionOnDisk(self.pkg_path)
        out = dist.listdir('.')
        
