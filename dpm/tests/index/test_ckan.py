import dpm.index.ckan


# TODO: mock these rather than rely on external access
class TestCkanIndex:
    '''Read only test.
    
    Don't want to duplicate too much of what is in ckanclient tests
    '''
    __external__ = True

    index = dpm.index.ckan.CkanIndex('http://thedatahub.org/api/')

    def test_get(self):
        name = u'ckan'
        out = self.index.get(name)
        assert out.name == name

    def test_search(self):
        out = [ x for x in self.index.search('ckanclient') ]
        assert len(out) == 1, out
        assert out[0].name in [u'ckanclient'], out[0]

