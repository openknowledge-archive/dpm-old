==============
Datapkg Design
==============

Overview
========

The following diagram gives a conceptual overview of the datapkg system. Most, though not all, of the classes indicated already exist within datapkg.

.. image:: overview.png
  :alt: Diagrammatic overview

The central object in datapkg is a **Package**. A Package consists of:

  * metadata
  * payload

One important thing to emphasize is that in datapkg the payload is often not directly available (since it may be very large) but is virtual, being represented by, for example, links to the payload or a listing of the items in the payload (the manifest). In addition to the basic metadata about a package (name, version, title, description etc) we also need to record things like dependencies. Thus a Package main attributes become:

  * basic
  * dependencies
  * manifest

Distributions are serialized Package on disk (or elsewhere) and handle all serialization and deserialization of packages.

  * Other people can provide plugins (datapkg.distribution)
  * These are tried in turn when loading from disk

Tools include downloaders, unpacking and the command line interface.

An Index represents a list of packages whether locally (like DbIndex) or remotely (like CkanIndex). A Repository is an Index plus storage/installation capacity.


Background and Motivation
=========================

Our aim was to have a *simple* way to 'package' data building on *existing* infrastructure. A package consists of 

  * Metadata
  * Payload

Basic aim: KISS (Keep It Simple Stupid!)

Allow people to grab and load data with the minimum of fuss.

Metadata
--------

Metadata has got to be 'hookable' -- that is easily extendable. We will look
to reuse existing standards wherever possible (see below on reuse).

Basic attributes (from dublin core):

  * id (dc:identifier)
  * download-url [opt] -- if not provided default to looking for a file
    called data.py/data.csv/... in same directory.
  * title (dc:title) [opt]
  * description [opt]
  * version [opt] 
  * creator/author (dc:creator) [opt]
  * source (dc:source) [opt]
  * license [opt]
    * rights -- is this needed
  * comments [opt]
  * further-metadata
  * specification of contents (perhaps another list of such packages!)

Payload
-------

It would be nice if the payload could be virtual -- that is if it could be
specified as the result of performing a certain set of steps. This way one
allows for compiling and dependencies (a distinction between binary and
source if you like). Otherwise one greatly limits the scope for reuse.

Reusing existing systems
------------------------

Metadata standards
******************

Wherever possible we should reuse existing metadata standards. In fact it is
essential for the system to work that people can reuse existing systems.

Infrastructure
**************

One possibility is to just treat data packages as a software package and
reuse existing packaging systems such as:

  * apt (debian/ubuntu)
  * distutils/easy_install/pypi (python)

While one would definitely want to reuse such existing infrastructure as far
as possible are there any modifications/additions one need to make to such
system?

  1. It would be unfortunate if a data package system were directly linked to
     a particular language or system. Better if specified by a standard that
     can be implemented inside any system.
  2. Metadata specs for some of these systems are a) software oriented b) not
     obviously available (e.g. apt).

We have therefore chosen to build on top of the python distutils approach.
