import random

from ..core.decorators import login_required
from ..core.handlers import BaseRequestHandler

from ..settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY


class Index(BaseRequestHandler):

    # @login_required
    def get(self):
        self.render(
            'home/index.html',
            stripe_public_key=STRIPE_PUBLIC_KEY,
            stripe_secret_key=STRIPE_SECRET_KEY,
        )


class Order(BaseRequestHandler):

    def post(self):
        if not self.create_stripe_customer():
            self.set_status(400)
            self.write(dict(
                status='customer_failed',
                message='Unable to create a new Stripe customer.',
            ))
            return

        if not self.create_stripe_order():
            self.set_status(400)
            self.write(dict(
                status='order_failed',
                message='Unable to create a new Stripe order.',
            ))
            return

        self.write(dict(
            data=self.order,
            status='order_successful',
            message='A new Stripe order has been created.',
        ))

    def create_stripe_customer(self):
        name = self.get_argument('name')
        email = self.get_argument('email')
        token = self.get_argument('stripeToken')

        # TODO: Use an actual user ID.
        user_id = random.randint(1, 999999)

        self.customer = self.stripe.verify_customer(
            email=email,
            source=token,
            metadata=dict(
                name=name,
                user_id=user_id,
            ),
        )
        if self.customer is None:
            return False
        return True

    def create_stripe_order(self):
        sku = self.get_argument('sku')

        # TODO: Use an actual order ID.
        order_id = random.randint(1, 999999)

        self.order = self.stripe.create_order(
            [
                {
                    'type': 'sku',
                    'parent': sku,
                }
            ],
            self.customer.customer_id,
            metadata={
                'order_id': order_id,
                'product': 'Platinum',
                'artist': 'Sample Artist',
                'track': 'Sample Track',
            },
        )
        if self.order is None:
            return False

        self.order.pay(customer=self.customer.customer_id)
        
        return True
