from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datapkg.package import Package, metadata
Session = sessionmaker()

class Index(object):
    def __init__(self, dburi):
        self.dburi = dburi
        self.engine = create_engine(self.dburi)
        Session.configure(bind=self.engine)
        self.session = Session()

    def init(self):
        metadata.create_all(bind=self.engine)

    def list_packages(self):
        return self.session.query(Package).all()

    def register(self, pkg):
        self.session.save(pkg)
        self.session.commit()

    def has_package(self, pkg_name):
        num = self.session.query(Package).filter_by(name=pkg_name).count()
        return num > 0

    def get_package(self, pkg_name):
        pkg = self.session.query(Package).filter_by(name=pkg_name).first()
        # self.session.expunge(pkg)
        # self.session.close()
        self.session.update(pkg)
        return pkg

