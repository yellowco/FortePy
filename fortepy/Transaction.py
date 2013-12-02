from WebServices.WebService import WebService
from AGI.RetrospectiveTransaction import RetrospectiveTransaction
from datetime import datetime
from WebServices.PaymentMethod import PaymentMethod

class Transaction(WebService, RetrospectiveTransaction):
    def __init__(self, **kwargs):
        super(Transaction, self).__init__(WebService.TRANSACTION)
        self.record = self.endpoint.factory.create('TransactionSummary')
        self.record.MerchantID = WebService.MERCHANT_ID
        self.record.MerchantClientID = None
        self.record.TransactionID = ""
        self.record.Status = ""
        self.record.TsCreated = datetime.utcnow()
        self.record.Last4 = ""
        self.record.BilltoFirstName = ""
        self.record.BilltoLastName = ""
        self.record.BilltoCompanyName = ""
        self.record.CardType = ""
        self.record.DebitCredit = ""
        self.record.EnteredBy = ""
        self.record.ConsumerOrderID = ""
        self.record.ConsumerID = ""
        self.record.WalletID = ""
        self.record.ResponseCode = ""
        self.record.AuthCode = ""
        self.record.Amount = 0.0
        self.record.ConvenienceFeePrincipal = 0.0
        self.record.TransactionType = 0

        for key, value in kwargs.items():
            setattr(client, key, value)

    @property
    def id(self):
        return self.record.TransactionID
    
    @property
    def authorization_code(self):
        return self.record.AuthCode

    @property
    def payment_method_id(self):
        return self.record.WalletID

    @staticmethod
    def create():
        raise Exception("One does not simply create a transaction.")

    @staticmethod
    def retrieve(id):
        tx = Transaction()
        tx.record = WebService.TRANSACTION.service['BasicHttpBinding_IClientService'].getTransaction(WebService.get_authentication(WebService.TRANSACTION), WebService.MERCHANT_ID, id)[0][0]
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