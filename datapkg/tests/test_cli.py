import os
import commands
import tempfile
import shutil

import datapkg.util
import datapkg.repository

class TestCLI:

    @classmethod
    def setup_class(self):
        self.tmp_base = tempfile.gettempdir()
        self.tmpdir = os.path.join(self.tmp_base, 'datapkg-test-cli')
        self.repo_path = os.path.join(self.tmpdir, '.datapkg')
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        os.makedirs(self.tmpdir)
        self.cwd = os.getcwd()
        self.cmd_base = 'datapkg --repository %s ' % self.repo_path

    @classmethod
    def teardown_class(self):
        # reset cwd or problems in other tests
        os.chdir(self.cwd)

    def test_about(self):
        cmd = 'datapkg about'
        status, output = commands.getstatusoutput(cmd)
        exp = 'datapkg version'
        assert exp in output

    def test_walkthrough(self):
        # from beginning to end ...
        pkg_name = 'mytestpkg'

        # init
        cmd = self.cmd_base + 'init'
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert os.path.exists(self.repo_path)

        # create 
        pkg_path = os.path.join(self.tmpdir, pkg_name)
        cmd = self.cmd_base + 'create %s' % pkg_path
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert os.path.exists(pkg_path)

        # register + install
        cmd = self.cmd_base + 'register %s' % pkg_path 
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output

        # repo = datapkg.repository.Repository(self.repo_path)
        # pkgnames = [ pkg.name for pkg in repo.index.list_packages() ]
        # assert pkg_name in pkgnames

        # cmd = self.cmd_base + 'install %s' % pkg_path 
        # status, output = datapkg.util.getstatusoutput(cmd)
        # assert not status, output
