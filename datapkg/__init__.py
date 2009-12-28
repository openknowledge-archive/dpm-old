'''datapkg is a tool for easily distributing knowledge and data by using the
'packaging' concept, which is well established in software distribution. Full
documentation can be found at: http://knowledgeforge.net/ckan/doc/datapkg/

Contents:
    1. Quickstart
    2. Tutorial

NB: in what follows items prefixed with $ should be run on the command line.


1. Quickstart
+++++++++++++

Obtaining a Package
===================

Search for a package in an Index e.g. on CKAN.net::

    $ datapkg search ckan:// windhover
    ...
    datapkgdemo -- ...
    ...

Get some information about one of them (in this case our demonstration package
on
ckan.net)::

    $ datapkg info ckan://datapkgdemo

Let's install one of them (to the current directory)::

    $ datapkg install ckan://datapkgdemo .

This will download the Distribution file for Package 'datapkgdemo' and
unpack it in the current directory '.'.


Creating and Registering a Package
==================================

Create a new data Package on disk using datapkg file layout::

    $ datapkg create MyNewDataPackage

Edit the Package's metadata::

    $ vim MyNewDataPackage/setup.py

Add some data to the Package::

    $ cp mydata.csv MyNewDataPackage
    $ cp mydata.js MyNewDataPackage
    $ etc ...

Register it on CKAN::

    # NB: to register on CKAN you'll need to have an api-key
    # This can either be stored in your config file (see datapkg init config)
    # Or you can set it with the --api-key option
    $ datapkg register MyNewDataPackage ckan://

Check it has registered ok::

    $ datapkg info ckan://mynewdatapkg

[Not Yet Functional]: uploading package distributions.


2. Tutorial
+++++++++++

datapkg has two distinct uses:

    1. Finding and obtaining data made available *by* others.
    2. Making material available *to* others.


Basic Concepts
==============

Before we begin it is useful to understand some basic datapkg concepts:

    1. A Package -- the 'package' of data.
    2. A Distribution -- a serialization of the Package and optionally the data
       too (code, database, a book etc) to some concretely addressable form.
       For example: file(s) on disk, an API at a specific url.

For managing Packages datapkg uses:

    1. A Registry: a list of Package metadata (but not Package payload data)
    2. Repository: a Registry plus associated storage for association
       Distributions.

To specify a package (or just an index/repository) we often use a 'package
spec' (often termed just 'spec'), which have the following form::

    # for CKAN
    ckan://{package-name}
    # on disk
    file://{package-or-index-path}
    # or even just
    {package-or-index-path}


1. Obtaining Material
=====================

1.1 [Optional] Set Up Configuration
-----------------------------------

You may want to alter the default configuration, for example to specify your
CKAN apikey. To do this, first set up your local config::

    $ datapkg init config

This will create a .datapkgrc file in your home directory. You can then edit
this with your favourite text editor.

1.2 Locating and Installing Material
------------------------------------

See Quickstart section above.


2. Making Your Material Available to Others
===========================================

2.1 Creating a package (distribution)
-------------------------------------

First a skeletal distribution on disk::

    $ datapkg create {pkg-name-or-path}

Take a look inside your newly created distribution directory. There should
be 3 files/directories:

  1. MANIFEST.in: this specifies what files/directories within the distribution
     directory should actually be included in the package.

     * For instructions on using the MANIFEST.in to specify what files to
       include see http://docs.python.org/distutils/commandref.html#sdist-cmd

  2. .egg-info: this directory you can safely ignore
  3. setup.py: this files holds metadata about your package.

Generally the only file you should have to alter is setup.py. Open this up in
your favourite editor and then modify the various attributes to be as you would
like them.

Having sorted out the metadata you will actually want to add some material to
your package. You do this by simply copying material into the distribution
directory, e.g.::

    $ cd {my-new-package}
    $ cp {lots-of-my-data-files} .


2. Register your package
------------------------

Now you have created a package you will want to make it available.

You can either do this by registering it on a public registry such as CKAN or,
more simply, you can just upload it somewhere and point people to that
location.

Once that is done you register the package on CKAN by doing::

    $ datapkg register {path} ckan://


3. Installing your package
--------------------------

You can also install a distribution::

    $ datapkg install {package-spec} {file-spec}


3. For Developers
=================

The easiest thing (which also guarantees up-to-date-ness) is to look through
the unit tests in ./datapkg/tests/
'''
__version__ = '0.4'
__description__ = 'Data packaging system and utilities.'
__description_long__ = __doc__
__license__ = 'MIT'
__license_full__ = \
'''All material is licensed under the MIT License:

Copyright (c) 2005-2009, Open Knowledge Foundation

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os

class DatapkgException(Exception):
    pass

