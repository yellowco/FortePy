class Order(object):
    def __init__(self, order_id=None, consumer_id=None, wallet_id=None, entered_by=None, merchant_data=[], software_name=None, software_version=None):
        self.order_id = order_id
        self.consumer_id = consumer_id
        self.wallet_id = wallet_id
        self.entered_by = entered_by
        self.merchant_data = merchant_data
        self.software_name = software_name
        self.software_version = software_version

    @property
    def data(self):
        d = {'ecom_consumerorderid':self.order_id,
             'pg_consumer_id':self.consumer_id,
             'ecom_walletid':self.wallet_id,
             'pg_entered_by':self.entered_by,
             'pg_software_name':self.software_name,
             'pg_software_version':self.software_version}
        for index, value in enumerate(self.merchant_data):
            d["pg_merchant_data_%d" % index] = value
        return d