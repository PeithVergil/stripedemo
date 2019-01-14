import secrets

from tornado.testing import gen_test

from .base import BaseAsyncTestCase


def greetings(name):
    return 'Greetings! Hello, {}!'.format(name)


class Greetings:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return 'Greetings! Hello, {}!'.format(self.name)


class TestProvider(BaseAsyncTestCase):

    """
    To run this test:

        python -m tornado.testing tests.test_session_provider.TestProvider
    """

    def setUp(self):
        super().setUp()

        self.key = secrets.token_hex(8)
        self.val = dict(
            message='hello, world!'
        )

    def tearDown(self):
        super().tearDown()
        # Clean up sample data.
        self.storage.delete(self.key)

    @gen_test(timeout=10)
    def test_set(self):
        result = yield self.session.set(self.key, self.val)
        self.assertTrue(result)

    @gen_test(timeout=10)
    def test_set_class(self):
        result = yield self.session.set(self.key, Greetings)
        self.assertTrue(result)

    @gen_test(timeout=10)
    def test_set_function(self):
        result = yield self.session.set(self.key, greetings)
        self.assertTrue(result)


class TestSessionSetExisting(BaseAsyncTestCase):

    """
    Setting a value to an existing key should overwrite the value
    in the database.

    python -m unittest tests.test_session_provider.TestSessionSetExisting
    """

    def setUp(self):
        super().setUp()
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
        super().tearDown()
        # Clean up sample data.
        self.storage.delete(self.key)

    @gen_test(timeout=10)
    def test_set(self):
        val = yield self.session.get(self.key)
        self.assertEqual(val['number'], 123456)
        self.assertEqual(val['message'], 'hello, world!')

        # Overwrite sample data.
        self.val['number'] = 78910
        self.val['message'] = 'hello, galaxy!'
        result = yield self.session.set(self.key, self.val)
        self.assertTrue(result)

        val = yield self.session.get(self.key)
        self.assertEqual(val['number'], 78910)
        self.assertEqual(val['message'], 'hello, galaxy!')


class TestSessionGet(BaseAsyncTestCase):

    """
    python -m unittest tests.test_session_provider.TestSessionGet
    """

    def setUp(self):
        super().setUp()
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
        super().tearDown()
        # Clean up sample data.
        self.storage.delete(self.key)

    @gen_test(timeout=10)
    def test_get(self):
        val = yield self.session.get(self.key)
        self.assertEqual(val['number'], 123456)
        self.assertEqual(val['message'], 'hello, world!')

    @gen_test(timeout=10)
    def test_get_default(self):
        result = yield self.session.get('key_notfound', 3)
        self.assertEqual(result, 3)

    @gen_test(timeout=10)
    def test_get_notfound(self):
        result = yield self.session.get('key_notfound')
        self.assertIsNone(result)
