from ..core.handlers import BaseRequestHandler

from ..settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY


class Index(BaseRequestHandler):

    def get(self):
        self.render(
            'home/index.html',
            stripe_public_key=STRIPE_PUBLIC_KEY,
            stripe_secret_key=STRIPE_SECRET_KEY,
        )


class Order(BaseRequestHandler):

    def post(self):
        self.write(dict(
            status='token_invalid',
            message='The given access token does not '
                    'exist or may have already expired.',
        ))
