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

        # from beginning to end ...
        self.pkg_name = u'mytestpkg'
        self.pkg_path = os.path.join(self.tmpdir, self.pkg_name)

    @classmethod
    def teardown_class(self):
        # do not teardown directory in order to allow investigation on error
        # reset cwd or problems in other tests
        os.chdir(self.cwd)

    def test_about(self):
        cmd = 'datapkg about'
        status, output = commands.getstatusoutput(cmd)
        exp = 'datapkg version'
        assert exp in output

    def _test_create(self):
        cmd = self.cmd_base + 'create %s' % self.pkg_path
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert os.path.exists(self.pkg_path)
        fp = os.path.join(self.pkg_path, self.pkg_name, 'abc.txt')
        fo = open(fp, 'w')
        fo.write('Ideas are cheap, implementation is costly.')
        fo.close()

    def test_walkthrough(self):

        # init
        cmd = self.cmd_base + 'repo init'
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert os.path.exists(self.repo_path)

        # create 
        self._test_create()

        # register
        cmd = self.cmd_base + 'register %s' % self.pkg_path 
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output

        repo = datapkg.repository.Repository(self.repo_path)
        pkgnames = [ pkg.name for pkg in repo.index.list() ]
        assert self.pkg_name in pkgnames

        # install
        cmd = self.cmd_base + 'install %s' % self.pkg_path 
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        # dest path with be self.pkg_name-version-*
        dirs = os.listdir(repo.installed_path)
        filtered = filter(lambda x: x.startswith(self.pkg_name), dirs)
        assert len(filtered) > 0, dirs

        # info
        # A: from self.pkg_name
        cmd = self.cmd_base + 'info %s' % self.pkg_name
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert self.pkg_name in output, output

        # TODO B: from disk

        # inspect - not yet implemented
        # cmd = self.cmd_base + 'inspect %s' % self.pkg_name
        # status, output = datapkg.util.getstatusoutput(cmd)
        # assert not status, output

        # dump
        offset = 'abc.txt'
        cmd = self.cmd_base + 'dump %s %s' % (self.pkg_name, offset)
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
    
    # For this need dummy ckan running locally with standard test data

    def test_ckan(self):
        localckan = 'http://localhost:5000/api/rest'
        apikey = 'tester'
        ckanbase = 'datapkg --repository %s ' % localckan
        ckanbase += '--api-key %s ' % apikey

        # list
        listcmd = ckanbase + 'list'
        status, output = datapkg.util.getstatusoutput(listcmd)
        assert not status, output
        assert 'annakarenina' in output, output

        # info
        cmd = ckanbase + 'info %s' % 'annakarenina'
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert 'annakarenina' in output, output

        # create dummy package if not created already
        if not os.path.exists(self.pkg_path):
            self._test_create()
        
        # register
        registercmd = ckanbase + 'register %s' % self.pkg_path
        status, output = datapkg.util.getstatusoutput(registercmd)
        assert not status, output
        # check actually registered
        listcmd = ckanbase + 'info %s' % self.pkg_name
        status, output = datapkg.util.getstatusoutput(listcmd)
        assert not status, output
        assert self.pkg_name in output, output
        # TODO: test other info is registered

