from .DirectSocketInterface import DirectSocketInterface
from ..WebServices.WebService import WebService

class RetrospectiveTransaction(object):
	def __init__(self, trace_number=None, authorization_code=None):
		self.trace_number = trace_number
		self.authorization_code = authorization_code
		self._client = None
		self.verification = None
		self.order = None
		self.recurrence = None
		
	def verify_with(self, verification):
		self.verification = verification
		return self

	def regarding_order(self, order):
		self.order = order
		return self

	def including_recurrence(self, recurrence):
		self.recurrence = recurrence
		return self

	def transaction(self, type, amount):
		d = {'pg_transaction_type': type,
			 'pg_total_amount': amount,
			 'pg_original_trace_number': self.trace_number,
			 'pg_original_authorization_code': self.authorization_code,
			 'ecom_walletid':self.id} # what is a wallet id...
		d.update(self.data)
		return self.execute(d)

	@staticmethod
	def get_client_data(client):
		d = {'ecom_billto_online_email': client.email,
			 'pg_billto_ssn': client.ssn,
			 'pg_billto_date_of_birth': client.birthdate.strftime("%d/%m/%Y") if client.birthdate else None,
			 'pg_customer_ip_address': client.ip}
		d.update(RetrospectiveTransaction.get_address_data(client.billing_address))
		d.update(RetrospectiveTransaction.get_drivers_license_data(client.drivers_license))
		return d

	@staticmethod
	def get_address_data(address):
		return {'pg_billto_postal_name_company':address.company,
				'ecom_billto_postal_name_first': address.first_name,
				'ecom_billto_postal_name_last': address.last_name,
				'ecom_billto_postal_street_line1': address.street1,
				'ecom_billto_postal_street_line2': address.street2,
				'ecom_billto_postal_city': address.city,
				'ecom_billto_postal_stateprov': address.state,
				'ecom_billto_postal_postalcode': address.postal,
				'ecom_billto_postal_countrycode': address.country,
				'ecom_billto_telecom_phone_number': address.phone}
	@staticmethod
	def get_verify_data(verify):
		return {'pg_avs_method':verify.code}

	@staticmethod
	def get_order_data(order):
		d = {'ecom_consumerorderid':order.order_id,
			 'pg_consumer_id':order.consumer_id,
			 'pg_entered_by':order.entered_by,
			 'pg_software_name':order.software_name,
			 'pg_software_version':order.software_version}
		for index, value in enumerate(order.merchant_data):
			d["pg_merchant_data_%d" % index] = value
		return d

	@staticmethod
	def get_drivers_license_data(license):
		return {'pg_billto_dl_number': license.number,
				'pg_billto_dl_state': license.state}
	
	@staticmethod
	def get_recurrence_data(recurrence):
		data = {'pg_schedule_quantity':recurrence.quantity,
				'pg_schedule_frequency':recurrence.frequency,
				'pg_schedule_recurring_amount':recurrence.amount}
		if recurrence.start_date:
			data['pg_schedule_start_date'] = recurrence.start_date.strftime("%d/%m/%Y")
		return data

	def execute(self, operation={}):
		with DirectSocketInterface() as socket:
			socket.write_header()
			if self._client:
				operation.update(RetrospectiveTransaction.get_client_data(self._client))
			else:
				raise Exception("Parent client not specified, could not execute transaction.")
			if self.order:
				operation.update(RetrospectiveTransaction.get_order_data(self.order))
			if self.verification:
				operation.update(RetrospectiveTransaction.get_verify_data(self.verification))
			if self.recurrence:
				operation.update(RetrospectiveTransaction.get_recurrence_data(self.recurrence))
			
			for key, value in operation.items():
				socket.write(key, value)
			socket.send()
			response = socket.read()
			return response['pg_response_type'] == 'A', response['pg_trace_number'], response