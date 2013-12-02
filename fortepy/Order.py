class Order(object):
    def __init__(self, order_id=None, consumer_id=None, wallet_id=None, entered_by=None, merchant_data=[], software_name=None, software_version=None):
        self.order_id = order_id
        self.consumer_id = consumer_id
        self.wallet_id = wallet_id
        self.entered_by = entered_by
        self.merchant_data = merchant_data
        self.software_name = software_name
        self.software_version = software_version
