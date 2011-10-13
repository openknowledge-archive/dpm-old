=================
Extending Datapkg
=================

Datapkg has been designed to be easily extensible. At the present time you can
write your own implementations of:

  * Commands - extend dpm command line interface with new commands
  * Indexes - add new Indexes with which dpm can communicate
  * Distribution - add new Distribution types (either for reading or writing or
    both)
  * (Package) Resource downloader - add support for downloading different types
    of resources
  * Uploader (via OFS) - upload to different storage backends


Commands
========

It is easy to add your own custom commands to the set of commands available
from the `dpm` command line interface.

To provide a new command named 'mycommand':

  1. Create a new command class inheriting from `dpm.cli.Command`. This may
     be called anything you want. Assume it is called 'MyNewCommand' in package
     mynewpackage.command
  2. In the setup.py of your new python package (containing the new command)
     add to the `dpm.cli` entry poing section and entry named 'mycommand'::

      [dpm.cli]
      mycommand = mynewpackage.command:MyNewCommand

Command Base Class
------------------

.. autoclass:: dpm.cli.Command
  :members:


Index
=====

To provide a new Index for dpm to use (e.g. in dpm search and dpm
download commands) you must:

  1. Create a new Index class inheriting from `dpm.index.IndexBase` (see
     below)
  2. Add an entry point for your Index class in the `[dpm.index]` section
     of your setup.py entry_points.

    * NB: the index will be available in dpm commands (such as search) via
      the entry point name. E.g. if the entry point section looks like::

        [dpm.index]
        mynewindex = mypackage.customindex:CustomIndex

      then the can be used in dpm commands as follows::

        $ dpm search mynewindex:// {search-tem}


Index Base class
----------------

.. autoclass:: dpm.index.base.IndexBase
  :members:


Distributions
=============

To provide a new Distribution (either for reading, writing or both) for dpm
to use you must:

  1. Create a new Distribution class inheriting from
     :class:`dpm.distribution.DistributionBase` (see
     below)
  2. Add an entry point for your Index class in the `[dpm.distribution]` section
     of your setup.py entry_points.

Distribution Base class
-----------------------

.. autoclass:: dpm.distribution.DistributionBase
  :members:


Resource Downloader
===================

.. autoclass:: dpm.download.ResourceDownloaderBase
  :members:


Uploading
=========

dpm utilizes the pluggable blobstore library OFS
(http://bitbucket.org/okfn/ofs).

To add a new storage backend just extend OFS and this new backend will be
automatically available to dpm.

