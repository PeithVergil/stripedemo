from datetime import datetime, timedelta

from peewee import BlobField, CharField, DateTimeField

from ..core.models import BaseModel, database


class Session(BaseModel):
    key = CharField(max_length=128, unique=True)
    val = BlobField()

    # The expiration date.
    exp = DateTimeField(null=True)

    @staticmethod
    def exists(key):
        now = datetime.utcnow()

        with database:
            query = (
                Session
                .select()
                .where(
                    Session.key == key
                )
                .where(
                    Session.exp >= now
                )
            )
            return query.exists()

    @staticmethod
    def fetch(key):
        now = datetime.utcnow()

        with database:
            query = (
                Session
                .select()
                .where(
                    Session.key == key
                )
                .where(
                    Session.exp >= now
                )
            )
            try:
                return query.get()
            except Session.DoesNotExist:
                return None

    @staticmethod
    def edit(key, val):
        with database:
            query = (
                Session
                .update(
                    val=val
                )
                .where(
                    Session.key == key
                )
            )
            return query.execute()

    @staticmethod
    def new(key, val, expires=None):
        now = datetime.utcnow()

        if expires is not None:
            exp = now + timedelta(seconds=expires)
        else:
            exp = now + timedelta(hours=1)

        with database:
            return Session.create(
                key=key,
                val=val,
                exp=exp,
            )

    @staticmethod
    def rm(key):
        with database:
            query = (
                Session
                .delete()
                .where(
                    Session.key == key
                )
            )
            return query.execute()

    def __str__(self):
        return 'Session(id={}, key={})'.format(self.id, self.key)
