# SQLAlchemy stuff
from sqlalchemy import Column, MetaData, Table, types, ForeignKey
from sqlalchemy import orm


import simplejson
class JsonType(types.TypeDecorator):
    '''Store data as JSON serializing on save and unserializing on use.
    '''
    impl = types.UnicodeText

    def process_bind_param(self, value, engine):
        # None or {}
        if not value:
            return None
        else:
            # ensure_ascii=False => allow unicode but still need to convert
            return unicode(simplejson.dumps(value, ensure_ascii=False))

    def process_result_value(self, value, engine):
        if value is None:
            return None
        else:
            return simplejson.loads(value)

    def copy(self):
        return JsonType(self.impl.length)

# Instantiate meta data manager.
dbmetadata = MetaData()

package_table = Table('package', dbmetadata,
    Column('id', types.Integer, primary_key=True),
    Column('name', types.Unicode(255)),
    Column('installed_path', types.UnicodeText()),
    Column('metadata', JsonType()),
#     Column('description', types.UnicodeText()),
#     Column('notes', types.UnicodeText()),
#     Column('url', types.UnicodeText()),
#     Column('download_url', types.UnicodeText()),
#     Column('license', types.UnicodeText()),
#     Column('tags', types.UnicodeText()),
)


from sqlalchemy.orm import MapperExtension, EXT_STOP
class ReconstituteExtension(MapperExtension):
    def populate_instance(self, mapper, selectcontext, row, instance, **flags):
        # in v0.5 we can change to use on_reconstitute see
        # http://www.sqlalchemy.org/docs/05/mappers.html#advdatamapping_mapper_onreconstitute

        # here we follow
        # http://www.sqlalchemy.org/docs/04/sqlalchemy_orm_mapper.html#docstrings_sqlalchemy.orm.mapper_Mapper
        mapper.populate_instance(selectcontext, instance, row, **flags)
        instance.init_on_load()
        return EXT_STOP

from sqlalchemy.orm import mapper

