from .. import Config
from ..Client import Client
import unittest
import datetime

class Test(unittest.TestCase):
	def test_client(self):
		Config.config(merchant_id = 160361,
			transaction_key = '1NSa45VrQJk2j5',
			api_login_id = '5ot80D7XdD',
			agi_password = 'Kqq4QKt35L6')
		self.client = Client.create()
		self.client.billing_address.first_name = 'Kevin'
		self.client.billing_address.last_name = 'Wang'
		self.client.email = 'kevmo314@gmail.com'
		self.assertIsNotNone(self.client.save().id, "Client did not save properly on the server")
		self.assertIsNotNone(Client.retrieve(self.client.id), "Could not retrieve the client from the server")
		self.assertEqual(Client.retrieve(self.client.id).email, self.client.email, "Email attribute not retrieved from the server")
		self.assertIsNone(Client.retrieve(-1), "An invalid client was returned from the server")
		self.assertRaises(Exception, Client.all)
		id = self.client.id
		self.client.email = 'newemail@mail.com'
		self.assertEqual(self.client.save().id, id, "The server created a new id instead of updating the existing one")
		self.assertEqual(Client.retrieve(id).email, self.client.email, "Email attribute was not updated")
		self.client.delete()
		self.assertIsNone(Client.retrieve(id), "Client was not deleted from the server")

if __name__ == '__main__':
	unittest.main()
