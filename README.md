This library provides a pure Python interface to the Spreedly REST APIs.

## Installation
The easiest way to install the latest version
is by using pip/easy_install to pull it from Github:

    $ pip install git+https://github.com/calvinpy/spreedly-sdk
    $ easy_install git+https://github.com/calvinpy/spreedly-sdk

You may also use Git to clone the repository from
Github and install it manually:

    $ git clone https://github.com/calvinpy/spreedly-sdk
    $ python setup.py install

## Documentation
  - [Quick Start](https://docs.spreedly.com/)
  - [Payment methods](https://docs.spreedly.com/payment-methods/)
  - [Gateways](https://docs.spreedly.com/gateways/)
  - [Transactions](https://docs.spreedly.com/transactions/)
  - [Supported Credit Card Types](https://docs.spreedly.com/credit-card-types)
  - [Error Handling](https://docs.spreedly.com/error-handling)


## Basic usage
### Client
```python
import spreedly

client = spreedly.Client(ENVIRONMENT_KEY, ACCESS_SECRET)
```

### Gateways

To use Spreedly Core you have to have at least one gateway. 
You can create a test gateway, by default . 

#### Payment Gateway
```python
client.gateway()
```

```python
{
  'characteristics': {
    'supports_3dsecure_authorize': True,
    'supports_3dsecure_purchase': True,
    'supports_authorize': True,
    'supports_capture': True,
    'supports_credit': True,
    'supports_offsite_authorize': True,
    'supports_offsite_purchase': True,
    'supports_purchase': True,
    'supports_purchase_via_preauthorization': True,
    'supports_reference_authorization': True,
    'supports_reference_purchase': True,
    'supports_remove': True,
    'supports_store': True,
  'supports_void': True
  },
  'created_at': datetime.datetime(2014, 5, 25, 0, 30, 45),
  'credentials': None,
  'gateway_specific_fields': None,
  'gateway_type': 'test',
  'name': 'Spreedly Test',
  'payment_methods': {
    'payment_method': [
      'credit_card',
      'sprel',
      'third_party_token',
      'bank_account'
     ]
  },
  'redacted': False,
  'state': 'retained',
  'token': 'U2JKWnRYIsNKWfta9kITRUbci0j',
  'updated_at': datetime.datetime(2014, 5, 25, 0, 30, 45)
}
```

Each gateway type has a different set of credentials needed to communicate with it and are only available in some countries.

[Supported gateways](https://spreedly.com/gateways)

```python
client.gateway(gateway_type, **credential_data)
```

#### Retrieve gateway

```python
gateway_token = 'U2JKWnRYIsNKWfta9kITRUbci0j'
client.get_gateway(gateway_token)
```

```python
client.get_gateway_list()
client.get_gateway_list(since_token=gateway_token)
```

#### Update gateway

If you create a gateway using a normal authenticated add gateway api call, the gateway is automatically retained.

If a gateway is created using an unauthenticated channel such as client-side scripting, it is kept in a cached state until it is retained or automatically redacted. This allows your customers to create gateways using their own credentials, but until you retain it, it cannot be used and you will not be billed for it.

```python
client.retain(gateway_token)
```

Gateways can't be deleted (since they're permanently associated with any transactions run against them), but the sensitive credential information in them can be redacted so that they're inactive:


```python
client.redact(gateway_token)
```

### Payments

#### Purchase

A purchase call immediately takes funds from the payment method (assuming the transaction succeeds).

```python
payment_method_token = 'CwhkxFxm5nzn3cts4t7TzasgWBl'
client.purchase(100, 'EUR', payment_method_token, gateway_token)
```

```python
{
  'amount': 100,
  'api_urls': None,
  'created_at': datetime.datetime(2014, 5, 25, 1, 9, 43),
  'currency_code': 'EUR',
  'description': None,
  'email': None,
  'gateway_specific_fields': None,
  'gateway_specific_response_fields': None,
  'gateway_token': 'VacV0dCGUwU2Ydu0IZOBzFHxQQN',
  'gateway_transaction_id': '64',
  'ip': None,
  'merchant_location_descriptor': None,
  'merchant_name_descriptor': None,
  'message': {
    'messages.transaction_succeeded': 'Succeeded!'
  },
  'on_test_gateway': True,
  'order_id': None,
  'payment_method': {
    'address1': None,
    'address2': None,
    'card_type': 'visa',
    'city': None,
    'country': None,
    'created_at': datetime.datetime(2014, 5, 25, 1, 8, 45),
    'data': None,
    'email': None,
    'errors': None,
    'first_name': 'Smith',
    'first_six_digits': '411111',
    'full_name': 'Smith Smith',
    'last_four_digits': '1111',
    'last_name': 'Smith',
    'month': 12,
    'number': 'XXXX-XXXX-XXXX-1111',
    'payment_method_type': 'credit_card',
    'phone_number': None,
    'state': None,
    'storage_state': 'used',
    'test': True,
    'token': 'CwhkxFxm5nzn3cts4t7TzasgWBl',
    'updated_at': datetime.datetime(2014, 5, 25, 1, 9, 43),
    'verification_value': None,
    'year': 2017,
    'zip': None
  },
    'response': {
    'avs_code': None,
    'avs_message': None,
    'cancelled': False,
    'created_at': datetime.datetime(2014, 5, 25, 1, 9, 43),
    'cvv_code': None,
    'cvv_message': None,
    'error_code': None,
    'error_detail': None,
    'message': 'Successful purchase',
    'pending': False,
    'success': True,
    'updated_at': datetime.datetime(2014, 5, 25, 1, 9, 43)
  },
  'state': 'succeeded',
  'succeeded': True,
  'token': '8qge2CZBikhXr44c6vi1tqvjFVw',
  'transaction_type': 'Purchase',
  'updated_at': datetime.datetime(2014, 5, 25, 1, 9, 43)
}
```

If the purchase or authorize is successful, you may then want to retain the payment method. Passing the retain_on_success parameter to the purchase or authorize call can save you from having to make another API call to do the retain. If the purchase or authorize succeeds, then the payment method is retained for you.

```python
client.purchase(100, 'EUR', payment_method_token, gateway_token, retain_on_success=True)
```

#### Purchase using a reference transaction


Some gateways require some of their customers to submit a CVV value for all of their transactions. If you're one of the very few customers who can't seem to convince your gateway to remove the CVV requirement, reference transactions may help. And in some cases, using reference transactions can lower decline rates.

```python
transaction_token = '8qge2CZBikhXr44c6vi1tqvjFVw'
client.reference(100, 'EUR', payment_method_token, transaction_token)
```

```python
{
  'amount': 100,
  'api_urls': None,
  'created_at': datetime.datetime(2014, 5, 25, 1, 13, 29),
  'currency_code': 'EUR',
  'description': None,
  'email': None,
  'gateway_specific_fields': None,
  'gateway_specific_response_fields': None,
  'gateway_token': 'VacV0dCGUwU2Ydu0IZOBzFHxQQN',
  'gateway_transaction_id': '61',
  'ip': None,
  'merchant_location_descriptor': None,
  'merchant_name_descriptor': None,
  'message': {
    'messages.transaction_succeeded': 'Succeeded!'
  },
  'on_test_gateway': True,
  'order_id': None,
  'reference_token': '8qge2CZBikhXr44c6vi1tqvjFVw',
  'response': {
    'avs_code': None,
    'avs_message': None,
    'cancelled': False,
    'created_at': datetime.datetime(2014, 5, 25, 1, 13, 29),
    'cvv_code': None,
    'cvv_message': None,
    'error_code': None,
    'error_detail': None,
    'message': 'Successful purchase',
    'pending': False,
    'success': True,
    'updated_at': datetime.datetime(2014, 5, 25, 1, 13, 29)
  },
  'state': 'succeeded',
  'succeeded': True,
  'token': 'Xgv6FUCtMIFNhj8n5ibZCuEXldV',
  'transaction_type': 'PurchaseViaReference',
  'updated_at': datetime.datetime(2014, 5, 25, 1, 13, 29)
}
```



#### Authorization

An authorize works just like a purchase; the difference being that it doesn't actually take the funds. NOTE: authorize will hold funds on some payment methods, notably debit cards.

```python
client.authorize(100, 'EUR', payment_method_token, gateway_token)
```

```
{
  ...
  'transaction_type': 'Authorization'
  ...
}


```
#### Update payment
A capture will actually take the funds previously reserved via an authorization.

```python
client.capture(transaction_token)
```

Void is used to cancel out authorizations and, with some gateways, to cancel actual payment transactions within the first 24 hours (credits are used after that; see below).

```python
client.void(transaction_token)
```

A credit is like a void, except it actually reverses a charge instead of just canceling a charge that hasn't yet been made. It's a refund.

```python
client.credit(transaction_token)
```


#### Retrieve transactions

A particular transaction.

```python
client.get_transaction(transaction_token)
```

The details of the transactions for your account.

```python
client.get_transaction_list()
client.get_transaction_list(since_token=transaction_token)
```

The details of the transactions for a payment method.

```python
client.get_payment_method_transaction_list(payment_method_token)
client.get_payment_method_transaction_list(payment_method_token, since_token=transaction_token)
```

The details of the transactions for a gateway.

```python
client.get_gateway_transaction_list(gateway_token)
client.get_gateway_transaction_list(gateway_token, since_token=transaction_token)
```



