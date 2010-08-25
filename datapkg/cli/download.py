import os

from datapkg.cli.base import Command
from datapkg.download import PackageDownloader


class DownloadCommand(Command):
    name = 'download'
    summary = 'Download a package'
    min_args = 2
    max_args = 2
    usage = \
'''%prog {src-spec} {path}

Install a package specified by {src-spec} to path, e.g.::

    download ckan://name path-on-disk
'''

    def run(self, options, args):
        spec_from = args[0]
        dest_path_base = args[1]
        index, path = self.index_from_spec(spec_from)
        pkg = index.get(path)
        dest_path = os.path.join(dest_path_base, pkg.name)
        pkg_downloader = PackageDownloader(verbose=self.verbose)
        pkg_downloader.download(pkg, dest_path)


'''
        # This is a mess and needs to be sorted out
        # Need to distinguish Distribution from a simple Package and much else

        # TODO: decide what to do with stuff on local filesystem
        # if pkg.installed_path: # on local filesystem ...
        #     import shutil
        #     dest = os.path.join(path_to, pkg.name)
        #     shutil.copytree(pkg.installed_path, dest)

        # go through normal process (may just be metadata right ... not a dist)
        install_path = os.path.join(index_to.index_path, pkg.name)
        # we can assume for present that this is not a real 'package' and
        # therefore first register package on disk
        print 'Registering ... '
        install_path = index_to.register(pkg)
        print 'Created on disk at: %s' % install_path
        if pkg.download_url:
            import datapkg.util
            downloader = datapkg.util.Downloader(install_path)
            print 'Downloading package resources ...'
            downloader.download(pkg.download_url)
        else:
            msg = u'Warning: no resources to install for package %s (no download url)' % pkg.name
            logger.warn(msg)
            print msg
'''
