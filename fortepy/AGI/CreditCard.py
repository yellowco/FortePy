import DirectSocketInterface
import Forte
import RetrospectiveTransaction

class CreditCard(RetrospectiveTransaction.RetrospectiveTransaction):
    VISA = "VISA"
    MASTERCARD = "MAST"
    AMERICAN_EXPRESS = "AMER"
    DISCOVER = "DISC"
    DINERS_CLUB = "DINE"
    JCB = "JCB"
    def __init__(self, type, name, number, expiration_date, cvv):
        super().__init__(None, None)
        self.type = type
        self.name = name
        self.number = number
        self.expiration_month = expiration_date.month
        self.expiration_year = expiration_date.year
        self.cvv = cvv

    @property
    def data(self):
        d = {'ecom_payment_card_type': self.type,
             'ecom_payment_card_name': self.name,
             'ecom_payment_card_number': self.number,
             'ecom_payment_card_expdate_month': self.expiration_month,
             'ecom_payment_card_expdate_year': self.expiration_year,
             'ecom_payment_card_verification': self.cvv}
        return d


    def sale(self, amount):
        return self.transaction(10, amount)

    def authorization(self, amount):
        return self.transaction(11, amount)

    def capture(self, amount):
        if self.trace_number is None:
            raise AttributeError("Original trace number not set")
        return self.transaction(12, amount)

    def credit(self, amount):
        return self.transaction(13, amount)

    def void(self, amount):
        if self.trace_number is None:
            raise AttributeError("Original trace number not set")
        return self.transaction(14, amount)

    def preauthorization(self, amount):
        return self.transaction(15, amount)

    def balance_inquiry(self, amount):
        return self.transaction(16, amount)