import stripe

from ..settings import STRIPE_SECRET_KEY


stripe.api_key = STRIPE_SECRET_KEY


class StripeProvider:

    def create_customer(self, email, source, metadata=None):
        customer = stripe.Customer.create(
            email=email,
            source=source,
            metadata=metadata,
            description='We have a new customer.',
        )
        return customer

    def create_order(self, items, customer, metadata=None, currency='usd'):
        order = stripe.Order.create(
            items=items,
            currency=currency,
            customer=customer,
            metadata=metadata,
        )
        return order


stripe_provider = StripeProvider()
