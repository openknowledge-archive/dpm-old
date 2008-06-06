import os
import commands
import tempfile
import shutil

class TestCLI:

    @classmethod
    def setup_class(self):
        self.tmp = tempfile.mkdtemp()
        self.cwd = os.getcwd()

    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.tmp)
        # reset cwd or problems in other tests
        os.chdir(self.cwd)

    def test_about(self):
        cmd = 'datapkg about'
        status, output = commands.getstatusoutput(cmd)
        exp = 'datapkg version'
        assert exp in output

    def test_create(self):
        name = 'mytest'
        os.chdir(self.tmp)
        cmd = 'datapkg create ' + name
        status, output = commands.getstatusoutput(cmd)
        print output
        assert not status
        dest = os.path.join(self.tmp, name)
        assert os.path.exists(dest)

