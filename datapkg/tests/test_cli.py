import os
import commands
import tempfile
import shutil

import datapkg.tests.base

import datapkg.cli
import datapkg.util
import datapkg.repository
import datapkg.package

class TestCLI(datapkg.tests.base.TestCase):

    @classmethod
    def setup_class(self):
        self.tmpdir = self.make_tmpdir()
        self.index_path = os.path.join(self.tmpdir, 'datapkg-index')
        self.repo_path = os.path.join(self.tmpdir, 'datapkg-repo')
        self.index_spec = 'file://%s' % self.index_path
        self.repo_spec = 'file://%s' % self.repo_path
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        os.makedirs(self.tmpdir)
        self.cwd = os.getcwd()
        self.cmd_base = 'datapkg '

        self.pkg_name = u'mytestpkg'
        self.pkg_title = u'Test Title'
        self.pkg_path = os.path.join(self.tmpdir, self.pkg_name)
        fp = os.path.join(self.pkg_path, 'abc.txt')
        pkg = datapkg.package.Package(
            name=self.pkg_name,
            title=self.pkg_title,
            download_url='file://%s' % fp
            )
        pkg.write(self.pkg_path)
        fo = open(fp, 'w')
        fo.write('Ideas are cheap, implementation is costly.')
        fo.close()
        self.file_spec = u'file://%s' % self.pkg_path

    @classmethod
    def teardown_class(self):
        # do not teardown directory in order to allow investigation on error
        # reset cwd or problems in other tests
        os.chdir(self.cwd)

    def test_1_about(self):
        cmd = 'datapkg about'
        status, output = commands.getstatusoutput(cmd)
        exp = 'datapkg version'
        assert exp in output

    def test_4_walkthrough(self):
        cmd = self.cmd_base + 'list %s' % (self.index_spec)
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert not self.pkg_name in output, (cmd, output)

        # create 
        create_path = os.path.join(self.tmpdir, 'test-create-xxx')
        cmd = self.cmd_base + 'create %s' % create_path
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert os.path.exists(create_path)

        # info: from disk
        cmd = self.cmd_base + 'info %s' % self.file_spec
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert self.pkg_name in output, output
        assert self.pkg_title in output, output

        # register
        cmd = self.cmd_base + 'register %s %s' % (self.file_spec,
                self.index_spec)
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        destpath = os.path.join(self.index_path, self.pkg_name)
        assert os.path.exists(destpath), os.listdir(self.index_path)
        pkg = datapkg.package.Package.load(destpath)
        assert pkg.title == self.pkg_title

        cmd = self.cmd_base + 'list %s' % (self.index_spec)
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert self.pkg_name in output

        cmd = self.cmd_base + 'search %s %s' % (self.index_spec, self.pkg_name)
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        assert self.pkg_name in output

        # not a particularly good test because we won't change anything
        cmd = self.cmd_base + 'update %s %s' % (self.file_spec, self.index_spec)
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output

        # install
        cmd = self.cmd_base + 'install %s %s' % (self.file_spec,
                self.repo_spec)
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        print output
        # dest path with be self.pkg_name-version-*
        # dirs = os.listdir(repo.installed_path)
        # filtered = filter(lambda x: x.startswith(self.pkg_name), dirs)
        # assert len(filtered) > 0, dirs
        dest_path = os.path.join(self.repo_path, self.pkg_name)
        assert os.path.exists(dest_path), dest_path

        # inspect - not yet implemented
        # cmd = self.cmd_base + 'inspect %s' % self.pkg_name
        # status, output = datapkg.util.getstatusoutput(cmd)
        # assert not status, output

        # dump
        offset = 'abc.txt'
        cmd = self.cmd_base + 'dump %s %s' % (self.pkg_path, offset)
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
    
    # For this need dummy ckan running locally with standard test data
    def _test_ckan(self):
        # localckan = 'http://localhost:5000/api/'
        localckan = 'http://test.ckan.net/api/'
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

        # update - won't do anything as nothing has changed
        registercmd = ckanbase + 'update %s' % self.pkg_path
        status, output = datapkg.util.getstatusoutput(registercmd)
        assert not status, output

    # requires external access
    def test_6_ckan_readonly(self):
        # this depends on datapkgdemo existing on ckan.net 
        localckan = 'http://ckan.net/api'
        ckanspec = 'ckan://%s' % localckan
        ckanbase = 'datapkg '

        pkg_name = u'datapkgdemo'
        pkg_version = '0.1'
        # TODO: not unpacked yet
        fullname = '%s-%s.tar.gz' % (pkg_name, pkg_version)
        # install
        cmd = ckanbase + 'install %s/%s %s' % (ckanspec, pkg_name,
            self.repo_spec)
        status, output = datapkg.util.getstatusoutput(cmd)
        assert not status, output
        dest_path = os.path.join(self.repo_path, pkg_name, fullname)
        assert os.path.exists(dest_path), dest_path

