import WebService

class Client(WebService.WebService):
    ACTIVE = None
    DELETED = None
    SUSPENDED = None

    def __init__(self, id=None):
        if id is not None:
            self.record = Client.find_by_id(id).record
        else:
            super(Client, self).__init__('https://sandbox.paymentsgateway.net/WS/Client.wsdl')
            if Client.ACTIVE is None:
                statuses = self.soap.factory.create('ClientStatus')
                Client.ACTIVE = statuses['Active']
                Client.DELETED = statuses['Deleted']
                Client.SUSPENDED = statuses['Suspended']

            self.record = self.soap.factory.create('ClientRecord')
            self.MerchantID = WebService.WebService.MERCHANT_ID
            self.ClientID = None
            self.FirstName = ""
            self.LastName = ""
            self.CompanyName = ""
            self.Address1 = ""
            self.Address2 = ""
            self.City = ""
            self.State = ""
            self.PostalCode = ""
            self.CountryCode = ""
            self.PhoneNumber = ""
            self.EmailAddress = ""
            self.FaxNumber = ""
            self.ConsumerID = ""
            self.ShiptoFirstName = ""
            self.ShiptoLastName = ""
            self.ShiptoCompanyName = ""
            self.ShiptoAddress1 = ""
            self.ShiptoAddress2 = ""
            self.ShiptoCity = ""
            self.ShiptoState = ""
            self.ShiptoPostalCode = ""
            self.ShiptoCountryCode = ""
            self.ShiptoPhoneNumber = ""
            self.ShiptoFaxNumber = ""
            self.Status = Client.ACTIVE
    
    def save(self):
        if self.ClientID is None:
            self.ClientID = 0
            self.ClientID = self.soap.service['BasicHttpBinding_IClientService'].createClient(self.authentication, self.record)
        else:
            self.ClientID = self.soap.service['BasicHttpBinding_IClientService'].updateClient(self.authentication, self.record)
        return self

    def delete(self):
        if self.ClientID is not None:
            result = (self.soap.service['BasicHttpBinding_IClientService'].deleteClient(self.authentication, WebService.WebService.MERCHANT_ID, self.ClientID) == self.ClientID)
            self.ClientID = None
            return result


    @staticmethod
    def find_by_id(id):
        client = Client()
        client.record = client.soap.service['BasicHttpBinding_IClientService'].getClient(client.authentication, WebService.WebService.MERCHANT_ID, id)[0][0]
        return client