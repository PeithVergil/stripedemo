import logging

from concurrent import futures
from tornado.web import Application
from tornado.ioloop import IOLoop

from .routes import build_routes
from .settings import (
    ENV,
    PORT,
    DEBUG,
    SECRET,
    STATIC_PATH,
    TEMPLATE_PATH,
)
from .auth.provider import AuthProvider
from .home.provider import StripeProvider
from .session.provider import SessionProvider


if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class StripeDemo:

    executor = futures.ThreadPoolExecutor(4)

    @property
    def app(self):
        _app = getattr(self, '_app', None)
        if _app is None:
            _app = Application(build_routes(self), **self.settings)
            setattr(self, '_app', _app)
        return _app

    @property
    def auth(self):
        _auth = getattr(self, '_auth', None)
        if _auth is None:
            _auth = AuthProvider(self)
            setattr(self, '_auth', _auth)
        return _auth

    @property
    def loop(self):
        _loop = getattr(self, '_loop', None)
        if _loop is None:
            _loop = IOLoop.current()
            setattr(self, '_loop', _loop)
        return _loop

    @property
    def stripe(self):
        _stripe = getattr(self, '_stripe', None)
        if _stripe is None:
            _stripe = StripeProvider()
            setattr(self, '_stripe', _stripe)
        return _stripe

    @property
    def session(self):
        _session = getattr(self, '_session', None)
        if _session is None:
            _session = SessionProvider(self)
            setattr(self, '_session', _session)
        return _session

    @property
    def settings(self):
        """
        Tornado application settings.

        See:
        http://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings
        """
        logger.info('Loading settings file: {}'.format(ENV))

        _settings = getattr(self, '_settings', None)
        if _settings is None:
            #
            # General settings.
            #
            _settings = dict(debug=DEBUG)

            #
            # Static file settings.
            #
            _settings['static_path'] = STATIC_PATH

            #
            # Template file settings.
            #
            _settings['template_path'] = TEMPLATE_PATH

            #
            # Authentication and security settings.
            #
            _settings['cookie_secret'] = SECRET

            # Cache the application settings.
            setattr(self, '_settings', _settings)
        return _settings

    def run(self, func, *args, **kwargs):
        """
        Run the callable "func" in a separate thread.
        """
        return self.loop.run_in_executor(self.executor, func, *args, **kwargs)

    def start(self):
        logger.info('Listening on port: {}'.format(PORT))

        self.app.listen(PORT)
        self.loop.start()
