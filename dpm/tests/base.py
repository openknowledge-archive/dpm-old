import os
import shutil
import tempfile

class TestCase(object):
    #gettempdir() does not work for me, gives permission errors (dgraziotin)
    system_tmpdir = tempfile.mkdtemp()

    @classmethod
    def set_tmpdir(self):
        name = self.__module__ + '-' + self.__name__.lower()
        name = name.replace('.', '-')
        self.tmpdir = os.path.join(self.system_tmpdir, name)

    @classmethod
    def make_tmpdir(self):
        '''If exists remove it.'''
        self.set_tmpdir()
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        os.makedirs(self.tmpdir)
        return self.tmpdir

    @classmethod
    def setup_for_upload(self):
        import dpm
        self.upload_dir = os.path.join(self.tmpdir, 'upload-pt')
        # pairtree needs a clean (uncreated) dir
        # os.makedirs(self.upload_dir)
        section = 'upload:mypairtree'
        if not dpm.CONFIG.has_section(section):
            dpm.CONFIG.add_section(section)
        dpm.CONFIG.set(section, 'ofs.backend', 'pairtree')
        dpm.CONFIG.set(section, 'storage_dir', self.upload_dir)

#     @classmethod
#     def make_test_package(self, pkg_name, **kwargs):
#         import dpm.package
#         pkg = dpm.package.Package(pkg_name, **kwargs)
#         pkg.manifest['data.csv'] = None
#         pkg.manifest['data.js'] = {'format': 'json'}
#         return pkg
# 
#     # TODO: finish this off
#     @classmethod
#     def make_test_package_on_disk(self, pkg_name, **kwargs):
#         import dpm.package
#         pkg = dpm.package.Package(pkg_name, **kwargs)
#         pkg.manifest['data.csv'] = None
#         pkg.manifest['data.js'] = {'format': 'json'}
#         # pkg.write(...)
#         return pkg

