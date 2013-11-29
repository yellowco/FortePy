import WebService
import CcCardType
import EcAccountType

class PaymentMethod(WebService.WebService):
    def __init__(self, client=None):
        super(PaymentMethod, self).__init__(WebService.WebService.CLIENT)
        self.record = self.endpoint.factory.create('PaymentMethod')
        self.AcctHolderName = ""
        self.CcCardNumber = ""
        self.CcExpirationDate = ""
        self.CcCardType = CcCardType.VISA
        self.CcProcurementCard = False
        self.EcAccountNumber = ""
        self.EcAccountTRN = ""
        self.EcAccountType = EcAccountType.CHECKING
        self.Note = ""
        self.PaymentMethodID = None
        self.ClientID = client.ClientID if client else None
        self.MerchantID = WebService.WebService.MERCHANT_ID
        self.IsDefault = False
    
    def save(self):
        if self.PaymentMethodID is None:
            self.PaymentMethodID = 0
            self.PaymentMethodID = self.endpoint.service['BasicHttpBinding_IClientService'].createPaymentMethod(self.authentication, self.record)
        else:
            self.PaymentMethodID = self.endpoint.service['BasicHttpBinding_IClientService'].updatePaymentMethod(self.authentication, self.record)
        return self

    def delete(self):
        if self.PaymentMethodID is not None:
            result = (self.endpoint.service['BasicHttpBinding_IClientService'].deletePaymentMethod(self.authentication, WebService.WebService.MERCHANT_ID, self.PaymentMethodID) == self.PaymentMethodID)
            self.PaymentMethodID = None
            return result


    @staticmethod
    def find_by_id(id):
        payment_method = PaymentMethod()
        payment_method.record = WebService.WebService.CLIENT.service['BasicHttpBinding_IClientService'].getPaymentMethod(WebService.WebService.get_authentication(WebService.WebService.CLIENT), WebService.WebService.MERCHANT_ID, 0, id)[0][0]
        return payment_method

    @staticmethod
    def find_all_by_client_id(id):
        methods = WebService.WebService.CLIENT.service['BasicHttpBinding_IClientService'].getPaymentMethod(WebService.WebService.get_authentication(WebService.WebService.CLIENT), WebService.WebService.MERCHANT_ID, id, 0)[0]
        payment_objects = []
        for method in methods:
            payment_method = PaymentMethod()
            payment_method.record = method
            payment_objects.append(payment_method)
        return payment_objects
