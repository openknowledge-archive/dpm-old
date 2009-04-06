import datapkg.metadata as M

class TestMetadata:
    def test_1(self):
        meta = M.Metadata()
        meta.name = 'abc'
        assert meta.name == 'abc', meta
        assert str(meta).startswith('{'), meta

