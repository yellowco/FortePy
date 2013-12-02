from WebServices.PaymentMethod import PaymentMethod
from WebServices.WebService import WebService
from AGI.RetrospectiveTransaction import RetrospectiveTransaction

class CreditCard(PaymentMethod, RetrospectiveTransaction):
    CardType = WebService.CLIENT.factory.create('CcCardType')
    VISA = CardType['VISA']
    MAST = CardType['MAST']
    DISC = CardType['DISC']
    AMER = CardType['AMER']
    DINE = CardType['DINE']
    JCB = CardType['JCB']

    def __init__(self, **kwargs):
        PaymentMethod.__init__(**kwargs)
        RetrospectiveTransaction.__init__()
        self.cvv = ""
       
    @property
    def card_number(self):
        return self.record.CcCardNumber
    @card_number.setter
    def card_number(self, value):
        self.record.CcCardNumber = value
    @property
    def expiration_date(self):
        return self.record.CcExpirationDate
    @expiration_date.setter
    def expiration_date(self, value):
        self.record.CcExpirationDate = value
    @property
    def card_type(self):
        return self.record.CcCardType
    @card_type.setter
    def card_type(self, value):
        self.record.CcCardType = value
    @property
    def is_procurement_card(self):
        return self.record.CcProcurementCard
    @is_procurement_card.setter
    def is_procurement_card(self, value):
        self.record.CcProcurementCard = value

    @property
    def data(self):
        return {'ecom_payment_card_type': str(self.card_type),
                'ecom_payment_card_name': self.account_holder,
                'ecom_payment_card_number': self.card_number,
                'ecom_payment_card_expdate_month': self.expiration_date.month,
                'ecom_payment_card_expdate_year': self.expiration_date.year,
                'ecom_payment_card_verification': self.cvv}
        
    def sale(self, amount):
        return self.transaction(10, amount)
    def authorization(self, amount):
        return self.transaction(11, amount)
    def capture(self):
        if self.trace_number is None:
            raise AttributeError("Original trace number not set")
        return self.transaction(12, 0)
    def credit(self, amount):
        return self.transaction(13, amount)
    def void(self):
        if self.trace_number is None:
            raise AttributeError("Original trace number not set")
        return self.transaction(14, 0)
    def preauthorization(self, amount):
        return self.transaction(15, amount)
    def balance_inquiry(self, amount):
        return self.transaction(16, amount)