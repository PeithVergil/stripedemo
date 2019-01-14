import logging

from tornado.web import RequestHandler


logger = logging.getLogger(__name__)


class BaseRequestHandler(RequestHandler):

    def initialize(self, **kwargs):
        self.main = kwargs.get('main')


class SessionRequiredMixin:

    def get_current_user(self):
        session_token = self.get_secure_cookie('session')
        if session_token:
            # Grab the user info from the cache.
            user = self.storage.cache.get(session_token.decode())
            if user:
                return user
        return None
