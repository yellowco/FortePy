class Address(object):
	def __init__(self, first_name="", last_name="", company="", street1="", street2="", city="", state="", postal="", country="", phone="", fax=""):
		self.company = company
		self.first_name = first_name
		self.last_name = last_name
		self.street1 = street1
		self.street2 = street2
		self.city = city
		self.state = state if not state == '-1' else ""
		self.postal = postal
		self.country = country
		self.phone = phone
		self.fax = fax

	def __str__(self):
		return str(self.__dict__)
