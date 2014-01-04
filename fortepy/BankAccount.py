from .AGI.RetrospectiveTransaction import RetrospectiveTransaction
from .WebServices.PaymentMethod import PaymentMethod
from .WebServices.WebService import WebService

class BankAccount(PaymentMethod, RetrospectiveTransaction):
	CHECKING = None
	SAVINGS = None

	def __init__(self, **kwargs):
		RetrospectiveTransaction.__init__(self)
		PaymentMethod.__init__(self, **kwargs)

	@property
	def account_number(self):
		return self._record.EcAccountNumber
	@account_number.setter
	def account_number(self, value):
		self._record.EcAccountNumber = value
	@property
	def routing_number(self):
		return self._record.EcAccountTRN
	@routing_number.setter
	def routing_number(self, value):
		self._record.EcAccountTRN = value
	@property
	def type(self):
		return self._record.EcAccountType
	@type.setter
	def type(self, value):
		self._record.EcAccountType = value
	
	@property
	def data(self):
		return {'ecom_payment_check_trn': self.routing_number,
				'ecom_payment_check_account': self.account_number,
				'ecom_payment_check_account_type': 'C' if str(self.type).find('CHECKING') != -1 else 'S'}
	@staticmethod
	def retrieve(id, **kwargs):
		return PaymentMethod.retrieve(id, BankAccount, **kwargs)
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
