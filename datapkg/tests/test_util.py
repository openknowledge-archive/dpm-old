import platform
import os
import urllib
import zipfile

from datapkg.tests.base import TestCase
import datapkg.util


def test_getstatusoutput():
    exp = 'Python %s' % platform.python_version()
    cmd = 'python -V'
    status, output = datapkg.util.getstatusoutput(cmd)
    assert output == exp


class TestDownloader(TestCase):
    @classmethod
    def setup_class(self):
        # will now have self.tmpdir
        self.make_tmpdir()
        self.downloader = datapkg.util.Downloader(self.tmpdir)
        self.base_dir = self.downloader.base_dir
        indata_dir = os.path.join(self.tmpdir, 'indata')
        os.makedirs(indata_dir)
        self.csv = os.path.join(indata_dir, 'my.csv')
        fo = open(self.csv, 'w')
        fo.write('testing,xyz')
        fo.close()
        self.zipped_csv = os.path.join(indata_dir, 'myzip.zip')
        zipfo = zipfile.ZipFile(self.zipped_csv, 'w')
        # weirdly have to have some path prefix to my.csv for this to work!
        zipfo.write(self.csv, '/xxx/my.csv')
        zipfo.close()

    def test_1_download_csv(self):
        url = 'file://' + urllib.pathname2url(self.csv)
        out = self.downloader.download(url, copy_local=True)
        print out
        dest = os.path.join(self.base_dir, 'my.csv')
        assert os.path.exists(dest), dest

    def test_2_download_simple_zip(self):
        url = 'file://' + urllib.pathname2url(self.zipped_csv)
        self.downloader.download(url, copy_local=True)
        dest = os.path.join(self.base_dir, 'myzip.zip')
        # unpack case
        # dest = os.path.join(self.base_dir, 'myzip', 'my.csv')
        assert os.path.exists(dest), dest

    # requires external access
    # TODO: selectively disable ...
    def test_3_download_targz(self):
        test_url = 'http://knowledgeforge.net/ckan/datapkgdemo-0.1.tar.gz'

        self.downloader.download(test_url)
        dest = os.path.join(self.base_dir, 'datapkgdemo-0.1.tar.gz')
        assert os.path.exists(dest), dest

        # TODO: reinstate unpacking stuff
        # self.downloader.download(test_url, unpack=True)
        # dest = os.path.join(self.base_dir, 'datapkgdemo-0.1')
        # assert os.path.exists(dest), dest

    # slow, requires external access and hg
    # rgrp 2010-01-31: no longer working since switch to urlgrabber but leave
    # as may be reinstated in future
    def _test_2_download_hg(self):
        test_hg = 'hg+https://knowledgeforge.net/ckan/datapkg'
        dest = os.path.join(self.base_dir, 'datapkg')
        self.downloader.download(test_hg, unpack=False)
        assert os.path.exists(dest), dest

