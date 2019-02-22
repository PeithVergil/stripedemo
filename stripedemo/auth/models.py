import logging
import secrets

from datetime import datetime, timedelta

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegrityError,
)

from ..core.models import BaseModel, database


logger = logging.getLogger(__name__)


class User(BaseModel):
    username = CharField(max_length=90, unique=True)
    password = CharField(max_length=90)

    @staticmethod
    def new(username, password):
        with database:
            try:
                return User.create(
                    username=username,
                    password=password,
                )
            except IntegrityError:
                return None

    @staticmethod
    def rm(username):
        query = (
            User
            .delete()
            .where(
                User.username == username
            )
        )
        return query.execute()

    @property
    def auth_tokens(self):
        return (
            self.tokens
            .where(
                Token.expiry > datetime.utcnow()
            )
            .where(
                Token.type == 'auth'
            )
        )

    def __str__(self):
        return 'User(id={}, username={})'.format(self.id, self.username)


class Token(BaseModel):
    user = ForeignKeyField(User, backref='tokens')

    # Example:
    #
    # auth, reset, etc
    type = CharField(max_length=10)
    value = CharField(max_length=255)
    expiry = DateTimeField()
    refresh = CharField(max_length=255, null=True)

    @staticmethod
    def new(user,
            value,
            token_type='auth',
            token_expire=None,
            token_refresh=None):
        if token_expire is None:
            token_expire = 3600

        expiry = datetime.utcnow() + timedelta(seconds=token_expire)

        try:
            return Token.create(
                user=user,
                type=token_type,
                value=value,
                expiry=expiry,
            )
        except IntegrityError:
            logger.exception('Failed to save access token: {}'.format(value))
            return None

    @staticmethod
    def rm(value):
        with database:
            query = (
                Token
                .delete()
                .where(
                    Token.value == value
                )
            )
            return query.execute()

    class Meta:
        # These three fields must be unique together.
        indexes = (
            (('user', 'type', 'value'), True),
        )

    def __str__(self):
        return 'Token(user={}, type={}, value={}, expiry={})'.format(
            self.user, self.type, self.value, self.expiry
        )
