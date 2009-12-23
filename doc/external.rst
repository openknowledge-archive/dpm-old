===========================
Notes on External Libraries
===========================

pip_
====

.. _pip: http://pypi.python.org/pypi/pip

As pip_ is a command line tool not a library internal docs are rather poor so we
provide an overview here::

    class PackageFinder(object):
        This finds packages.
        This is meant to match easy_install's technique for looking for
        packages, by reading pages and looking for appropriate links

    class RequirementSet(object):
        More interesting to us as has tools for downloading and unpacking ...
        def __init__(self, build_dir, src_dir, download_dir, download_cache=None,
                     upgrade=False, ignore_installed=False,
                     ignore_dependencies=False):
        src_dir, build_dir not used in unpack_*
        (used in install/install_files, create_bundle)

        def unpack_url(self, link, location, only_download=False):


Downloading: Pages, VCS Systems etc
-----------------------------------

::

    class Link(object):
        Represents a url with a bit of extra info

        def __init__(self, url, comes_from=None):

    class VcsSupport
        cache vcs support information and override urlparse in useful ways

    class VersionControl
        base class with various implementations e.g. Subversion, Mercurial etc

    class HTMLPage

    class PageCache


Probably not relevant to us
---------------------------

::

    class InstallRequirement
        Looks like it handles actually installing something!
        ~600 lines of code

