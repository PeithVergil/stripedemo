import secrets

from datetime import datetime, timedelta

from stripedemo.core.models import database
from stripedemo.session.models import Session

from .base import BaseTestCase


class SessionMixin:

    def create(self, expires=None):
        return Session.new(
            secrets.token_hex(16),
            secrets.token_hex(16),
        )

    def validate(self, session):
        self.assertNotEqual(session.id, 0)
        self.assertNotEqual(session.key, '')
        self.assertNotEqual(session.val, '')


class TestSession(BaseTestCase, SessionMixin):

    """
    python -m unittest tests.test_session_models.TestSession
    """

    def test_new(self):
        session = self.create()
        self.validate(session)

        # Clean up sample data.
        session.delete_instance()

    def test_rm(self):
        session = self.create()
        self.validate(session)

        # Clean up sample data.
        self.assertEqual(Session.rm(session.key), 1)


class TestSessionFetch(BaseTestCase, SessionMixin):

    """
    python -m unittest tests.test_session_models.TestSessionFetch
    """

    def setUp(self):
        self._session = self.create()

    def tearDown(self):
        # Clean up sample data.
        self._session.delete_instance()

    def test_fetch(self):
        session = Session.fetch(self._session.key)
        self.assertIsNotNone(session)
        self.assertEqual(session.key, self._session.key)
        # Value is a binary since it got pickled.
        self.assertEqual(session.val, self._session.val.encode())


class TestSessionFetchExpired(BaseTestCase, SessionMixin):

    """
    python -m unittest tests.test_session_models.TestSessionFetchExpired
    """

    def setUp(self):
        # Create an expired session.
        exp = datetime.utcnow() - timedelta(hours=1)
        with database:
            self._session = Session.create(
                key=secrets.token_hex(16),
                val=secrets.token_hex(16),
                exp=exp,
            )

    def tearDown(self):
        # Clean up sample data.
        self._session.delete_instance()

    def test_fetch(self):
        self.assertIsNone(Session.fetch(self._session.key))


class TestSessionExists(BaseTestCase, SessionMixin):

    """
    python -m unittest tests.test_session_models.TestSessionExists
    """

    def setUp(self):
        self._session = self.create()

    def tearDown(self):
        # Clean up sample data.
        self._session.delete_instance()

    def test_exists(self):
        self.assertTrue(Session.exists(self._session.key))

    def test_exists_notfound(self):
        self.assertFalse(Session.exists('key_notfound'))


class TestSessionExistsExpired(BaseTestCase, SessionMixin):

    """
    python -m unittest tests.test_session_models.TestSessionExistsExpired
    """

    def setUp(self):
        # Create an expired session.
        exp = datetime.utcnow() - timedelta(hours=1)
        with database:
            self._session = Session.create(
                key=secrets.token_hex(16),
                val=secrets.token_hex(16),
                exp=exp,
            )

    def tearDown(self):
        # Clean up sample data.
        self._session.delete_instance()

    def test_exists_expired(self):
        self.assertFalse(Session.exists(self._session.key))
