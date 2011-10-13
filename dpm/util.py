import os
import sys
import urllib
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


import posixpath
import zipfile
class Downloader(object):
    '''Handling downloading (and unnpacking) of urls.
    '''
    def download(self, url, dest_dir, progress_bar=True, **kwargs):
        '''Download a 'resource' at `url` to a destination directory `dest`.

        @param dest_dir: destination directory to download to.

        @return: path to downloaded file

        TODO: support vcs backend (e.g. svn, hg etc)
        '''
        link = Link(url)
        filename = link.filename
        location = os.path.join(dest_dir, filename)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        if progress_bar:
            reporthook = self._dl_progress
        else:
            reporthook = None
        self._download_count = -1
        urllib.urlretrieve(url, location, reporthook=reporthook)
        return location

    def _dl_progress(self, count, block_size, total_size):
        def format_size(bytes):
            if bytes > 1000*1000:
                return '%.1fMb' % (bytes/1000.0/1000)
            elif bytes > 10*1000:
                return '%iKb' % (bytes/1000)
            elif bytes > 1000:
                return '%.1fKb' % (bytes/1000.0)
            else:
                return '%ib' % bytes
    
        if count == 0:
            print('Total size: %s' % format_size(total_size))
        last_percent = int((count-1)*block_size*100/total_size)
        # may have downloaded less if count*block_size > total_size
        maxdownloaded = count * block_size
        percent = min(int(maxdownloaded*100/total_size), 100)
        if percent > last_percent:
            # TODO: is this acceptable? Do we want to do something nicer?
            sys.stdout.write('%3d%% [%s>%s]\r' % (
                percent,
                percent/2 * '=',
                (50 - percent/2) * ' '
                ))
            sys.stdout.flush()
        if maxdownloaded >= total_size:
            print('\n')

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

