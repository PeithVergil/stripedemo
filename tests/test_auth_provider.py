from tornado.testing import gen_test

from stripedemo.auth.models import Token
from stripedemo.auth.provider import (
    password_hash,
    password_check,
)
from stripedemo import settings

from .base import BaseTestCase, BaseAsyncTestCase


class TestPasswordUtils(BaseTestCase):

    """
    To run this test:

        python -m tornado.testing tests.test_auth_provider.TestPasswordUtils
    """

    def test_hash(self):
        unhashed_password = 'abcdef'
        hashed_password = password_hash(unhashed_password, 'f7e51bde')
        self.assertEqual(
            hashed_password,
            'f7e51bde$04C800796024574AD453F8A18C2E'
            'FFA0C75C8B64F4338C230E5E20EF0BB9E0ED'
        )
        self.assertTrue(password_check(unhashed_password, hashed_password))

    def test_check(self):
        unhashed_password = 'abcdef'
        hashed_password = (
            'de6e85d899d8e5c8$B49B8AD5FDF9141C83F6F41'
            'B1CE62F3228F4595E56BA7DF2C9FD7549F1D3369E'
        )
        self.assertTrue(password_check(unhashed_password, hashed_password))


class BaseAuthProviderTest(BaseAsyncTestCase):

    @property
    def auth(self):
        return self.main.auth


class TestLogin(BaseAuthProviderTest):

    """
    To run this test:

        python -m tornado.testing tests.test_auth_provider.TestLogin
    """

    @gen_test(timeout=10)
    def test_login(self):
        result = yield self.auth.login(
            settings.TEST_USERNAME,
            settings.TEST_PASSWORD,
        )
        import pdb; pdb.set_trace()
        self.assertIsNotNone(result)

    @gen_test(timeout=10)
    def test_login_failed(self):
        result = yield self.auth.login('invalid_user', 'invalid_pass')
        self.assertIsNone(result)


class TestSaveToken(BaseAuthProviderTest):

    """
    To run this test:

        python -m tornado.testing tests.test_auth_provider.TestSaveToken
    """

    token = dict(
        access_token='KYWke1VXGIWMICenIww2iNjL6B94AL',
        refresh_token='wI8XxuU6yAM8GAvmuLupLrDMIzQmSg',
    )

    def tearDown(self):
        super().tearDown()
        # Clean up sample data.
        self.assertEqual(Token.rm(self.token['access_token']), 1)

    @gen_test(timeout=10)
    def test_save(self):
        user = yield self.auth.authenticate('test_user', 'test_pass')
        result = yield self.auth.save_token(user, self.token)
        self.assertTrue(result)


class TestAuthenticate(BaseAuthProviderTest):

    """
    To run this test:

        python -m tornado.testing tests.test_auth_provider.TestAuthenticate
    """

    @gen_test(timeout=10)
    def test_authentication(self):
        result = yield self.auth.authenticate(
            settings.TEST_USERNAME,
            settings.TEST_PASSWORD,
        )
        import pdb; pdb.set_trace()
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.token)
        self.assertIsNotNone(result.user)

    @gen_test(timeout=10)
    def test_authentication_failed(self):
        result = yield self.auth.authenticate('invalid_user', 'invalid_pass')
        self.assertIsNone(result)


class TestFetchUserInfo(BaseAuthProviderTest):

    """
    To run this test:

        python -m tornado.testing tests.test_auth_provider.TestFetchUserInfo
    """

    @gen_test(timeout=10)
    def test_fetch_user(self):
        token = 'BHUfiiO0no54IItY12ydYYbEUS9Lmx'
        result = yield self.auth.fetch_user_info(token)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.id)

    @gen_test(timeout=10)
    def test_fetch_profile(self):
        token = 'BHUfiiO0no54IItY12ydYYbEUS9Lmx'
        result = yield self.auth.fetch_user_profile(token)
        self.assertIsNotNone(result)

    @gen_test(timeout=10)
    def test_fetch_contact(self):
        token = 'BHUfiiO0no54IItY12ydYYbEUS9Lmx'
        result = yield self.auth.fetch_user_profile(token)
        self.assertIsNotNone(result)

        result = yield self.auth.fetch_user_contact(token, result)
        self.assertIsNotNone(result)

    @gen_test(timeout=10)
    def test_fetch_failed(self):
        token = 'INVALIDACCESSTOKEN'
        result = yield self.auth.fetch_user_info(token)
        self.assertIsNone(result)
