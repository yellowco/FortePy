from .WebServices.WebService import WebService
from xml.dom import minidom

class IDVerify(WebService):
	def __init__(self, client):
		super(IDVerify, self).__init__(WebService.ID_VERIFY)
		xml = self.endpoint.service['IDVerifyWSSoap'].IDVerify(
			WebService.MERCHANT_ID,
			WebService.TRANSACTION_KEY,
			client.id,
			None, None,
			client.ssn,
			client.billing_address.first_name,
			client.billing_address.last_name,
			client.billing_address.street1,
			client.billing_address.city,
			client.billing_address.state,
			client.billing_address.postal,
			client.billing_address.phone,
			client.drivers_license.number,
			client.drivers_license.state
		)
		print(minidom.parseString(xml))
