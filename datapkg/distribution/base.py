import os

class DistributionBase(object):
    # distribution_type = None

    def __init__(self, package=None):
        self.package = package

    def write(self, path, **kwargs):
        '''Write this distribution to disk at `path`.
        '''
        raise NotImplementedError

    @classmethod
    def load(self, path):
        '''Load a L{Package} object from a path to a package distribution.
        
        @return: the Distribution object.
        '''
        raise NotImplementedError

    def stream(self, path):
        '''Return a fileobj stream for material at `path`.
        '''
        full_path = os.path.join(self.package.installed_path, path)
        return open(full_path)




