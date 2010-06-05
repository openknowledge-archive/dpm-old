from base import *


class DbIndex(IndexBase):
    '''Database-based index.
    '''
    def __init__(self, dburi):
        # import here as we do not want to require sqlalchemy
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        self.dburi = dburi
        self.engine = create_engine(self.dburi)
        print self.engine
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def init(self):
        from datapkg.db import dbmetadata
        dbmetadata.create_all(bind=self.engine)

    # TODO: DEPRECATE or limit number of results
    def list(self):
        return self.session.query(Package).all()

    def register(self, package):
        self.session.add(package)
        self.session.commit()

    def update(self, package):
        self.session.merge(package)
        self.session.commit()

    def has(self, pkg_name):
        num = self.session.query(Package).filter_by(name=pkg_name).count()
        return num > 0

    def get(self, pkg_name):
        pkg = self.session.query(Package).filter_by(name=pkg_name).first()
        # no package may exist with that name
        if pkg:
            self.session.update(pkg)
        return pkg
    
    def search(self, query):
        q = self.session.query(Package).filter(
                Package.name.ilike(u'%' + query + u'%')
                )
        q = q.limit(100)
        pkgs = q.all()
        return pkgs

# TODO: 2009-07-31 remove at some point
# for backwards compatibility
Index = DbIndex


