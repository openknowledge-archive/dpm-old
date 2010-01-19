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

4. Take a look at the manual::

    $ datapkg man

