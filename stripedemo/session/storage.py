import json
import pickle

from .models import Session


class Storage:

    prefix = 'STORAGE_'

    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, val, expire=None):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def exists(self, key):
        raise NotImplementedError

    def _key(self, key):
        return '{}{}'.format(self.prefix, key)

    def _dump(self, val):
        try:
            return json.dumps(val)
        except TypeError:
            return False

    def _load(self, val):
        try:
            return json.loads(val)
        except TypeError:
            return None


class DatabaseSession(Storage):

    prefix = 'DATABASE_SESSION_'

    def set(self, key, val, expires=None):
        result = self._update(key, val)
        if not result:
            result = self._create(key, val, expires)
            if not result:
                return False
        return True

    def get(self, key, default=None):
        session = Session.fetch(self._key(key))
        if not session:
            return default
        return self._load(session.val)

    def delete(self, key):
        rows_deleted = Session.rm(self._key(key))
        if rows_deleted == 0:
            return False
        return True

    def exists(self, key):
        return Session.exists(self._key(key))

    def _update(self, key, val):
        result = Session.edit(
            self._key(key), self._dump(val)
        )
        if not result:
            return False
        return True

    def _create(self, key, val, expires):
        result = Session.new(
            self._key(key), self._dump(val), expires
        )
        if not result:
            return False
        return True

    def _dump(self, val):
        try:
            return pickle.dumps(val)
        except TypeError:
            return False

    def _load(self, val):
        try:
            return pickle.loads(val)
        except TypeError:
            return None
