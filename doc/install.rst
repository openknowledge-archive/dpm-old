Installation
============

1. Install python: http://www.python.org/

2. Install setuptools library (and (optional) virtualenv)

3. Install datapkg
   
   Using setuptool's easy_install::

      $ easy_install datapkg
    
   Or to install with pip (http://pypi.python.org/pypi/pip)::

      $ pip install datapkg

   If you want it in a nice insulated virtualenv do instead::

      # set up virtualenv
      $ virtualenv your_virtual_env

      # EITHER (with easy_install)
      $ . your_virtual_env/bin/activate
      $ easy_install datapkg

      # OR (with pip) 
      $ pip -E your_virtual_env install datapkg

   NB: f you want to install from source datapkg's mercurial repository is
   here: http://knowledgeforge.net/ckan/datapkg

4. Extras (e.g. upload capabilities).
   
   If you want to use the upload capabilities you will need to install the OFS library::

      $ easy_install ofs
      # or
      $ pip install ofs

   You can also install plugins - see the project's home page for a current list.

5. Take a look at the manual::

    $ datapkg man

