import logging

from tornado.web import RequestHandler


logger = logging.getLogger(__name__)


class BaseRequestHandler(RequestHandler):

    def initialize(self, **kwargs):
        self.main = kwargs.get('main')

    def get_current_user(self):
        session_token = self.get_secure_cookie('session')

        logger.info('Fetching user session: {}'.format(session_token))

        if session_token:
            # Grab the user info from the cache.
            user = self.storage.get(session_token.decode())
            if user:
                logger.info('Found user session: {}'.format(user))
                return user
        return None

    @property
    def auth(self):
        return self.main.auth

    @property
    def session(self):
        return self.main.session

    @property
    def storage(self):
        return self.main.session.store
