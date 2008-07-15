from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datapkg.package import Package, metadata
Session = sessionmaker()

class Index(object):
    def __init__(self, dburi):
        self.dburi = dburi
        self.engine = create_engine(self.dburi)
        Session.configure(bind=self.engine)

    def init(self):
        print self.dburi
        print self.engine
        metadata.create_all(bind=self.engine)

    def list_packages(self):
        session = Session()
        return session.query(Package).all()

    def register(self, pkg):
        session = Session()
        session.merge(pkg)
        session.commit()

