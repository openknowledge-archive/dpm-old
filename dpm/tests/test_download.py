import os

from dpm.tests.base import TestCase
import zipfile
import dpm.download
import dpm.package


class TestPackageDownloader(TestCase):
    @classmethod
    def setup_class(self):
        ## will now have self.tmpdir
        self.make_tmpdir()
        self.downloader = dpm.download.PackageDownloader(verbose=True)

        ## create resources
        indata_dir = os.path.join(self.tmpdir, 'indata')
        os.makedirs(indata_dir)
        self.csv = os.path.join(indata_dir, 'my.csv')
        fo = open(self.csv, 'w')
        fo.write('testing,xyz')
        fo.close()
        ## zipfile
        self.zipped_csv = os.path.join(indata_dir, 'myzip.zip')
        zipfo = zipfile.ZipFile(self.zipped_csv, 'w')
        ## weirdly have to have some path prefix to my.csv for this to work!
        zipfo.write(self.csv, '/xxx/my.csv')
        zipfo.close()

        self.pkg = dpm.package.Package(name='mytestpkg')
        self.pkg.resources = [
                {'url': 'file://%s' % self.csv, 'format': 'csv'}
                ]
        self.dest_dir = os.path.join(self.tmpdir, 'download')
        self.pkg2 = dpm.package.Package(name='mytestpkg2')
        self.pkg2.resources = [
                {'url': 'file://%s' % self.csv, 'format': 'csv'},
                {'url': 'file://%s' % self.zipped_csv, 'format': 'dpm/zip'}
                ]

    def test_01_download(self):
        ourdest = os.path.join(self.dest_dir, self.pkg.name)
        out = self.downloader.download(self.pkg, ourdest)
        dest = os.path.join(ourdest, 'datapackage.json')
        assert os.path.exists(dest), dest
        dest = os.path.join(ourdest, 'my.csv')
        assert os.path.exists(dest), dest

    def test_02_download_with_multiple_resources(self):
        ourdest = os.path.join(self.dest_dir, self.pkg2.name)
        filterfunc = lambda x,y: x.get('format', '').startswith('dpm')
        out = self.downloader.download(self.pkg2, ourdest, filterfunc)
        dest = os.path.join(ourdest, 'myzip.zip')
        assert os.path.exists(dest), dest
        dest = os.path.join(ourdest, 'my.csv')
        assert not os.path.exists(dest), dest

