import os

from dpm.tests.base import TestCase
import dpm
import dpm.upload


class TestUploader(TestCase):
    @classmethod
    def setup_class(self):
        ## will now have self.tmpdir
        self.make_tmpdir()
        self.uploader = dpm.upload.Uploader(verbose=True)

        ## create resources
        indata_dir = os.path.join(self.tmpdir, 'indata')
        os.makedirs(indata_dir)
        self.csv = os.path.join(indata_dir, 'my.csv')
        fo = open(self.csv, 'w')
        fo.write('testing,xyz')
        fo.close()

        self.destdir = os.path.join(self.tmpdir, 'dest')
        # pairtree needs a clean (uncreated) dir
        # os.makedirs(self.destdir)
        section = 'upload:mypairtree'
        dpm.CONFIG.add_section(section)
        dpm.CONFIG.set(section, 'ofs.backend', 'pairtree')
        dpm.CONFIG.set(section, 'storage_dir', self.destdir)

    def test_01_bucket_label(self):
        destspec = 'mypairtree://mybucket/mylabel.csv'
        bucket, label = self.uploader.get_bucket_label(destspec)
        assert bucket == 'mybucket'
        assert label == 'mylabel.csv'

    # TODO: re-enable (2011-11-18)
    # Disabling as requires ofs and pairtree installed
    # Plus upload is not that important/functional atm
    def test_02_upload(self):
        destspec = 'mypairtree://mybucket/mylabel.csv'
        self.uploader.upload(self.csv, destspec)
        destpath = os.path.join(self.destdir, 'pairtree_root', 'my', 'bu',
                'ck', 'et', 'obj', 'mylabel.csv')
        assert os.path.exists(destpath)

