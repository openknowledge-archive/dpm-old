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


import urllib2
import sys
import pip
complete_log = []
pip.logger = pip.Logger([(pip.Logger.NOTIFY, sys.stdout),
                     (pip.Logger.DEBUG, complete_log.append)])

class Downloader(object):
    '''Handling downloading (and unnpacking) of resources.

    Do not just handle normal urls but also version control systems (e.g. hg,
    svn, git).

    Much of our functionality is obtained by wrapping the pip
    (http://pypi.python.org/pypi/pip). More information on pip can be found in
    the docs (doc/external.rst).
    '''

    def __init__(self,  base_dir):
        '''
        @param base_dir: base directory to use for downloading material as
        necessary (e.g. when ``dest`` not specified in ``download``.
        '''
        self.base_dir = base_dir
        self.cache_dir = os.path.join(self.base_dir, '.download_cache')
        # makes self.base_dir too ...
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self.reqset = pip.RequirementSet(build_dir=None, src_dir=None,
                download_dir=self.base_dir, download_cache=self.cache_dir)

    def download(self, url, dest=None, unpack=True):
        '''Download a 'resource' (normal file, vcs repo etc) at url to dest.

        @param dest: destination to download to -- if None save to
        self.base_dir/{url-file-name}.

        Warning if unpack=True then dest is ignored and file is always unpacked
        to self.base_dir
        '''
        link = pip.Link(url)
        if dest is None:
            filename = link.splitext()[0]
            location = os.path.join(self.base_dir, filename)
        else:
            location = dest
        only_download = not unpack
        try:
            self.reqset.unpack_url(link, location, only_download)
        except urllib2.HTTPError, e:
            logger.fatal('Could not download %s because of error %s'
                         % (url, e))
            raise Exception(
                'Could not download %s because of HTTP error %s for URL %s'
                % (url, e, url))

