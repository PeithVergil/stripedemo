import logging

from ..home.models import Customer, Subscription


logger = logging.getLogger(__name__)


class SubsProvider:

    def __init__(self, main):
        self.main = main

    def all(self):
        logger.info('Selecting all subscriptions from the database.')
        return (
            Subscription
            .select()
            .join(Customer)
        )
