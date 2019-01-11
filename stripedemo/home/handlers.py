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

        if order.status == 'created':
            self.order_done(order)
        else:
            self.order_fail()

    def order_done(self, order):
        self.write(dict(
            data=order,
            status='order_successful',
            message='A new order has been created.',
        ))

    def order_fail(self):
        self.set_status(400)
        self.write(dict(
            status='order_failed',
            message='Unable to create a new order.',
        ))
