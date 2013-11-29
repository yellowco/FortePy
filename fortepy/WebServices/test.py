import unittest
import datetime
import Client
import PaymentMethod
import EcAccountType

class Test(unittest.TestCase):
    def test_clients(self):
        client = Client.Client()
        client.CompanyName = "TestCo"
        client.save()
        self.assertIsNotNone(client.ClientID)
        c2 = Client.Client(client.ClientID)
        self.assertEqual(c2.CompanyName, "TestCo")
        client.CompanyName = "ReTestCo"
        client.save()
        c2 = Client.Client(client.ClientID)
        self.assertEqual(c2.CompanyName, "ReTestCo")
        self.assertTrue(client.delete())

    def test_payment_methods(self):
        client = Client.Client()
        client.CompanyName = "TestCo"
        client.save()
        pm1 = PaymentMethod.PaymentMethod(client)
        pm1.AcctHolderName = "Bill John"
        pm1.EcAccountNumber = '89005112216'
        pm1.EcAccountTRN = '021283916'
        pm1.EcAccountType = EcAccountType.CHECKING
        pm1.save()
        self.assertIsNotNone(pm1.PaymentMethodID)
        pm2 = PaymentMethod.PaymentMethod(client)
        pm2.AcctHolderName = "Bill John"
        pm2.EcAccountNumber = '89005112214'
        pm2.EcAccountTRN = '021283916'
        pm2.EcAccountType = EcAccountType.CHECKING
        pm2.save()
        self.assertIsNotNone(pm2.PaymentMethodID)
        self.assertEqual(len(PaymentMethod.PaymentMethod.find_all_by_client_id(1009211)), 2)
        self.assertEqual(PaymentMethod.PaymentMethod.find_by_id(pm2.PaymentMethodID).EcAccountNumber, 'XXXXXX2214')
        self.assertTrue(pm1.delete())
        self.assertTrue(pm2.delete())

if __name__ == '__main__':
    unittest.main()
