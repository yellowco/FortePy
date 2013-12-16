from .WebService import WebService

class PaymentMethod(WebService):
	def __init__(self, **kwargs):
		super(PaymentMethod, self).__init__(WebService.CLIENT)
		self._record = self.endpoint.factory.create('PaymentMethod')
		self._record.AcctHolderName = ""
		self._record.CcCardNumber = ""
		self._record.CcExpirationDate = ""
		self._record.CcCardType = None
		self._record.CcProcurementCard = False
		self._record.EcAccountNumber = ""
		self._record.EcAccountTRN = ""
		self._record.EcAccountType = WebService.CLIENT.factory.create('EcAccountType')['CHECKING']
		self._record.Note = ""
		self._record.PaymentMethodID = None
		self._record.ClientID = None
		self._record.MerchantID = WebService.MERCHANT_ID
		self._record.IsDefault = False
		self._client = None
		for key, value in kwargs.items():
			setattr(self, key, value)

	@property
	def client(self):
		return self._client
	@client.setter
	def client(self, value):
		self._client = value
		self._record.ClientID = self._client.id
	@property
	def note(self):
		return self._record.Note
	@note.setter
	def note(self, value):
		self._record.Note = value
	@property
	def id(self):
		return self._record.PaymentMethodID
	@property
	def account_holder(self):
		return self._record.AcctHolderName
	@account_holder.setter
	def account_holder(self, value):
		self._record.AcctHolderName = value
	@property
	def is_default(self):
		return self._record.IsDefault
	@is_default.setter
	def is_default(self, value):
		self._record.IsDefault = value

	def save(self):
		if self.id is None:
			self._record.PaymentMethodID = 0
			self._record.PaymentMethodID = self.endpoint.service['BasicHttpBinding_IClientService'].createPaymentMethod(self.authentication, self._record)
		else:
			self._record.PaymentMethodID = self.endpoint.service['BasicHttpBinding_IClientService'].updatePaymentMethod(self.authentication, self._record)
		return self

	def delete(self):
		if self.id is not None:
			result = (self.endpoint.service['BasicHttpBinding_IClientService'].deletePaymentMethod(self.authentication, WebService.MERCHANT_ID, self.id) == self.id)
			self._record.PaymentMethodID = None
		return self

	@staticmethod
	def retrieve(id, type):
		record = WebService.CLIENT.service['BasicHttpBinding_IClientService'].getPaymentMethod(WebService.get_authentication(WebService.CLIENT), WebService.MERCHANT_ID, 0, id)[0][0]
		payment_method = type()
		payment_method._record = record
		return payment_method

	@staticmethod
	def find_all_by_client_id(id, bank_type, cc_type):
		methods = WebService.CLIENT.service['BasicHttpBinding_IClientService'].getPaymentMethod(WebService.get_authentication(WebService.CLIENT), WebService.MERCHANT_ID, id, 0)
		payment_objects = []
		if methods:
			for method in methods[0]:
				if method.CcCardNumber == "" or method.CcCardNumber is None:
					payment_method = bank_type()
				else:
					payment_method = cc_type()
				payment_method._record = method
				payment_objects.append(payment_method)
		return payment_objects
