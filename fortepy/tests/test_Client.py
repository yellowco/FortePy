from .. import Config
from ..Client import Client
import unittest
import datetime

class ClientTest(unittest.TestCase):
	def setUp(self):
		Config.config(merchant_id = 160361,
			transaction_key = '1NSa45VrQJk2j5',
			api_login_id = '5ot80D7XdD',
			agi_password = 'Kqq4QKt35L6')

	def test_client(self):
		client = Client.create()
		client.billing_address.first_name = 'Kevin'
		client.billing_address.last_name = 'Wang'
		client.email = 'kevmo314@gmail.com'
		client.save()
		self.assertIsNotNone(client.id, "Client did not save properly on the server")
		self.assertIsNotNone(Client.retrieve(client.id), "Could not retrieve the client from the server")
		self.assertEqual(Client.retrieve(client.id).email, client.email, "Email attribute not retrieved from the server")
		self.assertIsNone(Client.retrieve(-1), "An invalid client was returned from the server")
		self.assertRaises(Exception, Client.all)
		id = client.id
		client.email = 'newemail@mail.com'
		self.assertEqual(client.save().id, id, "The server created a new id instead of updating the existing one")
		self.assertEqual(Client.retrieve(id).email, client.email, "Email attribute was not updated")
		client.delete()
		self.assertIsNone(Client.retrieve(id), "Client was not deleted from the server")


if __name__ == '__main__':
	unittest.main()
