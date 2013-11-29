import WebService
import ClientStatus

class Client(WebService.WebService):
    def __init__(self, id=None):
        if id is not None:
            self.record = Client.find_by_id(id).record
        else:
            super(Client, self).__init__(WebService.WebService.CLIENT)
            self.record = self.endpoint.factory.create('ClientRecord')
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
            self.ConsumerID = ""
            self.Status = ClientStatus.ACTIVE
    
    def save(self):
        if self.ClientID is None:
            self.ClientID = 0
            self.ClientID = self.endpoint.service['BasicHttpBinding_IClientService'].createClient(self.authentication, self.record)
        else:
            self.ClientID = self.endpoint.service['BasicHttpBinding_IClientService'].updateClient(self.authentication, self.record)
        return self

    def delete(self):
        if self.ClientID is not None:
            result = (self.endpoint.service['BasicHttpBinding_IClientService'].deleteClient(self.authentication, WebService.WebService.MERCHANT_ID, self.ClientID) == self.ClientID)
            self.ClientID = None
            return result


    @staticmethod
    def find_by_id(id):
        client = Client()
        client.record = WebService.WebService.CLIENT.service['BasicHttpBinding_IClientService'].getClient(WebService.WebService.get_authentication(WebService.WebService.CLIENT), WebService.WebService.MERCHANT_ID, id)[0][0]
        return client