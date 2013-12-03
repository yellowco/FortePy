from .WebServices.WebService import WebService
from .AGI.RetrospectiveTransaction import RetrospectiveTransaction
from datetime import datetime
from .WebServices.PaymentMethod import PaymentMethod

class Transaction(WebService, RetrospectiveTransaction):
    def __init__(self, **kwargs):
        super(Transaction, self).__init__(WebService.TRANSACTION)
        self._record = self.endpoint.factory.create('TransactionSummary')
        self._record.MerchantID = WebService.MERCHANT_ID
        self._record.MerchantClientID = None
        self._record.TransactionID = ""
        self._record.Status = ""
        self._record.TsCreated = datetime.utcnow()
        self._record.Last4 = ""
        self._record.BilltoFirstName = ""
        self._record.BilltoLastName = ""
        self._record.BilltoCompanyName = ""
        self._record.CardType = ""
        self._record.DebitCredit = ""
        self._record.EnteredBy = ""
        self._record.ConsumerOrderID = ""
        self._record.ConsumerID = ""
        self._record.WalletID = ""
        self._record.ResponseCode = ""
        self._record.AuthCode = ""
        self._record.Amount = 0.0
        self._record.ConvenienceFeePrincipal = 0.0
        self._record.TransactionType = 0

        for key, value in kwargs.items():
            setattr(client, key, value)

    @property
    def id(self):
        return self._record.TransactionID
    
    @property
    def authorization_code(self):
        return self._record.AuthCode

    @property
    def payment_method_id(self):
        return self._record.WalletID

    @staticmethod
    def save():
        raise Exception("One does not simply save a transaction.")

    @staticmethod
    def create():
        raise Exception("One does not simply create a transaction.")

    @staticmethod
    def retrieve(id):
        tx = Transaction()
        tx._record = WebService.TRANSACTION.service['BasicHttpBinding_IClientService'].getTransaction(WebService.get_authentication(WebService.TRANSACTION), WebService.MERCHANT_ID, id)[0][0]
        return tx

    def capture():
        method = PaymentMethod.retrieve(self.payment_method_id)
        method.trace_number = self.id
        method.authorization_code = self.authorization_code
        return method.capture()

    def void():
        method = PaymentMethod.retrieve(self.payment_method_id)
        method.trace_number = self.id
        method.authorization_code = self.authorization_code
        return method.void()