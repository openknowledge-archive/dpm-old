import os
import shutil
import tempfile

class TestCase(object):
    system_tmpdir = tempfile.gettempdir()

    @classmethod
    def set_tmpdir(self):
        name = self.__module__ + '-' + self.__class__.__name__
        name = name.replace('.', '-')
        self.tmpdir = os.path.join(self.system_tmpdir, name)

    @classmethod
    def make_tmpdir(self):
        '''If exists remove it.'''
        self.set_tmpdir()
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        os.makedirs(self.tmpdir)
        
