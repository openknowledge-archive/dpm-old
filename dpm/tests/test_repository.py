import os
import tempfile
import shutil
from StringIO import StringIO

from dpm.tests.base import TestCase
import dpm.repository


class _TestFileRepository(TestCase):
    @classmethod
    def setup_class(self):
        self.make_tmpdir()
        self.init_path = os.path.join(self.tmpdir, '.dpm')

    def test_init(self):
        self.repo = dpm.repository.FileRepository(self.init_path)
        assert os.path.exists(self.init_path)

