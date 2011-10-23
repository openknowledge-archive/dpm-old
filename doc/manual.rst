===========
User Manual
===========

dpm is a command line tool (and library) for quickly and easily
distributing collections of data.

.. note:: in what follows items prefixed with $ should be run on the command line.


Quickstart
++++++++++

Obtaining a Package
===================

Search for a package in an Index e.g. on CKAN.net::

    # let's search for iso country/language codes data (iso 3166 ...)
    $ dpm search ckan:// iso
    ...
    iso-3166-2-data -- Linked ISO 3166-2 Data
    ...

Get some information about one of them::

    $ dpm info ckan://iso-3166-2-data

Let's download it (to the current directory)::

    $ dpm download ckan://iso-3166-2-data .

This will download the Package 'iso-3166-2-data' together with its "Resources"
and unpack it into a directory named 'iso-3166-2-data'.

Note: we specify packages using 'package specs' like 'ckan://{name}. For more
on package 'specs' as they are called see the dedicated section below.

Note that, if you replace the ckan:// spec with a file:// spec, you can use
most of the commands for files on disk. For example, if you've downloaded a
data package to, say, /tmp/xyz you could do::

    $ dpm info file:///tmp/xyz

See the help on indivdual commands for more information.


Creating and Registering a Package
==================================

Initialize a new data Package on disk using dpm file layout::

    $ dpm init MyNewDataPackage

Edit the Package's metadata::

    $ vim MyNewDataPackage/setup.py

Add some data to the Package::

    $ cp mydata.csv MyNewDataPackage
    $ cp mydata.js MyNewDataPackage
    $ etc ...

Register it on CKAN::

    # NB: to register on CKAN you'll need to have an api-key
    # This can either be stored in your config file (see dpm setup config)
    # Or you can set it with the --api-key option
    $ dpm register file://MyNewDataPackage ckan://

Check it has registered ok::

    $ dpm info ckan://mynewdpm

You can also upload associated package resources to a storage system. For
example, to register {your-file} with the default storage system associated to
CKAN in a bucket named after {yourpackagename}::

    # this requires you have created your default dpmrc config file
    $ dpm upload {your-file} ckan://{yourpackagename}/{filename}


Tutorial
++++++++

dpm has two distinct uses:

    1. Finding and obtaining data made available *by* others.
    2. Making material available *to* others.


Basic Concepts
==============

Before we begin it is useful to understand some basic dpm concepts:

    1. A Package -- the 'package' of data.
    2. A Distribution -- a serialization of the Package and optionally the data
       too (code, database, a book etc) to some concretely addressable form.
       For example: file(s) on disk, an API at a specific url.

For managing Packages dpm uses:

    1. A Registry: a list of Package metadata (but not Package payload data)
    2. Repository: a Registry plus associated storage for association
       Distributions.


Package Specs (Specifications)
==============================

To specify a package (or just an index/repository) we often use a 'package
spec' (often termed just 'spec'), which have the following url-like form::

    # for CKAN
    ckan://{package-name}
    # on disk
    file://{package-or-index-path}

The use of a 'naked' spec, i.e. one without any scheme such as ckan:// or
file://, like 'mypackage' is used for referring to packages with regard to the
*default* package index.


Obtaining Material
==================

Set Up Configuration [Optional]
-------------------------------

You may want to alter the default configuration, for example to specify your
CKAN apikey. To do this, first set up your local config::

    $ dpm setup config

This will create a .dpmrc file in your home directory. You can then edit
this with your favourite text editor.

Locating and Installing Material
--------------------------------

See Quickstart section above.


Making Your Material Available to Others
========================================

Creating a package (distribution)
---------------------------------

First a skeletal distribution on disk::

    $ dpm init {pkg-name-or-path}

Take a look inside your newly data package. There should be 2 files:

  1. datapackage.json. This is a json file that contains the package metadata
  2. manifest.json. This is a json file giving the file manifest.

For more about the structure of packgae distributions see the :doc:`design` page. 

With the metadata sorted you should add some material to your package. You do
this by simply copying material into the distribution directory, e.g.::

    $ cd {my-new-package}
    $ cp {lots-of-my-data-files} .


Register your package
---------------------

Now you have created a package you will want to make it available.

You can either do this by registering it on a public registry such as CKAN or,
more simply, you can just upload it somewhere and point people to that
location.

Once that is done you register the package on CKAN by doing::

    $ dpm register file://{path} ckan://


Installing your package
-----------------------

You can also download a distribution (only onto disk at the moment!)::

    $ dpm download {package-spec} {path-on-disk}


More About the Command Line
+++++++++++++++++++++++++++

To get a full list of dpm's commands::

    $ dpm help

To get help on a specific command do::

    $ dpm help {command-name}

For generic help do::

    $ dpm -h

