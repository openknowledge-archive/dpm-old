===========================================
Data Package Manager - New Plan Autumn 2011
===========================================


The two roles:

* dpm as a data *package* manager - like pip, gem, apt-get
* dpm as a data *source* manager - like mercurial / git / ...

dpm as pure *package* manager
-----------------------------

Commands::

  dpm search
  dpm info
  dpm install
  dpm publish 

dpm as source package manager
-----------------------------

Commands::

  dpm clone
  dpm init
  dpm push
  dpm add

Creating source data package from scratch::

  $ dpm init {name}
  > ask you a few questions
  Your source data package has been created at ...
  
  # create csv
  $ cp /some/path/to/my.csv data/my.csv
  $ dpm add data/my.csv
  $ dpm status
  Staged files are ...
  
  # Now upload
  $ dpm push 
  Pushing to ...

Working on existing::

  $ dpm clone {url} {path}
  ...
  $ edit some files
  
  $ dpm add {changed files}
  $ dpm push ...

Source package layout
~~~~~~~~~~~~~~~~~~~~~

Same as normal package but in addition have .dpm directory::

  datapackage.json
  .dpm/
    config
    manifest
  
.dpm/config file
~~~~~~~~~~~~~~~~

Looks like::

  [remote]
  # ckan url
  url = http://test.ckan.org/

.dpm/manifest
~~~~~~~~~~~~~

List of files that we manage and their connection to remote webstore. On push this needs to sync with datapackage.json::

  {resource} 
      local_path
      webstore_url
      state: new, unchanged, changed, deleted
      syncinfo: {
          unique_columns:
      }


Questions
~~~~~~~~~

* Duplication of datapackage.json and .dpm/config and .dpm/manifest?

