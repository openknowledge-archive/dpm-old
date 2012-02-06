=======
History
=======

HEAD
====

v0.10 2012-01-29
================

  * Rename from datapkg to dpm (data package manager)
  * Support for dpm push for "source" packages
  * Clean set of library commands to facilitate reuse of dpm from 3rd party
    code (thanks to @dgraziotin)

v0.9 2011-09-30
===============

  * Standardize on JSON-based distribution (and remove ini-based distribution)
  * Fix various (minor) bugs
  * Overhaul docs
  * Breaking change: json package info now in datapackage.json

V0.8 2011-02-09
===============

  * ResourceDownloader objects and plugin point (#964)
  * Refactor PackageDownloader to use ResourceDownloader and support Resource
    filtering
  * Retrieval options for package resourcs (#405). Support selection of
    resources to download (on command line or API) via glob style patterns or
    user interaction.

V0.7.1 2010-12-02
=================

  * MINOR: soften dependency on ckanclient to >= 0.3 for better compatibility
    with CKAN

V0.7 2010-10-11
===============

  * MAJOR: Support for uploading dpms (upload.py)
  * MAJOR: Much improved and extended documenation
  * MAJOR: New sqlite-based DB index giving support for a simple, central,
    'local' index (ticket:360)
  * MAJOR: Make dpm easily extendable

    * Support for adding new Index types with plugins
    * Support for adding new Commands with command plugins
    * Support for adding new Distributions with distribution plugins

  * Improved package download support (also now pluggable)
  * Reimplement url download using only python std lib (removing urlgrabber
    requirment and simplifying installation)
  * Improved spec: support for db type index + better documentation
  * Better configuration management (especially internally)
  * Reduce dependencies by removing dependency on PasteScript and PasteDeploy
    (#98)
  * Various minor bugfixes and code improvements


V0.6.1 2010-05-04
=================

  * Bugfix release to address breaking changes in python >= 2.6.5 - see
    http://bugs.python.org/issue7904

V0.6 2010-04-28
===============

  * Fixes for unicode in package metadata (when writing to disk)
  * Remove use of ast module as only in python 2.5/2.6 
  * Upgrade to use ckanclient 0.3
  * Improved python api for usage of dpm (load_package and load_index)

V0.5 2010-02-12
===============

  * Improve downloading of package resources (and remove dependency on pip)
  * Improved installation with metadata written consistently (install now
    really, really works!)
  * Register to disk works (writes metadata to disk)
  * Continued improvements to CLI and documentation

V0.4.1 2010-01-19
=================

  * Restrict to pip<=0.6.1 (just released pip 0.6.2 has major code re-layout
    which causes breakages)

V0.4 2009-12-28
===============

  * Major refactoring to simplify and standardize CLI using 'package specs'
  * Support for searching indices from CLI, e.g.::
        dpm search ckan:// myquery
  * Simple installation onto disk
  * Overhauled and improved documentation and put docs online


V0.3 2009-08-25
===============

This release features major improvements over v0.2 particularly in area of CKAN
integration with 'write' support especially improved.

  * Better and more flexible system for reading and writing packages to disk 

    * New Distribution object to encapsulate writing and reading to disk
    * Implemenations for Python packages (PythonDistribution) and simple ini
      file (metadata.txt) format (IniBasedDistribution)

  * Improved approach for configuration with config stored in a dedicated ini
    file and lots of minor fixes to improve CLI experience
  * Create new Index object SimpleIndex
  * Completely overhaul package metadata with support for many additional
    attribues (author, maintainer, extras etc)
  * Improved, sphinx-built docs (http://knowledgeforge.net/ckan/doc/dpm/)


v0.2 2009-03-18
===============

  * Completely refactor CLI making it better documented and easier to use
  * Support for 'flat' package structure on disk
  * Improve creation of on disk package (MANIFEST.in etc)
  * CKAN integration fully functional
  * Almost all commands now functioning *and* tested


v0.1 2008-12-15
===============

  * Manual much improved 
  * CLI: info and dump commands working (r331)
  * Substantial improvements to interface to setuptools and easy_install
    (pypkgtools)
  * First official released to PyPI
  * Several bugs fixed


v0.0.5 2008-07-15
=================

  * Start on manual
  * Core objects mostly working: Register, Repository, Package
  * Integration with CKAN (not tested)
  * Lots of tests
  * Basic functions but a way to go for proper upload/download cycle
  

2007-06-20: Project Started
===========================

