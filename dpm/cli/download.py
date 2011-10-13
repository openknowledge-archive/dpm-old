import os

from dpm.cli.base import Command
from dpm.download import PackageDownloader


class DownloadCommand(Command):
    name = 'download'
    summary = 'Download a package'
    min_args = 2
    max_args = 4
    usage = \
'''%prog {src-spec} {path} [format-pattern] [url-pattern]

Download a package (i.e. metadata and resources) specified by {src-spec} to
{path}.

Resources to retrieve are selected interactively if no format-pattern is given.
If provided, the optional glob-style format-pattern and url-pattern arguments
are matched against the format and url of the resource to determine whether it
should be retrieved.

    # download the package specified by ckan://name to path-on-disk
    # selecting the resources to retrieve interactively
    download ckan://name path-on-disk

    # download all resources
    # Note need to quote *
    download ckan://name path-on-disk "*"

    # download only those resources that have format 'csv' (or 'CSV')
    download ckan://name path-on-disk csv

    # download only those resources that have format starting xml/
    download ckan://name path-on-disk xml/*

    # download only those resources that have a url starting http://abc (and any format)
    download ckan://name path-on-disk "*" http://abc*
'''

    def run(self, options, args):
        pkg_downloader = PackageDownloader(verbose=True)
        spec_from = args[0]
        dest_path_base = args[1]
        if len(args) > 2:
            formatpat = args[2]
            urlpat = args[3] if len(args) > 3 else '*'
            filterfunc = PackageDownloader.make_glob_filterfunc(
                    formatpat,
                    urlpat)
        else:
            filterfunc = pkg_downloader.filterfunc_interactive_choice

        index, path = self.index_from_spec(spec_from)
        pkg = index.get(path)
        dest_path = os.path.join(dest_path_base, pkg.name)
        pkg_downloader.download(pkg, dest_path, filterfunc)


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
            import dpm.util
            downloader = dpm.util.Downloader(install_path)
            print 'Downloading package resources ...'
            downloader.download(pkg.download_url)
        else:
            msg = u'Warning: no resources to install for package %s (no download url)' % pkg.name
            logger.warn(msg)
            print msg
'''
