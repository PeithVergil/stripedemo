import peewee

from ..core.models import BaseModel


class Customer(BaseModel):

    # Example:
    #
    # user@example.com
    email = peewee.CharField(100, unique=True)

    # Example:
    #
    # cus_ETZvkwcsxFRiSG
    customer_id = peewee.CharField(50)

    date_created = peewee.DateTimeField()
    date_updated = peewee.DateTimeField()

    def __str__(self):
        return 'Customer(id={}, email={}, customer_id={})'.format(
            self.id, self.email, self.customer_id,
        )
