import os
import tempfile
import shutil

import datapkg
import datapkg.cli

class TestTemplate:

    @classmethod
    def setup_class(self):
        self.tmp = tempfile.mkdtemp()

    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.tmp)

    def test_create(self):
        name = 'annakarenina'
        datapkg.create(name=name, base_path=self.tmp)
        dest = os.path.join(self.tmp, name)
        assert os.path.exists(dest)
        setuppy = os.path.join(dest, 'setup.py')
        assert os.path.exists(setuppy)

#     def test_full_walkthrough(self):
#         cmd = datapkg.cli
#         cmd.init()
#         default = 'default_name'
#         # cmd.install(default)
