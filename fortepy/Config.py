from .WebServices.WebService import WebService
from .AGI.DirectSocketInterface import DirectSocketInterface
from .WebServices.PaymentMethod import PaymentMethod
from suds.client import Client

def config(merchant_id=None, api_login_id=None, transaction_key=None, agi_password=None, require_compliance=None, sandbox=None):
	WebService.MERCHANT_ID = merchant_id or WebService.MERCHANT_ID
	WebService.API_LOGIN_ID = api_login_id or WebService.API_LOGIN_ID
	WebService.TRANSACTION_KEY = transaction_key or WebService.TRANSACTION_KEY
	DirectSocketInterface.MERCHANT_ID = merchant_id or DirectSocketInterface.MERCHANT_ID
	DirectSocketInterface.AGI_PASSWORD = agi_password or DirectSocketInterface.AGI_PASSWORD
	PaymentMethod.REQUIRE_COMPLIANCE = require_compliance if require_compliance is not None else PaymentMethod.REQUIRE_COMPLIANCE
	if sandbox is not None or WebService.CLIENT is None:
		if sandbox:
			WebService.CLIENT = Client('https://sandbox.paymentsgateway.net/WS/Client.wsdl')
			WebService.TRANSACTION = Client('https://sandbox.paymentsgateway.net/WS/Transaction.wsdl')
		else:
			WebService.CLIENT = Client('https://ws.paymentsgateway.net/Service/v1/Client.wsdl')
			WebService.TRANSACTION = Client('https://ws.paymentsgateway.net/Service/v1/Transaction.wsdl')