import datapkg.index.ckan


class TestCkanIndex:
    '''Read only test.
    
    Don't want to duplicate too much of what is in ckanclient tests
    '''
    __external__ = True

    index = datapkg.index.ckan.CkanIndex('http://ckan.net/api')

    def test_get(self):
        name = u'ckan'
        out = self.index.get(name)
        assert out.name == name

    def test_search(self):
        out = [ x for x in self.index.search('ckan') ]
        assert len(out) >= 3, out
        assert out[0].name in [u'ckan', u'ckanclient'], out[0]

