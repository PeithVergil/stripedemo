import random

from ..core.decorators import login_required
from ..core.handlers import BaseRequestHandler

from ..settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY


class Index(BaseRequestHandler):

    @login_required
    def get(self):
        self.render(
            'subs/index.html',
            stripe_public_key=STRIPE_PUBLIC_KEY,
            stripe_secret_key=STRIPE_SECRET_KEY,
        )


class Subscribe(BaseRequestHandler):

    @login_required
    def post(self):
        if not self.create_stripe_customer():
            self.set_status(400)
            self.write(dict(
                status='customer_failed',
                message='Unable to create a new Stripe customer.',
            ))
            return

        if not self.create_stripe_subscription():
            self.set_status(400)
            self.write(dict(
                status='subscription_failed',
                message='Unable to create a new Stripe subscription.',
            ))
            return

        self.write(dict(
            data=self.subs,
            status='subscription_successful',
            message='A new Stripe subscription has been created.',
        ))

    def create_stripe_customer(self):
        user = self.current_user
        name = self.get_argument('name')
        token = self.get_argument('stripeToken')

        self.customer = self.stripe.verify_customer(
            user=user,
            source=token,
            metadata=dict(
                name=name,
                user_id=user['id'],
            ),
        )
        if self.customer is None:
            return False
        return True

    def create_stripe_subscription(self):
        sku = self.get_argument('sku')

        # TODO: Use an actual subscription ID.
        subs_id = random.randint(1, 999999)

        self.subs = self.stripe.create_subscription(
            [
                {
                    'price': sku,
                }
            ],
            self.customer.customer_id,
            metadata={
                'subs_id': subs_id,
                'product': 'Avenger Subscription',
                'artist': 'Sample Artist',
                'track': 'Sample Track',
            },
        )
        if self.subs is None:
            return False
        
        self.stripe.insert_subscription(self.customer.id, self.subs['id'])

        return True


class Subscriptions(BaseRequestHandler):

    @login_required
    def get(self):
        subs = self.subs.all()

        self.render('subs/subscriptions.html', subs=subs)
