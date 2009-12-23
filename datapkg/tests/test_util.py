import platform
import os

from datapkg.tests.base import TestCase
import datapkg.util


def test_getstatusoutput():
    exp = 'Python %s' % platform.python_version()
    cmd = 'python -V'
    status, output = datapkg.util.getstatusoutput(cmd)
    assert output == exp


class TestPip(TestCase):
    @classmethod
    def setup_class(self):
        self.make_tmpdir()
        # now have self.tmpdir
        self.downloader = datapkg.util.Downloader(self.tmpdir)
        self.base_dir = self.downloader.base_dir

    def test_1_download_targz(self):
        test_url = 'http://knowledgeforge.net/ckan/datapkgdemo-0.1.tar.gz'

        self.downloader.download(test_url, unpack=False)
        dest = os.path.join(self.base_dir, 'datapkgdemo-0.1.tar.gz')
        assert os.path.exists(dest), dest

        self.downloader.download(test_url, unpack=True)
        dest = os.path.join(self.base_dir, 'datapkgdemo-0.1')
        assert os.path.exists(dest), dest

    # TODO: reinstate or selectively disable
    # slow, requires external access and hg
    def _test_2_download_hg(self):
        test_hg = 'hg+https://knowledgeforge.net/ckan/datapkg'
        dest = os.path.join(self.base_dir, 'datapkg')
        self.downloader.download(test_hg, unpack=False)
        assert os.path.exists(dest), dest

