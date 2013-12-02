from WebServices.PaymentMethod import PaymentMethod
from WebServices.WebService import WebService

class BankAccount(PaymentMethod):
    AccountType = WebService.CLIENT.factory.create('EcAccountType')
    CHECKING = AccountType['CHECKING']
    SAVINGS = AccountType['SAVINGS']

    def __init__(self, **kwargs):
        PaymentMethod.__init__(**kwargs)
        RetrospectiveTransaction.__init__()

    @property
    def account_number(self):
        return self.record.EcAccountNumber
    @account_number.setter
    def account_number(self, value):
        self.record.EcAccountNumber = value
    @property
    def routing_number(self):
        return self.record.EcAccountTRN
    @routing_number.setter
    def routing_number(self, value):
        self.record.EcAccountTRN = value
    @property
    def type(self):
        return self.record.EcAccountType
    @type.setter
    def type(self, value):
        self.record.EcAccountType = value
    
    @property
    def data(self):
        return {'ecom_payment_check_trn': self.routing_number,
                'ecom_payment_check_account': self.account_number,
                'ecom_payment_check_account_type': 'C' if str(self.type).find('CHECKING') != -1 else 'S'}

    @staticmethod
    def create(**kwargs):
        return BankAccount(**kwargs)

    def sale(self, amount):
        return self.transaction(20, amount)
    def authorization(self, amount):
        return self.transaction(21, amount)
    def capture(self, amount):
        if self.trace_number is None:
            raise AttributeError("Original trace number not set")
        return self.transaction(22, amount)
    def credit(self, amount):
        return self.transaction(23, amount)
    def void(self, amount):
        if self.trace_number is None:
            raise AttributeError("Original trace number not set")
        return self.transaction(24, amount)
    def force(self, amount):
        return self.transaction(25, amount)
    def verify(self, amount):
        return self.transaction(26, amount)