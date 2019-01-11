from ..core.handlers import BaseRequestHandler

from ..settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from .provider import stripe_provider


class Index(BaseRequestHandler):

    def get(self):
        self.render(
            'home/index.html',
            stripe_public_key=STRIPE_PUBLIC_KEY,
            stripe_secret_key=STRIPE_SECRET_KEY,
        )


class Order(BaseRequestHandler):

    def post(self):
        sku = self.get_argument('sku')
        name = self.get_argument('name')
        email = self.get_argument('email')

        card = self.get_argument('stripeCard')
        token = self.get_argument('stripeToken')

        customer = stripe_provider.create_customer(
            email=email,
            source=token,
            metadata=dict(
                name=name,
                user_id=123456,
            ),
        )

        order = stripe_provider.create_order(
            [
                {
                    'type': 'sku',
                    'parent': sku,
                }
            ],
            customer,
            metadata={
                'order_id': 12345,
                'product': 'Platinum',
                'artist': 'Sample Artist',
                'track': 'Sample Track',
            },
        )

        self.write(dict(
            card=card,
            token=token,
            status='token_invalid',
            message='The given access token does not '
                    'exist or may have already expired.',
            order=order,
            customer=customer,
        ))
