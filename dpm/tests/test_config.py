import dpm
import dpm.config

class TestConfig:
    def test_make_default_config(self):
        cfg = dpm.config.make_default_config()
        assert set(cfg.sections()) == set(['dpm', 'index:ckan',
            'index:db', 'upload:ckan']), cfg.sections()
        assert cfg.get('index:ckan', 'ckan.url') == 'http://thedatahub.org/api/'

    def test_dictget(self):
        cfg = dpm.config.Config()
        default = 'ZZZZZZ'
        out = cfg.dictget('DEFAULT', 'xyz', default)
        assert out == default

