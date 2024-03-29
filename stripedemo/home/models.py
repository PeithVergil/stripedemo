import peewee

from ..core.models import BaseModel
from ..auth.models import User


class Customer(BaseModel):

    #########################
    # USER
    #########################
    user = peewee.ForeignKeyField(User, backref='customers', null=False)

    # Example:
    #
    # cus_ETZvkwcsxFRiSG
    customer_id = peewee.CharField(50)

    date_created = peewee.DateTimeField()
    date_updated = peewee.DateTimeField()

    def __str__(self):
        return 'Customer(id={}, user={}, customer_id={})'.format(
            self.id, self.user, self.customer_id,
        )


# class Order(BaseModel):

#     tier = ForeignKeyField(Tier, backref='orders', null=True)

#     #########################
#     # CUSTOMER
#     #########################
#     customer = ForeignKeyField(OrderCustomer, backref='orders', null=True)

#     #########################
#     # SONG
#     #########################
#     song_url = CharField(max_length=255)
#     song_name = CharField(max_length=255)
#     song_genre = IntegerField()
#     song_artist = CharField(max_length=255)
#     song_length = IntegerField()

#     #########################
#     # ORDER
#     #########################

#     # Values:
#     #
#     # 0 == no payment/payment failed
#     # 1 == payment complete
#     # 2 == report ordered
#     # 3 == report received
#     # 4 == customer notified
#     # order_status = SmallIntegerField(default=0)

#     #########################
#     # REPORT
#     #########################
#     report_id = IntegerField(null=True)
#     report_url = CharField(max_length=255, null=True)
#     report_data = TextField(null=True)

#     date_ordered = DateTimeField(null=True)
#     date_received = DateTimeField(null=True)

#     # Values:
#     #
#     # 0 == report not ordered
#     # 1 == report ordered
#     # 2 == report ready for retrieval
#     # 3 == report received
#     # 4 == customer notified
#     report_status = SmallIntegerField(default=0)

#     #########################
#     # TIMESTAMP
#     #########################
#     date_created = DateTimeField(null=False)
#     date_updated = DateTimeField(null=False)

#     updated_by = CharField(100, default='Song Review Service')

#     @property
#     def report_info(self):
#         """
#         Decode the raw JSON data from "report_data" into a Python dict.
#         """
#         _report_info = getattr(self, '_report_info', None)
#         if _report_info is None:
#             _report_info = json.loads(self.report_data)
#             setattr(self, '_report_info', _report_info)
#         return _report_info

#     @property
#     def track_rating(self):
#         try:
#             return self.report_info['data']['TrackRating']
#         except KeyError:
#             return None

#     @property
#     def passion_rating(self):
#         try:
#             return self.report_info['data']['PassionRating']
#         except KeyError:
#             return None

#     @property
#     def market_potential(self):
#         try:
#             return self.report_info['data']['MktPot']
#         except KeyError:
#             return None

#     def __str__(self):
#         s = 'OrderDetail(id={}, customer={}, report_id={}, report_status={})'
#         return s.format(
#             self.id,
#             self.customer,
#             self.report_id,
#             self.report_status,
#         )


class Subscription(BaseModel):

    #########################
    # CUSTOMER
    #########################
    customer = peewee.ForeignKeyField(Customer, backref='subscriptions', null=False)

    #########################
    # SUBSCRIPTION
    #########################
    # Example:
    #
    # sub_1KMGEBDESBOwdUc02i6z18Fy
    subscription_id     = peewee.CharField(50)
    

    #########################
    # TIMESTAMP
    #########################
    date_created = peewee.DateTimeField(null=False)
    date_updated = peewee.DateTimeField(null=False)

    def __str__(self):
        s = 'Subscription(id={}, customer={}, subscription_id={})'
        return s.format(
            self.id,
            self.customer,
            self.subscription_id,
        )
