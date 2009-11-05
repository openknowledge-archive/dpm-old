import os
import ConfigParser

import datapkg
default_root_path = os.path.join(os.path.expanduser('~'), '.datapkg')
default_config_path = os.path.join(os.path.expanduser('~'), '.datapkgrc')
default_repo_path = os.path.join(default_root_path, 'repository')

def get_config(config_path=default_config_path):
    config = None
    if os.path.exists(config_path):
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(config_path))
    else:
        return make_default_config()
    return config

def make_default_config(repo_path=default_repo_path):
    cfg = ConfigParser.SafeConfigParser()
    cfg.set('DEFAULT', 'version', datapkg.__version__)
    cfg.set('DEFAULT', 'ckan.url',  'http://ckan.net/api/')
    cfg.set('DEFAULT', 'ckan.api_key', '')
    cfg.set('DEFAULT', 'repo.default_path', repo_path)
    return cfg

def write_default_config(path=default_config_path, repo_path=default_repo_path):
    if os.path.exists(path):
        msg = 'init() failed. It looks like you already ' + \
                'have configuration at %s' % path
        raise ValueError(msg)
    root_path = os.path.dirname(path)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    cfg = make_default_config(repo_path)
    cfg.write(file(path, 'w'))
    return cfg

