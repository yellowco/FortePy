from .WebServices.WebService import WebService
from .AGI.RetrospectiveTransaction import RetrospectiveTransaction
from datetime import datetime
from .WebServices.PaymentMethod import PaymentMethod

class Transaction(WebService):
	def __init__(self, record=None, **kwargs):
		WebService.__init__(self, WebService.TRANSACTION)
		self._record = record if record else self.default_record
		for key, value in kwargs.items():
			setattr(client, key, value)

	@property
	def default_record(self):
		record = self.endpoint.factory.create('TransactionSummary')
		record.MerchantID = WebService.MERCHANT_ID
		record.MerchantClientID = None
		record.TransactionID = ""
		record.Status = ""
		record.TsCreated = datetime.utcnow()
		record.Last4 = ""
		record.BilltoFirstName = ""
		record.BilltoLastName = ""
		record.BilltoCompanyName = ""
		record.CardType = ""
		record.DebitCredit = ""
		record.EnteredBy = ""
		record.ConsumerOrderID = ""
		record.ConsumerID = ""
		record.WalletID = ""
		record.ResponseCode = ""
		record.AuthCode = ""
		record.Amount = 0.0
		record.ConvenienceFeePrincipal = 0.0
		record.TransactionType = 0
		return record

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
		try:
			record = WebService.TRANSACTION.service['BasicHttpBinding_ITransactionService'].getTransaction(WebService.get_authentication(WebService.TRANSACTION), WebService.MERCHANT_ID, id.lower())
			return Transaction(record=record) if record else None
		except Exception as ex:
			return None

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