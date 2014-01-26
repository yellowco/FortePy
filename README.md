# FortePy

Python bindings for the [Forte payment network](http://www.forte.net/).

Still in development. The API below is guaranteed, but functionality is not at the moment.

[![Build Status](https://travis-ci.org/kevmo314/FortePy.png?branch=master)](https://travis-ci.org/kevmo314/FortePy) [![Coverage Status](https://coveralls.io/repos/kevmo314/FortePy/badge.png)](https://coveralls.io/r/kevmo314/FortePy)

## Configure

```
import fortepy
fortepy.config(merchant_id, api_login_id, transaction_key, agi_password, sandbox, require_compliance)
```

By default, `sandbox` is set to `False` and `require_compliance` is set to `False`. The other parameters must be initialized.

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
client.add_payment_method(bank_account)
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

### Arbitrary attribute storage

FortePy has the ability to use the `Note` property as a blob type to store arbitrary data objects, which are saved along with the payment method.

```
import fortepy
fortepy.config(merchant_id, api_login_id, transaction_key, agi_password)

client = fortepy.Client.retrieve(id=client_id)
client.payment_methods[k].my_property = 15
client.save()
```

To disable this feature, issue `fortepy.config(require_compliance=True)`.

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

### Fancier stuff

```
import fortepy
fortepy.config(merchant_id, api_login_id, transaction_key, agi_password)

client = fortepy.Client.retrieve(id=client_id)
order = fortepy.Order()
verification = fortepy.AddressVerification()
recurrence = fortepy.Recurrence()
tx_id = client.payment_methods[0]
	.regarding_order(order)
	.including_recurrence(recurrence)
	.verify_with(verification)
	.sale(15)
```

## Properties and Methods

### fortepy.Client

#### Properties

```
id:12345 # read only
email:'somewhere@there.com'
consumer_id:12345
billing_address:<fortepy.Address>
shipping_address:<fortepy.Address>
status:<fortepy.Client.[ACTIVE|DELETED|SUSPENDED]>
ssn:"123-45-6789"
drivers_license:<fortepy.DriversLicense>
birthdate:<datetime>
ip:"123.123.123.123"
payment_methods:[<fortepy.PaymentMethod>]
transactions:[<fortepy.Transaction>] #read only
```

#### Methods

```
fortepy.Client.create() returns <fortepy.Client>
fortepy.Client.retrieve(id) returns <fortepy.Client>
fortepy.Client().save() returns self
fortepy.Client().delete() returns self
fortepy.Client().verify() returns string of xml, see [Forte documentation](http://www.paymentsgateway.com/developerDocumentation/Integration/webservices.aspx) for details
```

### fortepy.Address

#### Properties

```
first_name:'John'
last_name:'Customer'
street1:'132 there'
street2:'apt 123'
city:'somecity'
state:'IL'
postal:'01234'
country:'USA'
phone:'1234567890'
fax:'1234567890'
```

### fortepy.DriversLicense

#### Properties

```
number:'W293847425345234'
state:'IL'
```

### fortepy.BankAccount extends fortepy.PaymentMethod

#### Properties

```
id:23094832 # read only
client:<fortepy.Client>
note:"some note"
account_holder:'John Client'
is_default:True
account_number:'01253499345'
routing_number:'043958345'
type:<fortepy.BankAccount.[CHECKING|SAVINGS]>
```

#### Methods

```
fortepy.BankAccount.create() returns <fortepy.CreditCard>
fortepy.BankAccount.retrieve(id) returns <fortepy.PaymentMethod> # note that this may return a credit card object
fortepy.BankAccount().sale(amount) returns (approved[True|False], tx_id, {<response data>})
fortepy.BankAccount().authorization(amount) returns (approved[True|False], tx_id, {<response data>})
fortepy.BankAccount().credit(amount) returns (approved[True|False], tx_id, {<response data>})
fortepy.BankAccount().force(amount) returns (approved[True|False], tx_id, {<response data>})
fortepy.BankAccount().verify(amount) returns (approved[True|False], tx_id, {<response data>})
fortepy.BankAccount().save() returns self
fortepy.BankAccount().delete() returns self
```

### fortepy.CreditCard extends fortepy.PaymentMethod

#### Properties

```
id:23094832 # read only
client:<fortepy.Client>
note:"some note"
account_holder:'John Client'
is_default:True
card_number:'01253499345'
expiration_date:<datetime>
card_type:<fortepy.CreditCard.[VISA|MAST|DISC|AMER|DINE|JCB]>
is_procurement_card:True
```

#### Methods

```
fortepy.CreditCard.create() returns <fortepy.CreditCard>
fortepy.CreditCard.retrieve(id) returns <fortepy.PaymentMethod> # note that this may return a bank account object
fortepy.CreditCard().sale(amount) returns (approved[True|False], tx_id, {<response data>})
fortepy.CreditCard().authorization(amount) returns (approved[True|False], tx_id, {<response data>})
fortepy.CreditCard().credit(amount) returns (approved[True|False], tx_id, {<response data>})
fortepy.CreditCard().preauthorization(amount) returns (approved[True|False], tx_id, {<response data>})
fortepy.CreditCard().balance_inquiry(amount) returns (approved[True|False], tx_id, {<response data>})
fortepy.CreditCard().save() returns self
fortepy.CreditCard().delete() returns self
```
