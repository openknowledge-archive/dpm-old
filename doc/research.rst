========
Research
========


Python
======

Basic distribution format is zip or tar.gz. Metadata rather hacked (originally
just distributed code files not metadata).

  * Metadata (setup.py and/or PKG-INFO)
  * Payload: files (including) data specified usually using combination of
    setup.py and MANIFEST/MANIFEST.in (manifest template)
  * setuptools and egg-info is a bit of a mess (see below and our wrapper code)
    but getting sorted out (as of late 2009)

Further documentation:

  1. Misc

    * A Database of Installed Python Packages:
      <http://www.python.org/dev/peps/pep-0262/>
    * Presentation: https://dfwpython.org/static/pycon/1-python-distutils.pdf

  2. Setuptools

    * http://farmdev.com/thoughts/76/the-python-packaging-problem/
    * http://wiki.python.org/moin/Distutils
    * Observations:

      * REALLY hard to work what is going on. E.g.
      * How does .easy-install.pth stuff work.

    * Without doing custom install
      http://peak.telecommunity.com/DevCenter/EasyInstall#custom-installation-locations
      cannot get all the easy_install magic of looking stuff up by name (as
      this involves messing with python binary or site packages). So just
      install and get the dirctory path.



Debian (and R)
==============

TODO: write-up

  * Built format is tar
  * metadata in ini-file + resources (files)


OPeNDAP (open network data access protocol)
===========================================

Mostly culled from http://www.opendap.org/user/quick-html/quick_1.html

Originally developed by oceaneographic institute as DODS (Distributed
Oceanographic Data System) as a protocol for accessing and serving data in a
manner that is transparent for remote users.

Main aspects are:

  1. Metadata

    1. Dataset Descriptor Structure  (DDS) -- Structure of the data. "This
       provides a description of the "shape" of the data, using a vaguely
       C-like syntax. You get a dataset's DDS by appending .dds to the URL."
    2. Data Attribute Structure (DAS) -- "contains information about the data,
       such as units and the name of the variable"

      * "NOTE: The DAS is populated at the data provider's discretion. Because
        of this, the quality of the data in it (the metadata) varies widely.
        The data in the Reynolds dataset used in this example are COARDS
        compliant. Other metadata standards you may encounter with DODS data
        are HDF-EOS, EPIC, FGDC, or no metadata at all."

    3. Info service: append .info to the url to get back DDS and DAS

  2. Data:

    * html query: Append .html to the URL, and you get a form that directs you
      to add information to sample the data at a URL

  3. Querying. query string: {url}?{array-name}[{restriction ...}]

    * e.g. ...sst/mnmean.nc.asc?time[0:6]

Example: http://www.cdc.noaa.gov/cgi-bin/nph-nc/Datasets/reynolds_sst/sst.mnmean.nc


Virtual Observatory
===================

  * Sharing datasets in astronomy
  * Developed a data catalogue and data search and retrieval service


OAI-PMH
=======

Protocol for retrieving bibliographic catalogue data especially in relation to (research) papers.

  * Metadata: dublin-core based (XML)
  * Payload/resources: not relevant as not transmitted (metadata only service)
    -- though can obviously point to resources.

