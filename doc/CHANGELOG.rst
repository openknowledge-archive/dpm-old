=======
History
=======

HEAD
====

V0.6.1 2010-05-04
=================

  * Bugfix release to address breaking changes in python >= 2.6.5 - see
    http://bugs.python.org/issue7904

V0.6 2010-04-28
===============

  * Fixes for unicode in package metadata (when writing to disk)
  * Remove use of ast module as only in python 2.5/2.6 
  * Upgrade to use ckanclient 0.3
  * Improved python api for usage of datapkg (load_package and load_index)

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
        datapkg search ckan:// myquery
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
  * Improved, sphinx-built docs (http://knowledgeforge.net/ckan/doc/datapkg/)


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

