from suds.client import Client
import WebService
PaymentType = WebService.WebService.CLIENT.factory.create('PaymentType')
ECHECK = PaymentType['eCheck']
CREDIT_CARD = PaymentType['CreditCard']
