from .WebServices.WebService import WebService
from .WebServices.PaymentMethod import PaymentMethod
from .BankAccount import BankAccount
from .CreditCard import CreditCard
from .Address import Address
from .DriversLicense import DriversLicense

class Client(WebService):
	ClientStatus = WebService.CLIENT.factory.create('ClientStatus')
	ACTIVE = ClientStatus['Active']
	DELETED = ClientStatus['Deleted']
	SUSPENDED = ClientStatus['Suspended']
	def __init__(self, record=None, **kwargs):
		super(Client, self).__init__(WebService.CLIENT)
		self._record = record if record else self.default_record
		self._load_addresses()
		self._payment_methods = None # populate later!
		self.ssn = ""
		self.drivers_license = DriversLicense()
		self.birthdate = None
		self.ip = ""
		for key, value in kwargs.items():
			setattr(self, key, value)
	
	@property
	def default_record(self):
		record = self.endpoint.factory.create('ClientRecord')
		record.MerchantID = WebService.MERCHANT_ID
		record.ClientID = None
		record.FirstName = ""
		record.LastName = ""
		record.CompanyName = ""
		record.Address1 = ""
		record.Address2 = ""
		record.City = ""
		record.State = ""
		record.PostalCode = ""
		record.CountryCode = ""
		record.PhoneNumber = ""
		record.EmailAddress = ""
		record.FaxNumber = ""
		record.ConsumerID = ""
		record.ShiptoFirstName = ""
		record.ShiptoLastName = ""
		record.ShiptoCompanyName = ""
		record.ShiptoAddress1 = ""
		record.ShiptoAddress2 = ""
		record.ShiptoCity = ""
		record.ShiptoState = ""
		record.ShiptoPostalCode = ""
		record.ShiptoCountryCode = ""
		record.ShiptoPhoneNumber = ""
		record.ShiptoFaxNumber = ""
		record.ConsumerID = ""
		record.Status = Client.ACTIVE
		return record
	
	def _load_addresses(self):
		self.billing_address = Address(self._record.FirstName, self._record.LastName, self._record.CompanyName, self._record.Address1, self._record.Address2, self._record.City, self._record.State, self._record.PostalCode, self._record.CountryCode, self._record.PhoneNumber, self._record.FaxNumber)
		self.shipping_address = Address(self._record.ShiptoFirstName, self._record.ShiptoLastName, self._record.ShiptoCompanyName, self._record.ShiptoAddress1, self._record.ShiptoAddress2, self._record.ShiptoCity, self._record.ShiptoState, self._record.ShiptoPostalCode, self._record.ShiptoCountryCode, self._record.ShiptoPhoneNumber, self._record.ShiptoFaxNumber)
	
	def _save_addresses(self):
		value = self.billing_address
		self._record.FirstName = value.first_name
		self._record.LastName = value.last_name
		self._record.CompanyName = value.company
		self._record.Address1 = value.street1
		self._record.Address2 = value.street2
		self._record.City = value.city
		self._record.State = value.state
		self._record.PostalCode = value.postal
		self._record.CountryCode = value.country
		self._record.PhoneNumber = value.phone
		self._record.FaxNumber = value.fax
		value = self.shipping_address
		self._record.ShiptoFirstName = value.first_name
		self._record.ShiptoLastName = value.last_name
		self._record.ShiptoCompanyName = value.company
		self._record.ShiptoAddress1 = value.street1
		self._record.ShiptoAddress2 = value.street2
		self._record.ShiptoCity = value.city
		self._record.ShiptoState = value.state
		self._record.ShiptoPostalCode = value.postal
		self._record.ShiptoCountryCode = value.country
		self._record.ShiptoPhoneNumber = value.phone
		self._record.ShiptoFaxNumber = value.fax
	
	@property
	def id(self):
		return self._record.ClientID
	@property
	def email(self):
		return self._record.EmailAddress
	@email.setter
	def email(self, value):
		self._record.EmailAddress = value
	@property
	def consumer_id(self):
		return self._record.ConsumerID
	@consumer_id.setter
	def consumer_id(self, value):
		self._record.ConsumerID = value
	@property
	def status(self):
		return self._record.Status
	@status.setter
	def status(self, value):
		self._record.Status = value
		
	def add_payment_method(self, method):
		self.payment_methods.append(method)
		method.client = self
		return self
		
	@property
	def payment_methods(self):
		if self._payment_methods is None:
			if self.id is None:
				# They're not saved, so they shouldn't have any payments.
				self._payment_methods = []
			else:
				self._payment_methods = PaymentMethod.find_all_by_client_id(self.id, BankAccount, CreditCard)
		return self._payment_methods
	@property
	def transactions(self):
		return Transaction.find_all_by_client_id(self.id)

	@staticmethod
	def create(**kwargs):
		return Client(**kwargs)

	def save(self):
		self._save_addresses()
		if self.id is None:
			self._record.ClientID = 0
			self._record.ClientID = self.endpoint.service['BasicHttpBinding_IClientService'].createClient(self.authentication, self._record)
		else:
			self._record.ClientID = self.endpoint.service['BasicHttpBinding_IClientService'].updateClient(self.authentication, self._record)

		if self._payment_methods is not None:
			for payment_method in self._payment_methods:
				payment_method.save()

		return self

	def delete(self):
		if self.id is not None:
			result = (self.endpoint.service['BasicHttpBinding_IClientService'].deleteClient(self.authentication, WebService.MERCHANT_ID, self.id) == self.id)
			self._record.ClientID = None
		return self

	@staticmethod
	def retrieve(id):
		try:
			record = WebService.CLIENT.service['BasicHttpBinding_IClientService'].getClient(WebService.get_authentication(WebService.CLIENT), WebService.MERCHANT_ID, id)
			return Client(record=record[0][0]) if record else None
		except Exception as ex:
			return None

	@staticmethod
	def all():
		raise Exception("Forte's API does not permit retrieving all clients at the moment.")
