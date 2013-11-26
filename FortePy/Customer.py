class Customer(object):
    def __init__(self, company=None, address=None, phone=None, email=None, ssn=None, drivers_license=None, birthdate=None, ip=None):
        self.company = company
        self.address = address
        self.phone = phone
        self.email = email
        self.ssn = ssn
        self.drivers_license = drivers_license
        self.birthdate = birthdate
        self.ip = ip
    
    @property
    def data(self):
        d = {'pg_billto_postal_name_company':self.company,
             'ecom_billto_telecom_phone_number': self.phone,
             'ecom_billto_online_email': self.email,
             'pg_billto_ssn': self.ssn,
             'pg_billto_date_of_birth': self.birthdate.strftime("%d/%m/%Y"),
             'pg_customer_ip_addres': self.ip}
        d.update(self.address.data)
        d.update(self.drivers_license.data)
        return d


