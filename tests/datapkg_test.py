import os
import tempfile
import shutil

import datapkg

class TestTemplate:

    def setup_class(self):
        self.tmp = tempfile.mkdtemp()

    def teardown_class(self):
        shutil.rmtree(self.tmp)

    def test_1(self):
        name = 'annakarenina'
        datapkg.create(name=name, base_path=self.tmp)
        dest = os.path.join(self.tmp, name)
        assert os.path.exists(dest)
        setuppy = os.path.join(dest, 'setup.py')
        assert os.path.exists(setuppy)
