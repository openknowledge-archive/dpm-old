import os
import shutil

from datapkg.tests.base import TestCase
import datapkg.pypkgtools
from datapkg.package import Package
import datapkg.distribution


class TestDistributionOnDisk(TestCase):
    # dist_type = datapkg.pypkgtools.DistributionOnDiskEggUnpacked

    # have to use a class method to avoid weird easy_install setup.py error
    @classmethod
    def setup_class(self):
        self.make_tmpdir()
        import datapkg.package
        self.pkgname = 'xxxyyy'
        self.srcdir = os.path.join(self.tmpdir, self.pkgname)
        self.pkg = Package(name=self.pkgname)
        self.dist = datapkg.distribution.PythonDistribution(self.pkg)
        self.dist.write(self.srcdir)
        self.offset = os.path.join(self.pkgname, 'info.txt')
        pkg_pkg_path = os.path.join(self.srcdir, self.offset)
        f = open(pkg_pkg_path, 'w')
        self.content = 'Ideas are cheap, implementation is costly'
        f.write(self.content)
        f.close()
        self.rawsrcdir = os.path.join(self.tmpdir, 'rawsrc')
        shutil.copytree(self.srcdir, self.rawsrcdir)
        # behind the scenes this is actually using distribution which could
        # create some circularity
        self.dist.install(self.tmpdir, self.srcdir)
        self.installed_pkg_path = self.pkg.installed_path

    def test_egg_unpacked(self):
        dist = datapkg.pypkgtools.DistributionOnDiskEggUnpacked(self.installed_pkg_path)
        self._run_tests(dist)

    def test_raw_source(self):
        dist = datapkg.pypkgtools.DistributionOnDiskRawSource(self.rawsrcdir)
        self._run_tests(dist)

    def test_egg_source(self):
        dist = datapkg.pypkgtools.DistributionOnDiskEggSource(self.srcdir)
        self._run_tests(dist)

    def _run_tests(self, dist):
        self._test_metadata(dist)
        self._test_pkg_name(dist)
        self._test_listdir(dist)
        self._test_resource_stream(dist)
        self._test_filelist(dist)

    def _test_pkg_name(self, dist):
        assert dist.name == self.pkgname, dist.name

    def _test_metadata(self, dist):
        assert dist.metadata.name == self.pkgname
        assert dist.metadata.download_url == None
        assert dist.metadata.keywords == '' or dist.metadata.keywords is None, dist.metadata.keywords
        # TODO: why does this fail?
        # assert dist.metadata.version == '0.0.0', dist.metadata.version

    def _test_listdir(self, dist):
        out = dist.listdir('.')
        assert 'xxxyyy' in out
        # will vary across types
        assert len(out) >= 2

    def _test_resource_stream(self, dist):
        fo = dist.resource_stream(self.offset)
        out = fo.read()
        assert out == self.content, out
    
    def _test_filelist(self, dist):
        assert 'xxxyyy/info.txt' in dist.filelist, dist.filelist


# encountering that weird error on any subsequent run of setup_lass
# related to installing an egg ...
#class TestDistributionOnDiskRawSource(TestDistributionOnDisk):
#    dist_type = datapkg.pypkgtools.DistributionOnDiskRawSource
#
#    def setUp(self):
#        self.pkg_path = self.rawsrcdir
#
#class TestDistributionOnDiskEggSource(TestDistributionOnDisk):
#    dist_type = datapkg.pypkgtools.DistributionOnDiskEgg
#    def setUp(self):
#        self.pkg_path = self.srcdir

