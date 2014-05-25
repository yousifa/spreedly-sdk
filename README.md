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

#### Add Payment Gateway
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

[Supported gateways](https://spreedly.com/gateways)
```python
client.gateway(gateway_type, **data)
```

#### Retrieve gateways

```python
gateway_token = 'U2JKWnRYIsNKWfta9kITRUbci0j'
client.get_gateway(gateway_token)
```

```python
client.get_gateway_list()
client.get_gateway_list(since_token=gateway_token)
```

#### Gateway operations

```python
client.retain(gateway_token)
client.redact(gateway_token)
```

### Payments

#### Add Purchase
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

```python
client.purchase(100, 'EUR', payment_method_token, gateway_token, retain_on_success=True)
```

#### Add Authorization
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
#### Payment operations
```python
client.capture(transaction_token)
```

```python
client.void(transaction_token)
```

```python
client.credit(transaction_token)
```

```python
client.credit(transaction_token)
```

#### Retrieve transactions

```python
client.get_transaction(transaction_token)
```

```python
client.get_transaction_list()
client.get_transaction_list(since_token=transaction_token)
```

```python
client.get_payment_method_transaction_list(payment_method_token)
client.get_payment_method_transaction_list(payment_method_token, since_token=transaction_token)
```

```python
client.get_gateway_transaction_list(gateway_token)
client.get_gateway_transaction_list(gateway_token, since_token=transaction_token)
```



