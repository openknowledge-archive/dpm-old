import os

from dpm.cli.base import Command
from dpm.download import PackageDownloader


class DownloadCommand(Command):
    name = 'download'
    summary = 'Download a package'
    min_args = 1
    max_args = 4
    usage = \
'''%prog {src-spec} [path] [format-pattern] [url-pattern]

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
        index, path = self.index_from_spec(spec_from)
        pkg = index.get(path)

        if len(args) > 1:
            dest_path = os.path.abspath(args[1])
        else:
            dest_path = os.path.join(os.path.abspath('.'), pkg.name)
        if len(args) > 2:
            formatpat = args[2]
            urlpat = args[3] if len(args) > 3 else '*'
            filterfunc = PackageDownloader.make_glob_filterfunc(
                    formatpat,
                    urlpat)
        else:
            filterfunc = pkg_downloader.filterfunc_interactive_choice

        pkg_downloader.download(pkg, dest_path, filterfunc)

