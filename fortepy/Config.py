from .WebServices.WebService import WebService
from .Client import Client
from .BankAccount import BankAccount
from .CreditCard import CreditCard
from .AGI.DirectSocketInterface import DirectSocketInterface
from .WebServices.PaymentMethod import PaymentMethod
from suds.client import Client as suds

def config(merchant_id=None, api_login_id=None, transaction_key=None, agi_password=None, require_compliance=None, sandbox=None):
	WebService.MERCHANT_ID = merchant_id or WebService.MERCHANT_ID
	WebService.API_LOGIN_ID = api_login_id or WebService.API_LOGIN_ID
	WebService.TRANSACTION_KEY = transaction_key or WebService.TRANSACTION_KEY
	DirectSocketInterface.MERCHANT_ID = merchant_id or DirectSocketInterface.MERCHANT_ID
	DirectSocketInterface.AGI_PASSWORD = agi_password or DirectSocketInterface.AGI_PASSWORD
	PaymentMethod.REQUIRE_COMPLIANCE = require_compliance if require_compliance is not None else PaymentMethod.REQUIRE_COMPLIANCE
	if sandbox is not None or WebService.CLIENT is None:
		if sandbox:
			WebService.CLIENT = suds('https://sandbox.paymentsgateway.net/WS/Client.wsdl')
			WebService.TRANSACTION = suds('https://sandbox.paymentsgateway.net/WS/Transaction.wsdl')
		else:
			WebService.CLIENT = suds('https://ws.paymentsgateway.net/Service/v1/Client.wsdl')
			WebService.TRANSACTION = suds('https://ws.paymentsgateway.net/Service/v1/Transaction.wsdl')
<<<<<<< HEAD
		WebService.IDVERIFY = suds('https://ws.paymentsgateway.net/idverify/idverifyWS.asmx?wsdl')
=======
		WebService.ID_VERIFY = suds('https://ws.paymentsgateway.net/idverify/idverifyWS.asmx?wsdl')
>>>>>>> add idverify
		AccountType = WebService.CLIENT.factory.create('EcAccountType')
		BankAccount.CHECKING = AccountType['CHECKING']
		BankAccount.SAVINGS = AccountType['SAVINGS']
		CardType = WebService.CLIENT.factory.create('CcCardType')
		CreditCard.VISA = CardType['VISA']
		CreditCard.MAST = CardType['MAST']
		CreditCard.DISC = CardType['DISC']
		CreditCard.AMER = CardType['AMER']
		CreditCard.DINE = CardType['DINE']
		CreditCard.JCB = CardType['JCB']
		ClientStatus = WebService.CLIENT.factory.create('ClientStatus')
		Client.ACTIVE = ClientStatus['Active']
		Client.DELETED = ClientStatus['Deleted']
		Client.SUSPENDED = ClientStatus['Suspended']
