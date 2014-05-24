import requests
import xmltodict
import lxml.builder as lb

from lxml import etree
from xml.parsers.expat import ExpatError
from datetime import datetime


__version__ = '0.1'
__author__ = 'calvin'
__license__ = 'Apache Software License'


class SpreedlyError(Exception):

    """
    Exception Handling
    """

    def __init__(self, message=None, response=None):
        self.response = response
        self.code = response.status_code
        self.message = message

    def json(self):
        return xmltodict.parse(self.response.text, dict_constructor=dict)


class Client(object):

    """
    A client for the Spreedly API.

    See https://docs.spreedly.com
    for complete documentation for the API.
    """

    user_agent = 'SpreedlySdk/rest-sdk-spreedly 0.1'

    def __init__(self, environment_key, access_secret,
                 gateway_token=None, version='1', format_type='xml'):

        self.environment_key = environment_key
        self.access_secret = access_secret
        self.gateway_token = gateway_token
        self.version = version
        self.format_type = format_type

    def endpoint(self, action):
        return 'https://core.spreedly.com/v{version}/{action}.{type}'.format(
            version=self.version, action=action, type=self.format_type)

    @property
    def headers(self):
        return {
            'User-Agent': self.user_agent,
            'Content-Type': 'application/' + self.format_type
        }

    def _postprocessor(self, item, key, data):
        if isinstance(data, dict):
            item_type = data.get('@type')

            if item_type == 'boolean':
                data = data['#text'] == 'true'

            elif item_type == 'datetime':
                data = datetime.strptime(
                    data['#text'], "%Y-%m-%dT%H:%M:%SZ")

        return key, data

    def request(self, url, method, data=None, headers=None, **kwargs):
        http_headers = self.headers
        http_headers.update(headers or {})

        if data is not None:
            data = etree.tostring(data)

        response = requests.request(method, url, auth=(
            self.environment_key, self.access_secret),
            data=data, headers=http_headers, **kwargs)

        if response.status_code == 401:
            raise SpreedlyError('Unauthorized', response)

        if response.status_code == 402:
            raise SpreedlyError('Payment Required', response)

        if response.status_code == 422:
            raise SpreedlyError('Unprocessable', response)

        try:
            data = xmltodict.parse(
                response.text, postprocessor=self._postprocessor,
                dict_constructor=dict)

        except ExpatError:
            raise SpreedlyError('XML parse error', response)

        if not (200 <= response.status_code < 300):
            raise SpreedlyError('Client error', response)

        return data

    def get(self, action, params=None, headers=None):
        return self.request(self.endpoint(
            action), 'GET', params=None, headers=headers)

    def since(self, action, since_token=None):
        params = {}

        if since_token is not None:
            params['since_token'] = since_token

        return self.get(action, params=params)

    def post(self, action, data=None, headers=None):
        return self.request(self.endpoint(
            action), 'POST', data=data, headers=headers)

    def put(self, action, data=None, headers=None):
        return self.request(self.endpoint(
            action), 'PUT', data=data, headers=headers)

    def _nested(*keys):
        def wrap(f):
            def wrapped(self, *args, **kwargs):
                response = f(self, *args, **kwargs)
                return reduce(lambda d, k: d and d[k], keys, response)
            return wrapped
        return wrap

    @_nested('gateway')
    def gateway(self, gateway_type='test', **kwargs):
        data = lb.E.gateway(lb.E.gateway_type(gateway_type))

        for param, value in kwargs.iteritems():
            etree.SubElement(data, param).text = value

        return self.post('gateways', data=data)

    @_nested('gateway')
    def get_gateway(self, gateway_token):
        return self.get("gateways/{}".format(gateway_token))

    @_nested('gateways', 'gateway')
    def get_gateway_list(self, since_token=None):
        return self.since('gateways', since_token)

    def update_gateway(self, gateway_token, login, password):
        data = lb.E.gateway(lb.E.login(login), lb.E.password(password))
        return self.put("gateways/{}".format(gateway_token), data=data)

    def retain(self, gateway_token):
        return self.put("gateways/{}/retain".format(gateway_token))

    def redact(self, gateway_token):
        return self.put("gateways/{}/redact".format(gateway_token))

    @_nested('payment_method')
    def get_payment_method(self, payment_method):
        return self.get("payment_methods/{}".format(payment_method))

    @_nested('payment_methods', 'payment_method')
    def get_payment_method_list(self, since_token=None):
        """ API Issue: Empty list """
        return self.since('payment_methods', since_token)

    @_nested('transaction')
    def purchase(self, amount, currency_code, payment_method_token,
                 retain_on_success=False, payment_type='purchase'):

        data = lb.E.transaction(
            lb.E.amount(str(amount)),
            lb.E.currency_code(currency_code),
            lb.E.payment_method_token(payment_method_token))

        if retain_on_success:
            data.getchildren().append(lb.E.retain_on_success('true'))

        return self.post("gateways/{}/{}".format(
            self.gateway_token, payment_type), data=data)

    @_nested('transaction')
    def reference(self, amount, currency_code, transaction_token):
        data = lb.E.transaction(
            lb.E.amount(str(amount)),
            lb.E.currency_code(currency_code))

        return self.post("transactions/{}/purchase".format(
            transaction_token), data=data)

    def authorize(self, amount, currency_code, payment_method_token):
        return self.purchase(
            amount=amount, currency_code=currency_code,
            payment_method_token=payment_method_token,
            payment_type='authorize')

    @_nested('transaction')
    def capture(self, transaction_token):
        return self.post("transactions/{}/capture".format(transaction_token))

    @_nested('transaction')
    def void(self, transaction_token):
        return self.post("transactions/{}/void".format(transaction_token))

    @_nested('transaction')
    def credit(self, transaction_token):
        return self.post("transactions/{}/credit".format(transaction_token))

    @_nested('transaction')
    def get_transaction(self, transaction_token):
        return self.get("transactions/{}".format(transaction_token))

    @_nested('transactions', 'transaction')
    def get_transaction_list(self, since_token=None):
        return self.since('transactions', since_token)

    @_nested('transactions', 'transaction')
    def get_payment_method_transaction_list(
            self, payment_method_token, since_token=None):
        action = "payment_methods/{}/transactions".format(payment_method_token)
        return self.since(action, since_token)

    @_nested('transactions', 'transaction')
    def get_gateway_transaction_list(self, gateway_token, since_token=None):
        action = "gateways/{}/transactions".format(gateway_token)
        return self.since(action, since_token)
