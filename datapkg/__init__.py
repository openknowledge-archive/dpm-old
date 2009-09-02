'''datapkg is a tool for easily distributing knowledge and data by using the 'packaging' concept, which is well established in free software distribution.

By putting data in a package, it gets labelled with standardized metadata and
can be put in a datapkg repository, such as CKAN or a local one. Once in such
a repository, the packages are easy to find and retrieve.

Contents:
    1. Quickstart
    2. Tutorial

1. Quickstart
+++++++++++++

Obtaining a Package
===================

We're going to search for a name of a Package on the CKAN server::

    $ datapkg --ckan search testpkg
    1 Package found:
    testpkg

Let's get it::

    $ datapkg --ckan install testpkg.

This will download the Distribution file testpkg.egg containing the Package
'testpkg' to the current directory (.). Now let's take a look inside it::

    $ datapkg info testpkg.egg

We can see from the metadata that it is a book by Gerald Manley Hopkin's called
"The Windhover" and the payload for the Package is one file, 'windhover.txt'.
Let's extract that file.

    $ datapkg dump windhover.txt

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

Register in your local repository or on CKAN::

    $ datapkg init repo # if repo not already initialized
    $ datapkg register MyNewDataPackage
    $ # OR
    $ datapkg register --ckan --api-key=....  MyNewDataPackage

Check it has registered ok::

    $ datapkg info MyNewDataPackage
    $ # OR (if on CKAN)
    $ datapkg info --ckan MyNewDataPackage

Download the Package again::

(TBD)

2. Tutorial
+++++++++++

datapkg has two distinct uses:

    1. Finding and obtaining data made available *by* others.
    2. Making material available *to* others.

NB: in what follows items prefixed with $ should be run on the command line.


Basic Concepts
==============

Before we begin it is useful to understand some basic datapkg concepts:

    1. A Package -- details about the data.
    2. A Distribution -- disk files which are the Package and optionally the data too (code, database, a book etc).

For managing Packages datapkg uses:

    1. A Registry: a list of Package metadata (but not Package payload data)
    2. Repository: a Registry plus a storage for Packages.

When you start off, the first thing you will do is create a local Repository.


1. Obtaining Material
=====================

1.1 Set Up Your Local Repository
--------------------------------

First set up your local repository::

    $ datapkg init repo

This will create a .datapkg directory in your home directory containing various
files including a main configuration file (config.ini).

(Alternatively you can choose another location for your repository by passing
the --repository option to the init command. If you do so, you will need to
pass this option to all other commands that require use of the repository.)

[Optional] Edit your repository configuration file:

    $ vi .datapkgrc

1.2 Install Material
--------------------

A datapkg Distribution file doesn't have to be associated with a repository to
query or extract its data. Download to your computer this example Distribution:
http://knowledgeforge.net/ckan/pkgdemo.egg
Let's examine it:

    $ datapkg info pkgdemo.egg

We can see that it contains a Package metadata, including name='pkgdemo', as
well as the Package's payload data - a text file.

Next we will register it with our local Registry. The Registry takes a copy of
the metadata and stores the path to the Distribution file.

    $ datapkg register pkgdemo.egg

Now because it is in the Registry, instead of using the filepath we can refer
to this the Package (inside the Distribution) by its name (from the metadata):

    $ datapkg info pkgdemo

It may well be convenient to store the whole of the Package in the repository.
Here we 'install' the Package in our local Repository (which behind the scenes
copies the text file into the .datapkg directory).:

    $ datapkg install pkgdemo

This is particularly useful if we are dealing with a Repository which can be
accessed on the Internet. For example you can specify the datapkg Repository
CKAN with: '--ckan' or one elsewhere with something like: '--repository=http:someserver.com/rest'.

NB: to install from a registered package the package will need to have a
download_url associated.

[NOT YET OPERATIONAL] You can also do this with non-datapkg material Install a
package directly from a url::

    $ datapkg install {url}

TODO: support for replacing path at any point with a url


1.3 Using Material
------------------

Whether you just have a distribution on disk or have installed a package you
can access this material from the command line by using the `dump` command::

    $ datapkg dump {path-or-name} {path-in-package}

For example, if you have installed the pkgdemo package from earlier you could
do::

    $ datapkg dump pkgdemo windhover.txt

Which should result in Gerald Manley Hopkin's "The Windhover" being printed
out (as this is the contents of windhover.txt).

To access the package from python code do::

    >>> import datapkg
    >>> datapkg.make_available('{name-or-path}')


1.4 Find Material
-----------------

Search for a Package on CKAN::

    $ datapkg --ckan list

You can find out about a Package on CKAN by doing::

    $ datapkg --ckan info {pkg-name}

[NOT YET OPERATIONAL]

Copy metadata from the CKAN Registry in your local Registry


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

  2. .egg-info: this directory you can safely ignore (though don't delete it)
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

    $ datapkg --ckan register {path}


3. Installing your package
--------------------------

You can also install the distribution into your local repository::

    $ datapkg install {path-to-distribution}


3. For Developers
=================

The easiest thing (which also guarantees up-to-date-ness) is to look through
the unit tests in ./datapkg/tests/
'''
__version__ = '0.3a'
__description__ = 'Data packaging system and utilities.'
__description_long__ = __doc__
__license__ = 'MIT'
__license_full__ = \
'''All material is licensed under the MIT License:

Copyright (c) 2005-2008, Open Knowledge Foundation

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

# TODO: 2009-03-09 Remove this.
# def install(name):
#     from manager import PackageManager
#     mgr = PackageManager()
#     mgr.install(name)
# 
# def upload(path='.'):
#     fns = os.listdir('.')
#     if 'setup.py' not in fns:
#         msg = '%s does not look like a data package (no setup.py ...)' % path
#         raise Exception(msg)
#     # TODO: implement the rest of this
    

class DatapkgException(Exception):
    pass
