import time, hmac
import six

class WebService(object):
	API_LOGIN_ID = None
	TRANSACTION_KEY = None
	MERCHANT_ID = None
	CLIENT = None
	TRANSACTION = None
	IDVERIFY = None
	
	def __init__(self):
		if WebService.API_LOGIN_ID is None:
			raise Exception("API Login ID is not set")
		if WebService.TRANSACTION_KEY is None:
			raise Exception("Transaction key is not set")
		if WebService.MERCHANT_ID is None:
			raise Exception("Merchant ID is not set")
		super(WebService, self).__setattr__('_record', None)


	@staticmethod
	def get_authentication(endpoint):
		auth = endpoint.factory.create('Authentication')
		auth.APILoginID = WebService.API_LOGIN_ID
		auth.UTCTime = "%d" % (time.time() * 10000000 + 621355968000000000)
		auth.TSHash = hmac.new(six.b(WebService.TRANSACTION_KEY), six.b("%s|%s" % (WebService.API_LOGIN_ID, auth.UTCTime))).hexdigest()
		return auth

	@property
	def authentication(self):
		return WebService.get_authentication(WebService.CLIENT) # It doesn't matter where

	def __str__(self):
		return str(self._record)
	def __repr__(self):
		return "<%s>" % str(self)
