from suds.client import Client
import time, hmac

class WebService(object):
	API_LOGIN_ID = None
	TRANSACTION_KEY = None
	MERCHANT_ID = None
	CLIENT = Client('https://sandbox.paymentsgateway.net/WS/Client.wsdl')
	TRANSACTION = Client('https://sandbox.paymentsgateway.net/WS/Transaction.wsdl')
	
	def __init__(self, endpoint):
		if WebService.API_LOGIN_ID is None:
			raise Exception("API Login ID is not set")
		if WebService.TRANSACTION_KEY is None:
			raise Exception("Transaction key is not set")
		if WebService.MERCHANT_ID is None:
			raise Exception("Merchant ID is not set")
		self.endpoint = endpoint
		self._record = None

	@staticmethod
	def get_authentication(endpoint):
		auth = endpoint.factory.create('Authentication')
		auth.APILoginID = WebService.API_LOGIN_ID
		auth.UTCTime = "%d" % (time.time() * 10000000 + 621355968000000000)
		auth.TSHash = hmac.new(bytes(WebService.TRANSACTION_KEY, 'UTF-8'), bytes("%s|%s" % (WebService.API_LOGIN_ID, auth.UTCTime), 'UTF-8')).hexdigest()
		return auth

	@property
	def authentication(self):
		return WebService.get_authentication(self.endpoint)

	def __str__(self):
		return str(self._record)
	def __repr__(self):
		return "<%s>" % str(self)