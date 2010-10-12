import sqlite3
try:
    import json
except:
    import simplejson as json
import uuid

import datapkg.package
from base import *


class DbIndexSqlite(IndexBase):
    '''A simple Database-based index using sqlite with no external library dependencies'''
    __db_version__ = 1
    def __init__(self, dburi=None):
        '''
        :param dburi: sqlalchemy type db uri (if not provided use db.dburi
        config variable.
        '''
        if dburi is not None: 
            self.dburi = dburi
        else:
            self.dburi = datapkg.CONFIG.get('index:db', 'db.dburi')
        self.dburi = self.dburi.replace('sqlite://', '')
    
    create_script = '''
    CREATE TABLE package (
        id TEXT NOT NULL, 
        name TEXT NOT NULL,
        metadata TEXT,
        search_field TEXT,
        manager_metadata TEXT,
        PRIMARY KEY (id)
    );

    CREATE TABLE setting (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value TEXT
    );

    INSERT INTO setting (name, value) VALUES ('db_version', '%s');
    ''' % __db_version__

    @property
    def conn(self):
        return sqlite3.connect(self.dburi)

    def init(self):
        try:
            # test for table existence
            arow = self.conn.execute('select * from package limit 1;').fetchall()
        except sqlite3.OperationalError, inst:
            self.conn.executescript(self.create_script)

    def _decode(self, metadata):
        if not metadata:
            out = {}
        else:
            out = json.loads(metadata.decode('utf8').replace("''", "'"))
        return out

    def _encode(self, metadata):
        out = json.dumps(metadata)
        out = out.encode('utf8')
        # see http://www.sqlite.org/faq.html#q14 - sql standard escapes single
        # quotes with ''
        out = out.replace("'", "''")
        return out

    def has(self, name):
        arow = self.conn.execute('select id from package where name = "%s";' % name).fetchall()
        return bool(arow)

    def _row_to_package(self, row):
        pkg = datapkg.package.Package(name=row[1], id=row[0])
        for k,v in self._decode(row[2]).items():
            setattr(pkg,k,v)
        for k,v in self._decode(row[4]).items():
            setattr(pkg,k,v)
        return pkg

    def get(self, name):
        # sql injection?
        results = self.conn.execute('select * from package where name = "%s";' % name).fetchall()
        if not results:
            return None
        else:
            row = results[0]
            return self._row_to_package(row)

    def register(self, pkg):
        metadata = self._encode(pkg.metadata)
        manager_metadata = self._encode(pkg.manager_metadata)
        sql = '''INSERT INTO package (id, name, metadata, search_field, manager_metadata) 
    VALUES ('%s', '%s', '%s', '%s', '%s');''' % (
                # pkg may not yet have id (new change)
                getattr(pkg, 'id',
                uuid.uuid4()),
                pkg.name,
                metadata,
                '',
                manager_metadata
                )
        out = self.conn.executescript(sql)
        self.conn.close()

    def update(self, pkg):
        # TODO: update search_field?
        metadata = self._encode(pkg.metadata)
        manager_metadata = self._encode(pkg.manager_metadata)
        sql = "UPDATE package SET "
        updates = [
                ('name', pkg.name),
                ('metadata', metadata),
                ('manager_metadata', manager_metadata),
                ]
        sql += ','.join([ "%s = '%s'" % (col,val) for col,val in updates ])
        sql += " WHERE name = '%s';" % pkg.name
        out = self.conn.executescript(sql)
        self.conn.close()

    def list(self):
        # TODO: an iterator?
        rows = self.conn.execute('select * from package').fetchall()
        return [ self._row_to_package(r) for r in rows ]

    def search(self, query):
        rows = self.conn.execute("select * from package where name LIKE '%%%s%%'" % query)
        return [ self._row_to_package(r) for r in rows ]


class DbIndexSqlalchemy(IndexBase):
    '''Database-based index using sqlalchemy.
    '''
    def __init__(self, dburi=None):
        '''
        :param dburi: sqlalchemy db uri (if not provided use variable from
        datapkg.CONFIG)
        '''
        # import here as we do not want to require sqlalchemy
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        if dburi is not None: 
            self.dburi = dburi
        else:
            self.dburi = datapkg.CONFIG.get('index:db', 'db.dburi')
        self.engine = create_engine(self.dburi)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def init(self):
        from datapkg.db import dbmetadata
        dbmetadata.bind = self.engine
        dbmetadata.create_all(bind=self.engine)

    def list(self):
        return self.session.query(Package)

    def register(self, package):
        self.session.add(package)
        self.session.commit()

    def update(self, package):
        self.session.merge(package)
        self.session.commit()

    def has(self, name):
        num = self.session.query(Package).filter_by(name=name).count()
        return num > 0

    def get(self, name):
        pkg = self.session.query(Package).filter_by(name=name).first()
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

