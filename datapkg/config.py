import os
import ConfigParser

import datapkg
default_root_path = os.path.join(os.path.expanduser('~'), '.datapkg')
default_config_path = os.path.join(os.path.expanduser('~'), '.datapkgrc')
default_repo_path = os.path.join(default_root_path, 'repository')

class Config(ConfigParser.SafeConfigParser):
    def dictget(self, section, option, default=None):
        '''Emulate `dict.get` on SafeConfigParser.

        :param section: as on SafeConfigParser.get
        :param option: ditto
        :param default: default value if option does not exist
        '''
        if self.has_option(section, option):
            return self.get(section, option)
        else:
            return default

def load_config(config_path=default_config_path):
    '''Load configuration from ini-style config file at `config_path` if it
    exists else returns default config (`make_default_config`).
    :param config_path: path to config on disk.
    :return: loaded config.
    '''
    config = None
    if os.path.exists(config_path):
        config = Config()
        config.readfp(open(config_path))
    else:
        # intentionally do not write to disk
        # creation of config on disk should be an *explicit* action
        config = make_default_config()
    return config

def make_default_config(repo_path=default_repo_path):
    '''Create default ConfigParser config.'''
    cfg = Config()
    cfg.add_section('datapkg')
    cfg.add_section('index:ckan')
    cfg.add_section('index:db')
    cfg.add_section('upload:ckan')
    cfg.set('datapkg', 'repo.default_path', repo_path)
    cfg.set('datapkg', 'index.default', 'file')
    cfg.set('index:ckan', 'ckan.url',  'http://ckan.net/api/')
    cfg.set('index:ckan', 'ckan.api_key', '')
    cfg.set('index:db', 'db.dburi', 'sqlite://%s/index.db' % repo_path)
    cfg.set('index:db', 'db.dburi', 'sqlite://%s/index.db' % repo_path)
    cfg.set('upload:ckan', 'ofs.backend', 'reststore')
    cfg.set('upload:ckan', 'host', 'http://storage.ckan.net')
    return cfg

def write_default_config(path=default_config_path, repo_path=default_repo_path):
    '''Write default config (`make_default_config`) to location on disk.
    '''
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

