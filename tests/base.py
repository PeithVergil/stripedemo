from unittest import TestCase

from tornado.testing import AsyncTestCase, AsyncHTTPTestCase

from stripedemo import app


class TestMixin(object):

    @property
    def main(self):
        _main = getattr(self, '_main', None)
        if _main is None:
            _main = app.StripeDemo()
            setattr(self, '_main', _main)
        return _main

    @property
    def stripe(self):
        return self.main.stripe

    @property
    def session(self):
        return self.main.session

    @property
    def storage(self):
        return self.main.session.store


class BaseTestCase(TestMixin, TestCase):
    pass


class BaseAsyncTestCase(TestMixin, AsyncTestCase):
    pass


class BaseAsyncHttpTestCase(TestMixin, AsyncHTTPTestCase):

    def get_app(self):
        return self.main.app
