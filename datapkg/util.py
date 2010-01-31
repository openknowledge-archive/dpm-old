import os
import platform

# annoyingly there does not seem to be a single standard way to check you are
# on windows
def getstatusoutput(cmd):
    '''Wrap L{commands.getstatusoutput} so it works on Windows.'''
    os = platform.system()
    if  os == 'Windows':
        # from http://gizmodise.com/linux/?p=70 
        import os
        pipe = os.popen('\"' + cmd + '\" 2>&1', 'r')
        text = pipe.read()
        sts = pipe.close()
        if sts is None: sts = 0
        if text[-1:] == '\n': text = text[:-1]
        return sts, text
    else:
        import commands
        return commands.getstatusoutput(cmd)


import urlgrabber
import urlgrabber.progress
import posixpath
import zipfile
class Downloader(object):
    '''Handling downloading (and unnpacking) of resources.
    '''

    def __init__(self,  base_dir='.', **kwargs):
        '''
        @param base_dir: default base directory to use for downloading
        material.
        '''
        self.base_dir = os.path.abspath(os.path.expanduser(base_dir))
        self.cache_dir = os.path.join(self.base_dir, '.download_cache')
        # makes self.base_dir too ...
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def download(self, url, dest=None, **kwargs):
        '''Download a 'resource' at url to dest.

        @param dest: if dest is None download to self.base_dir.
        @param kwargs: as for urlgrabber.urlgrab
        @return: path to downloaded file

        Notes: by default a progress meter is provided. To disable this pass
        progress_obj=None as a kwarg.

        TODO: support vcs backend (e.g. svn, hg etc)
        '''
        ourkwargs = {
            'progress_obj': urlgrabber.progress.TextMeter()
            }
        ourkwargs.update(kwargs)
        location = dest
        if location is None:
            link = Link(url)
            filename = link.filename
            location = os.path.join(self.base_dir, filename)
        filename = urlgrabber.urlgrab(url, location, **ourkwargs)
        return filename
    
    def unpack_file(self, src, dest):
        # if a zip, targz etc then unpack o/w leave it
        if (filename.endswith('.zip')
            or zipfile.is_zipfile(filename)):
            self.unzip_file(filename, location, flatten=not filename.endswith('.pybundle'))
        
    # from pip
    def unzip_file(self, filename, location, flatten=True):
        """Unzip the file (zip file located at filename) to the destination
        location"""
        if not os.path.exists(location):
            os.makedirs(location)
        zipfp = open(filename, 'rb')
        try:
            zip = zipfile.ZipFile(zipfp)
            leading = has_leading_dir(zip.namelist()) and flatten
            for name in zip.namelist():
                data = zip.read(name)
                fn = name
                if leading:
                    fn = split_leading_dir(name)[1]
                fn = os.path.join(location, fn)
                dir = os.path.dirname(fn)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                if fn.endswith('/') or fn.endswith('\\'):
                    # A directory
                    if not os.path.exists(fn):
                        os.makedirs(fn)
                else:
                    fp = open(fn, 'wb')
                    try:
                        fp.write(data)
                    finally:
                        fp.close()
        finally:
            zipfp.close()


# taken from pip v0.6.2
# MIT licensed
class Link(object):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return self.url

    def __repr__(self):
        return '<Link %s>' % self

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)

    @property
    def filename(self):
        url = self.url
        url = url.split('#', 1)[0]
        url = url.split('?', 1)[0]
        url = url.rstrip('/')
        name = posixpath.basename(url)
        assert name, (
            'URL %r produced no filename' % url)
        return name

    @property
    def scheme(self):
        return urlparse.urlsplit(self.url)[0]

    @property
    def path(self):
        return urlparse.urlsplit(self.url)[2]

    def splitext(self):
        return splitext(posixpath.basename(self.path.rstrip('/')))

