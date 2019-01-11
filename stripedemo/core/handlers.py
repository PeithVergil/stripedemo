import logging

from tornado.web import RequestHandler


logger = logging.getLogger(__name__)


class BaseRequestHandler(RequestHandler):

    def initialize(self, **kwargs):
        self.main = kwargs.get('main')
