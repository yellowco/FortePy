import WebService
import CcCardType
import EcAccountType
from ..BankAccount import BankAccount
from ..CreditCard import CreditCard

class PaymentMethod(WebService.WebService):
    def __init__(self, client=None, **kwargs):
        super(PaymentMethod, self).__init__(WebService.WebService.CLIENT)
        self.record = self.endpoint.factory.create('PaymentMethod')
        self.record.AcctHolderName = ""
        self.record.CcCardNumber = ""
        self.record.CcExpirationDate = ""
        self.record.CcCardType = CcCardType.VISA
        self.record.CcProcurementCard = False
        self.record.EcAccountNumber = ""
        self.record.EcAccountTRN = ""
        self.record.EcAccountType = WebService.WebService.CLIENT.factory.create('EcAccountType')['CHECKING']
        self.record.Note = ""
        self.record.PaymentMethodID = None
        self.record.ClientID = client.ClientID if client else None
        self.record.MerchantID = WebService.WebService.MERCHANT_ID
        self.record.IsDefault = False
        self._client = None
        for key, value in kwargs.items():
            setattr(client, key, value)

    @property
    def client(self):
        return self._client
    @client.setter
    def client(self, value):
        self._client = value
        self.record.ClientID = self._client.id
    @property
    def note(self):
        return self.record.Note
    @note.setter
    def note(self, value):
        self.record.Note = value
    @property
    def id(self):
        return self.record.PaymentMethodID
    @property
    def account_holder(self):
        return self.record.AcctHolderName
    @account_holder.setter
    def account_holder(self, value):
        self.record.AcctHolderName = value
    @property
    def is_default(self):
        return self.record.IsDefault
    @is_default.setter
    def is_default(self, value):
        self.record.IsDefault = value

    def save(self):
        if self.PaymentMethodID is None:
            self.PaymentMethodID = 0
            self.PaymentMethodID = self.endpoint.service['BasicHttpBinding_IClientService'].createPaymentMethod(self.authentication, self.record)
        else:
            self.PaymentMethodID = self.endpoint.service['BasicHttpBinding_IClientService'].updatePaymentMethod(self.authentication, self.record)
        return self

    def delete(self):
        if self.PaymentMethodID is not None:
            result = (self.endpoint.service['BasicHttpBinding_IClientService'].deletePaymentMethod(self.authentication, WebService.WebService.MERCHANT_ID, self.PaymentMethodID) == self.PaymentMethodID)
            self.PaymentMethodID = None
        return self

    @staticmethod
    def retrieve(id):
        record = WebService.WebService.CLIENT.service['BasicHttpBinding_IClientService'].getPaymentMethod(WebService.WebService.get_authentication(WebService.WebService.CLIENT), WebService.WebService.MERCHANT_ID, 0, id)[0][0]
        if record.CcCardNumber == "" or record.CcCardNumber is None:
            payment_method = BankAccount()
        else:
            payment_method = CreditCard()
        payment_method.record = record
        return payment_method

    @staticmethod
    def find_all_by_client_id(id):
        methods = WebService.WebService.CLIENT.service['BasicHttpBinding_IClientService'].getPaymentMethod(WebService.WebService.get_authentication(WebService.WebService.CLIENT), WebService.WebService.MERCHANT_ID, id, 0)[0]
        payment_objects = []
        for method in methods:
            if method.CcCardNumber == "" or method.CcCardNumber is None:
                payment_method = BankAccount()
            else:
                payment_method = CreditCard()
            payment_method.record = method
            payment_objects.append(payment_method)
        return payment_objects
