=======
History
=======

V0.4 ????
=========

  * Use 'package specs' in CLI to simplify and standardize operations on
    packages and indexes
  * Support for searching indices from CLI, e.g.::
        datapkg search ckan:// myquery
  * Simple installation onto disk


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

