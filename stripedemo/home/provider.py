import peewee
import stripe
import logging

from datetime import datetime

from ..settings import STRIPE_SECRET_KEY
from .models import Customer, Subscription


logger = logging.getLogger(__name__)


class StripeProvider:

    """
    A simple wrapper to the Stripe library.
    """

    def __init__(self):
        stripe.api_key = STRIPE_SECRET_KEY

    def verify_customer(self, user, source, metadata=None):
        customer = self.select_customer(user)
        if customer is None:
            customer = self.insert_customer(user, source, metadata)
        return customer

    def insert_customer(self, user, source, metadata=None):
        logger.info(
            'Inserting new customer info into the database: {}'.format(user['email'])
        )
        stripe_customer = self.create_stripe_customer(user['email'], source, metadata)
        if stripe_customer is None:
            return None

        now = datetime.utcnow()
        try:
            customer = Customer.create(
                user_id=user['id'],
                customer_id=stripe_customer.id,
                date_created=now,
                date_updated=now,
            )
        except peewee.DatabaseError as error:
            logger.exception(
                'Failed to insert a new customer into the database.'
            )
        else:
            logger.info('New customer: {}'.format(customer))
            return customer
        return None

    def select_customer(self, user):
        logger.info(
            'Selecting customer info from the database: {}'.format(user['email'])
        )
        query = (
            Customer
            .select()
            .where(Customer.user_id == user['id'])
        )

        customer = query.first()
        if customer is None:
            logger.info('Customer not found.')
            return None
        logger.info('Got customer: {}'.format(customer))
        return customer

    def create_order(self, items, customer, metadata=None, currency='usd'):
        order = stripe.Order.create(
            items=items,
            currency=currency,
            customer=customer,
            metadata=metadata,
        )
        return order
    
    def pay_order(self, order_id, customer_id):
        return stripe.Order.pay(order_id, customer=customer_id)
    
    def create_subscription(self, items, customer, metadata=None):
        order = stripe.Subscription.create(
            items=items,
            customer=customer,
            metadata=metadata,
        )
        return order
    
    def insert_subscription(self, customer_id, subscription_id):
        logger.info(
            'Inserting new subscription info into the database: {}'.format(subscription_id)
        )

        now = datetime.utcnow()
        try:
            subscription = Subscription.create(
                customer_id=customer_id,
                subscription_id=subscription_id,
                date_created=now,
                date_updated=now,
            )
        except peewee.DatabaseError as error:
            logger.exception(
                'Failed to insert a new subscription into the database.'
            )
        else:
            logger.info('New subscription: {}'.format(subscription))
            return subscription
        return None

    def create_stripe_customer(self, email, source, metadata=None):
        logger.info(
            'Creating a new Stripe customer: {}'.format(email)
        )
        try:
            stripe_customer = stripe.Customer.create(
                email=email,
                source=source,
                metadata=metadata,
                description='StripeDemo customer',
            )
        except stripe.error.StripeError as error:
            logger.exception('Failed to create a new Stripe customer.')
        else:
            logger.info('New Stripe customer: {}'.format(stripe_customer))
            return stripe_customer
        return None


stripe_provider = StripeProvider()
