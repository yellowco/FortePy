from WebServices import WebService
from WebServices.PaymentMethod import PaymentMethod
import ClientStatus
import Address
import DriversLicense

class Client(WebService.WebService):
    ClientStatus = WebService.WebService.CLIENT.factory.create('ClientStatus')
    ACTIVE = ClientStatus['Active']
    DELETED = ClientStatus['Deleted']
    SUSPENDED = ClientStatus['Suspended']
    def __init__(self, id=None, **kwargs):
        if id is not None:
            self.record = Client.find_by_id(id).record
        else:
            super(Client, self).__init__(WebService.WebService.CLIENT)
            self.record = self.endpoint.factory.create('ClientRecord')
            self.record.MerchantID = WebService.WebService.MERCHANT_ID
            self.record.ClientID = None
            self.record.FirstName = ""
            self.record.LastName = ""
            self.record.CompanyName = ""
            self.record.Address1 = ""
            self.record.Address2 = ""
            self.record.City = ""
            self.record.State = ""
            self.record.PostalCode = ""
            self.record.CountryCode = ""
            self.record.PhoneNumber = ""
            self.record.EmailAddress = ""
            self.record.FaxNumber = ""
            self.record.ConsumerID = ""
            self.record.ShiptoFirstName = ""
            self.record.ShiptoLastName = ""
            self.record.ShiptoCompanyName = ""
            self.record.ShiptoAddress1 = ""
            self.record.ShiptoAddress2 = ""
            self.record.ShiptoCity = ""
            self.record.ShiptoState = ""
            self.record.ShiptoPostalCode = ""
            self.record.ShiptoCountryCode = ""
            self.record.ShiptoPhoneNumber = ""
            self.record.ShiptoFaxNumber = ""
            self.record.ConsumerID = ""
            self.record.Status = Client.ACTIVE
            self._payment_methods = None # populate later!
            self.ssn = ""
            self.drivers_license = DriversLicense.DriversLicense()
            self.birthdate = None
            self.ip = ""
            for key, value in kwargs.items():
                setattr(client, key, value)
    
    @property
    def id(self):
        return self.record.ClientID
    @property
    def email(self):
        return self.record.EmailAddress
    @email.setter
    def email(self, value):
        self.record.EmailAddress = value
    @property
    def consumer_id(self):
        return self.record.ConsumerID
    @consumer_id.setter
    def consumer_id(self, value):
        self.record.ConsumerID = value
    @property
    def billing_address(self):
        return Address.Address(self.record.FirstName, self.record.LastName, self.record.CompanyName, self.record.Address1, self.record.Address2, self.record.City, self.record.State, self.record.PostalCode, self.record.CountryCode, self.record.PhoneNumber, self.record.FaxNumber)
    @billing_address.setter
    def billing_address(self, value):
        self.record.FirstName = value.first_name
        self.record.LastName = value.last_name
        self.record.CompanyName = value.company_name
        self.record.Address1 = value.street1
        self.record.Address2 = value.street2
        self.record.City = value.city
        self.record.State = value.state
        self.record.PostalCode = value.postal
        self.record.CountryCode = value.country
        self.record.PhoneNumber = value.phone
        self.record.FaxNumber = value.fax
    @property
    def shipping_address(self):
        return Address.Address(self.record.ShiptoFirstName, self.record.ShiptoLastName, self.record.ShiptoCompanyName, self.record.ShiptoAddress1, self.record.ShiptoAddress2, self.record.ShiptoCity, self.record.ShiptoState, self.record.ShiptoPostalCode, self.record.ShiptoCountryCode, self.record.ShiptoPhoneNumber, self.record.ShiptoFaxNumber)
    @billing_address.setter
    def shipping_address(self, value):
        self.record.ShiptoFirstName = value.first_name
        self.record.ShiptoLastName = value.last_name
        self.record.ShiptoCompanyName = value.company_name
        self.record.ShiptoAddress1 = value.street1
        self.record.ShiptoAddress2 = value.street2
        self.record.ShiptoCity = value.city
        self.record.ShiptoState = value.state
        self.record.ShiptoPostalCode = value.postal
        self.record.ShiptoCountryCode = value.country
        self.record.ShiptoPhoneNumber = value.phone
        self.record.ShiptoFaxNumber = value.fax
    @property
    def status(self):
        return self.record.Status
    @status.setter
    def status(self, value):
        self.record.Status = value
    @property
    def payment_methods(self):
        if self._payment_methods is None:
            self._payment_methods = PaymentMethod.find_all_by_client_id(self.id)
        return self._payment_methods
    @property
    def transactions(self):
        return Transaction.find_all_by_client_id(self.id)

    @staticmethod
    def create(**kwargs):
        return Client(**kwargs)

    def save(self):
        if self.ClientID is None:
            self.ClientID = 0
            self.ClientID = self.endpoint.service['BasicHttpBinding_IClientService'].createClient(self.authentication, self.record)
        else:
            self.ClientID = self.endpoint.service['BasicHttpBinding_IClientService'].updateClient(self.authentication, self.record)

        if self.__dict__['payment_methods'] is not None:
            for payment_method in self.__dict__['payment_methods']:
                payment_method.client = self
                payment_method.save()

        return self

    def delete(self):
        if self.ClientID is not None:
            result = (self.endpoint.service['BasicHttpBinding_IClientService'].deleteClient(self.authentication, WebService.WebService.MERCHANT_ID, self.ClientID) == self.ClientID)
            self.ClientID = None
        return self

    @staticmethod
    def retrieve(id):
        client = Client()
        client.record = WebService.WebService.CLIENT.service['BasicHttpBinding_IClientService'].getClient(WebService.WebService.get_authentication(WebService.WebService.CLIENT), WebService.WebService.MERCHANT_ID, id)[0][0]
        return client

    @staticmethod
    def all():
        # TODO stuff here
        pass