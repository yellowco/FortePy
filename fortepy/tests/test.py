import unittest
from ..Forte import Forte
from ..CreditCard import CreditCard
from ..DriversLicense import DriversLicense
from ..Address import Address
import datetime

class Test(unittest.TestCase):
    def test_credit_card_sale(self):
        cc = CreditCard.CreditCard(CreditCard.CreditCard.VISA,
                                   "joe bloggs",
                                   4111111111111111,
                                   datetime.date(year=2038, month=4, day=1),
                                   "123")
        customer = Customer.Customer(address=Address.Address("joe", "bloggs", "6031 S Ellis Ave", None, "Chicago", "IL", "60637", "USA"),
                                     phone="1234567890", 
                                     email="joe@bloggs.com", 
                                     ssn="1234567890", 
                                     drivers_license=DriversLicense.DriversLicense("012938039", "IL"),
                                     birthdate=datetime.date(year=1993, month=2, day=2))
        Forte.Forte(merchant_id=160361, password="Kqq4QKt35L6").for_customer(customer).execute(cc.sale(15))

if __name__ == '__main__':
    unittest.main()
