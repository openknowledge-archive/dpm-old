# SQLAlchemy stuff
from sqlalchemy import Column, MetaData, Table, types, ForeignKey
from sqlalchemy import orm
# from sqlalchemy import __version__ as _sqla_version
# import pkg_resources
# _sqla_version = pkg_resources.parse_version(_sqla_version)


# Instantiate meta data manager.
dbmetadata = MetaData()

package_table = Table('package', dbmetadata,
    Column('id', types.UnicodeText, primary_key=True),
    Column('name', types.Unicode(255)),
    Column('installed_path', types.UnicodeText()),
#     Column('description', types.UnicodeText()),
#     Column('notes', types.UnicodeText()),
#     Column('url', types.UnicodeText()),
#     Column('download_url', types.UnicodeText()),
#     Column('license', types.UnicodeText()),
#     Column('tags', types.UnicodeText()),
)


from sqlalchemy.orm import MapperExtension, EXT_STOP
class ReconstituteExtension(MapperExtension):
    # v0.4
    def populate_instance(self, mapper, selectcontext, row, instance, **flags):
        # in v0.5 we can change to use on_reconstitute see
        # http://www.sqlalchemy.org/docs/05/mappers.html#constructors-and-object-initialization

        # here we follow
        # http://www.sqlalchemy.org/docs/04/sqlalchemy_orm_mapper.html#docstrings_sqlalchemy.orm.mapper_Mapper
        try: # v0.5 will raise exception
            mapper.populate_instance(selectcontext, instance, row, **flags)
            instance.init_on_load()
            return EXT_STOP
        except:
            pass

    # v0.5
    def reconstruct_instance(self, mapper, instance):
        instance.init_on_load()

from sqlalchemy.orm import mapper

from dpm.package import Package
mapper(Package, package_table, extension=ReconstituteExtension())

