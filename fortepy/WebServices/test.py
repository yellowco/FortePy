import unittest
import datetime
import Client

class Test(unittest.TestCase):
    def test_credit_card_sale(self):
        client = Client.Client()
        client.CompanyName = "TestCo"
        client.save()
        self.assertTrue(client.ClientID is not None)
        c2 = Client.Client(client.ClientID)
        self.assertTrue(c2.CompanyName == "TestCo")
        client.CompanyName = "ReTestCo"
        client.save()
        c2 = Client.Client(client.ClientID)
        self.assertTrue(c2.CompanyName == "ReTestCo")
        self.assertTrue(client.delete())


if __name__ == '__main__':
    unittest.main()
