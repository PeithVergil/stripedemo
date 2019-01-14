from peewee import SqliteDatabase, Model

from ..settings import DATABASE


# Create a database connection.
# --------------------------------------------------------------
# See: http://docs.peewee-orm.com/en/latest/peewee/database.html
database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database
