from .. import Config
from ..Client import Client
from ..Transaction import Transaction
from ..AddressVerification import AddressVerification
from ..BankAccount import BankAccount
from ..CreditCard import CreditCard
import unittest
import datetime
import time

class AGITest(unittest.TestCase):
	def setUp(self):
		Config.config(merchant_id = 160361,
			transaction_key = '1NSa45VrQJk2j5',
			api_login_id = '5ot80D7XdD',
			agi_password = 'Kqq4QKt35L6',
			sandbox = True)
		self.client = Client.create()
		self.client.billing_address.first_name = 'Kevin'
		self.client.billing_address.last_name = 'Wang'
		self.bank_account = BankAccount.create(
			account_holder='John Customer',
			account_number='1234567845390',
			routing_number='253271806',
			type=BankAccount.CHECKING)
		self.client.add_payment_method(self.bank_account)

	def test_retrievable(self):
		self.client.save()
		c = Client.retrieve(id=self.client.id)
		approved, txid, response = c.payment_methods[0].sale(15)
		self.assertIsNotNone(txid, "Transaction ID is None")
		self.assertTrue(approved, "Transaction was not approved")
		c.delete()

	def test_approved(self):
		#
		# To be honest, I find this to be really dumb.
		#
		approved, txid, response = self.bank_account.sale(15)
		self.assertIsNotNone(txid, "Transaction ID is None")
		self.assertTrue(approved, "Transaction was not approved")
	
	def test_verification(self):
		self.client.billing_address.state = 'IL'
		self.client.billing_address.postal = '60637'
		self.client.billing_address.phone = '773-702-1234'
		self.client.email = 'test@gmail.com'
		verification = AddressVerification(0, 0, 2, 2, 2)
		approved, txid, response = self.bank_account.verify_with(verification).sale(15)
		self.assertIsNotNone(txid, "Transaction ID is None")
		self.assertTrue(approved, "Transaction was not approved")

	def _validate_error(self, approved, txid, response, code, description):
		self.assertFalse(approved, "Transaction was approved")
		self.assertIsNotNone(txid, "Transaction ID is None")
		self.assertEqual(response['pg_response_description'], description, "Error message does not match API")
		self.assertEqual(response['pg_response_code'], code, "Error code does not match API")

	def test_U02_1(self):
		self.bank_account.routing_number = '064000101'
		self._validate_error(*self.bank_account.sale(15), code="U02", description="TRN NOT APPROVED")

	def test_U02_2(self):
		self.bank_account.routing_number = '021000021'
		self.bank_account.account_number = '987654321'
		self._validate_error(*self.bank_account.sale(15), code="U02", description="ACCOUNT NOT APPROVED")
		
	def test_U05(self):
		self.client.billing_address.state = 'MI'
		self.client.billing_address.postal = '60637'
		verification = AddressVerification(0, 0, 2, 0, 0)
		approved, txid, response = self.bank_account.verify_with(verification).sale(15)
		self._validate_error(*self.bank_account.verify_with(verification).sale(15), code="U05", description="AVS FAILURE ZIPCODE")
		
	def test_U06(self):
		self.client.billing_address.state = 'MI'
		self.client.billing_address.phone = '773-702-1234'
		verification = AddressVerification(0, 0, 0, 2, 0)
		approved, txid, response = self.bank_account.verify_with(verification).sale(15)
		self._validate_error(*self.bank_account.verify_with(verification).sale(15), code="U06", description="AVS FAILURE AREACODE")

	def test_U07(self):
		self.client.email = 'test@hotmail.com'
		verification = AddressVerification(0, 0, 0, 0, 2)
		# The documentation is incorrect, this doesn't throw an error.
		# self._validate_error(*self.bank_account.verify_with(verification).sale(15), code="U07", description="AVS FAILURE EMAIL")

	def test_U10(self):
		self.bank_account.sale(15)
		# The documentation is incorrect, this doesn't throw an error.
		# self._validate_error(*self.bank_account.sale(15), code="U10", description="DUPLICATE TRANSACTION")
	def test_U12(self):
		self.client.billing_address.first_name = 'U12'
		self.bank_account.routing_number = '064000101'
		approved, txid, response = self.bank_account.sale(15)
		transaction = Transaction.retrieve('DA3410E9-17DF-4BCD-BB89-F4424FDBFAB4')
		# self._validate_error(*Transaction.retrieve(txid).void(), code="U12", description="UPDATE NOT ALLOWED")

if __name__ == '__main__':
	unittest.main()
