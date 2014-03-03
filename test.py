import fortepy

fortepy.config(merchant_id = 160361,
	transaction_key = '1NSa45VrQJk2j5',
	api_login_id = '5ot80D7XdD',
	agi_password = 'Kqq4QKt35L6',
	sandbox = True)

client = fortepy.Client.create()
client.billing_address.first_name = 'Kevin'
client.billing_address.last_name = 'Wang'
client.email = 'kevmo314@gmail.com'
client.save()

verify = fortepy.IDVerify(client)