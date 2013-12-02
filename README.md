# FortePy

Python bindings for the Forte payment network.

## Clients

### Creating a new client

```
import fortepy
fortepy.config(merchant_id, api_login_id, transaction_key, agi_password)

client = fortepy.Client.create(email='user@place.com')
client.billing_address = fortepy.Address(
	first_name='John', 
	last_name='Customer',
	company='SalesCo',
	street1='123 Sales Street',
	street2='Unit 3409',
	city='Chicago',
	state='IL',
	postal='60606',
	country='USA',
	phone='1234567890',
	fax='1234567899')
client.save()
```

### Finding and deleting a client

```
import fortepy
fortepy.config(merchant_id, api_login_id, transaction_key, agi_password)

client = fortepy.Client.retrieve(id=client_id)
client.delete()
```

## Payment Methods

### Creating a new payment method

```
import fortepy
fortepy.config(merchant_id, api_login_id, transaction_key, agi_password)

client = fortepy.Client.retrieve(id=client_id)
bank_account = fortepy.BankAccount.create(
	account_holder='John Customer',
	account_number='1234567890',
	routing_number='1234567890',
	type=fortepy.BankAccount.CHECKING)
client.payment_methods.append(bank_account)
client.save()
```

### Removing a payment method

```
import fortepy
fortepy.config(merchant_id, api_login_id, transaction_key, agi_password)

client = fortepy.Client.retrieve(id=client_id)
client.payment_methods[k].delete() # delete the kth payment method
```

Note that because `payment_methods` is cached, it may be wise to also issue `payment_methods.pop(k)`. `client` does not need to be saved afterwards as it is automatically applied.

## Transactions

### Issuing a transaction

```
import fortepy
fortepy.config(merchant_id, api_login_id, transaction_key, agi_password)

client = fortepy.Client.retrieve(id=client_id)
tx_id = client.payment_methods[0].sale(15)
```

Upon completion, `client.transactions` will contain a record of this transaction. Note that transactions cannot be added or modified directly, as they are historical records only.

### Finding a transaction

```
import fortepy
fortepy.config(merchant_id, api_login_id, transaction_key, agi_password)

transaction = fortepy.Transaction.retrieve(id=tx_id)
transaction.void() # or something
```