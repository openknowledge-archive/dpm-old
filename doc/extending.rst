=================
Extending Datapkg
=================

Datapkg has been designed to be easily extensible. At the present time you can
write your own implementations of:

  * Commands - extend datapkg command line interface with new commands
  * Indexes - add new Indexes with which datapkg can communicate
  * Distribution - add new Distribution types (either for reading or writing or
    both)
  * (Package) Resource downloader - add support for downloading different types
    of resources
  * Uploader (via OFS) - upload to different storage backends


Commands
========

It is easy to add your own custom commands to the set of commands available
from the `datapkg` command line interface.

To provide a new command named 'mycommand':

  1. Create a new command class inheriting from `datapkg.cli.Command`. This may
     be called anything you want. Assume it is called 'MyNewCommand' in package
     mynewpackage.command
  2. In the setup.py of your new python package (containing the new command)
     add to the `datapkg.cli` entry poing section and entry named 'mycommand'::

      [datapkg.cli]
      mycommand = mynewpackage.command:MyNewCommand

Command Base Class
------------------

.. autoclass:: datapkg.cli.Command
  :members:


Index
=====

To provide a new Index for datapkg to use (e.g. in datapkg search and datapkg
download commands) you must:

  1. Create a new Index class inheriting from `datapkg.index.IndexBase` (see
     below)
  2. Add an entry point for your Index class in the `[datapkg.index]` section
     of your setup.py entry_points.

    * NB: the index will be available in datapkg commands (such as search) via
      the entry point name. E.g. if the entry point section looks like::

        [datapkg.index]
        mynewindex = mypackage.customindex:CustomIndex

      then the can be used in datapkg commands as follows::

        $ datapkg search mynewindex:// {search-tem}


Index Base class
----------------

.. autoclass:: datapkg.index.base.IndexBase
  :members:


Distributions
=============

To provide a new Distribution (either for reading, writing or both) for datapkg
to use you must:

  1. Create a new Distribution class inheriting from
     :class:`datapkg.distribution.DistributionBase` (see
     below)
  2. Add an entry point for your Index class in the `[datapkg.distribution]` section
     of your setup.py entry_points.

Distribution Base class
-----------------------

.. autoclass:: datapkg.distribution.DistributionBase
  :members:


Resource Downloader
===================

.. autoclass:: datapkg.download.ResourceDownloaderBase
  :members:


Uploading
=========

datapkg utilizes the pluggable blobstore library OFS
(http://bitbucket.org/okfn/ofs).

To add a new storage backend just extend OFS and this new backend will be
automatically available to datapkg.

