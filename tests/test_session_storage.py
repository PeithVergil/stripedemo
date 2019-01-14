import time
import secrets

from .base import BaseTestCase


def greetings(name):
    return 'Greetings! Hello, {}!'.format(name)


class Greetings:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return 'Greetings! Hello, {}!'.format(self.name)


class TestSessionSet(BaseTestCase):

    """
    python -m unittest tests.test_session_storage.TestSessionSet
    """

    def setUp(self):
        self.key = secrets.token_hex(16)
        self.val = dict(
            message='hello, world!'
        )

    def tearDown(self):
        # Clean up sample data.
        self.storage.delete(self.key)

    def test_set(self):
        self.assertTrue(self.storage.set(self.key, self.val))

    def test_set_class(self):
        self.assertTrue(self.storage.set(self.key, Greetings))

    def test_set_function(self):
        self.assertTrue(self.storage.set(self.key, greetings))


class TestSessionSetExisting(BaseTestCase):

    """
    Setting a value to an existing key should overwrite the value
    in the database.

    python -m unittest tests.test_session_storage.TestSessionSetExisting
    """

    def setUp(self):
        # Create sample data.
        self.key = secrets.token_hex(16)
        self.val = dict(
            number=123456,
            message='hello, world!'
        )
        self.assertTrue(self.storage.set(
            self.key,
            self.val,
        ))

    def tearDown(self):
        # Clean up sample data.
        self.storage.delete(self.key)

    def test_set(self):
        val = self.storage.get(self.key)
        self.assertEqual(val['number'], 123456)
        self.assertEqual(val['message'], 'hello, world!')

        # Overwrite sample data.
        self.val['number'] = 78910
        self.val['message'] = 'hello, galaxy!'
        self.assertTrue(self.storage.set(self.key, self.val))

        val = self.storage.get(self.key)
        self.assertEqual(val['number'], 78910)
        self.assertEqual(val['message'], 'hello, galaxy!')


class TestSessionGet(BaseTestCase):

    """
    python -m unittest tests.test_session_storage.TestSessionGet
    """

    def setUp(self):
        # Create sample data.
        self.key = secrets.token_hex(16)
        self.val = dict(
            number=123456,
            message='hello, world!'
        )
        self.assertTrue(self.storage.set(
            self.key,
            self.val,
        ))

    def tearDown(self):
        # Clean up sample data.
        self.storage.delete(self.key)

    def test_get(self):
        val = self.storage.get(self.key)
        self.assertEqual(val['number'], 123456)
        self.assertEqual(val['message'], 'hello, world!')

    def test_get_default(self):
        self.assertEqual(self.storage.get('key_notfound', 3), 3)

    def test_get_notfound(self):
        self.assertIsNone(self.storage.get('key_notfound'))


class TestSessionGetClass(BaseTestCase):

    """
    Fetch a pickled Python class from the database and try using it.

    python -m unittest tests.test_session_storage.TestSessionGetClass
    """

    def setUp(self):
        # Pickle a class into the database.
        self.key, self.val = secrets.token_hex(16), Greetings
        self.assertTrue(self.storage.set(
            self.key,
            self.val,
        ))

    def tearDown(self):
        # Clean up sample data.
        self.storage.delete(self.key)

    def test_get_class(self):
        # Unpickle a class from the database.
        _Class = self.storage.get(self.key)

        self.assertIsNotNone(_Class)

        instance = _Class('World')
        self.assertEqual(instance.greet(), 'Greetings! Hello, World!')

        instance = _Class('Python')
        self.assertEqual(instance.greet(), 'Greetings! Hello, Python!')


class TestSessionGetFunction(BaseTestCase):

    """
    Fetch a pickled Python function from the database and try calling it.

    python -m unittest tests.test_session_storage.TestSessionGetFunction
    """

    def setUp(self):
        # Pickle a function into the database.
        self.key, self.val = secrets.token_hex(16), greetings
        self.assertTrue(self.storage.set(
            self.key,
            self.val,
        ))

    def tearDown(self):
        # Clean up sample data.
        self.storage.delete(self.key)

    def test_get_function(self):
        # Unpickle a function from the database.
        func = self.storage.get(self.key)

        self.assertIsNotNone(func)
        self.assertEqual(func('World'), 'Greetings! Hello, World!')
        self.assertEqual(func('Python'), 'Greetings! Hello, Python!')


class TestSessionGetExpired(BaseTestCase):

    """
    Wait for a session item to expire, then try fetching it.

    python -m unittest tests.test_session_storage.TestSessionGetExpired
    """

    def setUp(self):
        # Create sample data that will expire in a second.
        self.key = secrets.token_hex(16)
        self.val = dict(
            number=123456,
            message='hello, world!'
        )
        self.exp = 1
        self.assertTrue(self.storage.set(
            self.key,
            self.val,
            self.exp,
        ))

    def tearDown(self):
        # Clean up sample data.
        self.storage.delete(self.key)

    def test_get_function(self):
        # Wait for the sample data to expire.
        time.sleep(self.exp + 1)

        # The sample data should no longer exist.
        self.assertIsNone(self.storage.get(self.key))


class TestSessionExists(BaseTestCase):

    """
    python -m unittest tests.test_session_storage.TestSessionExists
    """

    def setUp(self):
        # Create sample data.
        self.key = secrets.token_hex(16)
        self.val = dict(
            number=123456,
            message='hello, world!'
        )
        self.assertTrue(self.storage.set(
            self.key,
            self.val,
        ))

    def tearDown(self):
        # Clean up sample data.
        self.storage.delete(self.key)

    def test_exists(self):
        self.assertTrue(self.storage.exists(self.key))

    def test_exists_notfound(self):
        self.assertFalse(self.storage.exists('key_notfound'))


class TestSessionExistsExpired(BaseTestCase):

    """
    Wait for a session item to expire, then check if it exists.

    python -m unittest tests.test_session_storage.TestSessionExistsExpired
    """

    def setUp(self):
        # Create sample data that will expire in a second.
        self.key = secrets.token_hex(16)
        self.val = dict(
            number=123456,
            message='hello, world!'
        )
        self.exp = 1
        self.assertTrue(self.storage.set(
            self.key,
            self.val,
            self.exp,
        ))

    def tearDown(self):
        # Clean up sample data.
        self.storage.delete(self.key)

    def test_exists_expired(self):
        # Wait for the sample data to expire.
        time.sleep(self.exp + 1)

        # The sample data should no longer exist.
        self.assertFalse(self.storage.exists(self.key))


class TestSessionDelete(BaseTestCase):

    """
    python -m unittest tests.test_session_storage.TestSessionDelete
    """

    def setUp(self):
        # Create sample data.
        self.key = secrets.token_hex(16)
        self.val = dict(
            number=123456,
            message='hello, world!'
        )
        self.assertTrue(self.storage.set(
            self.key,
            self.val,
        ))

    def tearDown(self):
        # Clean up sample data.
        self.storage.delete(self.key)

    def test_delete(self):
        self.assertTrue(self.storage.delete(self.key))

    def test_delete_notfound(self):
        self.assertFalse(self.storage.delete('key_notfound'))
