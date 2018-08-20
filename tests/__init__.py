#!/usr/bin/env python

import os
from unittest import main, mock, TestCase
import spreedly_sdk as spreedly
from lxml import etree


class SpreedlySdkTest(TestCase):

    def setUp(self):

        try:
            self.client = spreedly.Client(
                os.environ['SPREEDLY_ENVIRONMENT_KEY'],
                os.environ['SPREEDLY_ACCESS_SECRET'])

            self.gateway_token = os.environ['SPREEDLY_GATEWAY_TOKEN']
            self.payment_method_token = os.environ[
                'SPREEDLY_PAYMENT_METHOD_TOKEN']

        except KeyError:
            raise Exception(
                'SPREEDLY_ENVIRONMENT_KEY, SPREEDLY_ACCESS_SECRET, '
                'SPREEDLY_GATEWAY_TOKEN and SPREEDLY_PAYMENT_METHOD_TOKEN '
                'must be set as environmental variables.')

    def test_gateway(self):
        response = self.client.gateway()

        self.assertEqual(response['gateway_type'], 'test')
        self.assertEqual(response['state'], 'retained')

    def test_get_gateway(self):
        response = self.client.get_gateway(self.gateway_token)
        self.assertEqual(response['token'], self.gateway_token)

    def test_get_gateway_list(self):
        response = self.client.get_gateway_list()
        self.assertIsNot(len(response), 0)

    def issue_test_retain(self):
        response = self.client.retain(self.gateway_token)
        self.assertEqual(response['token'], self.gateway_token)

    def expired_test_redact(self):
        response = self.client.redact(self.gateway_token)

        self.assertTrue(response['succeeded'])
        self.assertTrue(response['gateway']['redacted'])
        self.assertEqual(response['gateway']['state'], 'redacted')
        self.assertEqual(response['gateway']['token'], self.gateway_token)

    def expired_test_purchase(self):
        amount = 100
        currency_code = 'EUR'

        response = self.client.purchase(
            amount, currency_code,
            self.payment_method_token, self.gateway_token)

        self.assertTrue(response['succeeded'])
        self.assertEqual(response['amount'], amount)
        self.assertEqual(response['currency_code'], currency_code)
        self.assertEqual(response['transaction_type'], 'Purchase')

        self.assertEqual(response['gateway_token'], self.gateway_token)
        self.assertEqual(
            response['payment_method']['token'], self.payment_method_token)

    def test_purchase_with_extra_gateway_parameters(self):
        amount = 100
        currency_code = 'EUR'

        with mock.patch('spreedly_sdk.Client.post') as post_method:
            self.client.purchase(
                amount, currency_code,
                self.payment_method_token, self.gateway_token,
                gateway_specific_fields={'openpay': {'device_session_id': '1232132sasdas'}})
            data = post_method.call_args[1]['data']
            self.assertIn(
                '<gateway_specific_fields><openpay><device_session_id>1232132sasdas</device_session_id></openpay></gateway_specific_fields>'.encode(),
                etree.tostring(data)
            )

    def test_get_payment_method(self):
        response = self.client.get_payment_method(self.payment_method_token)
        self.assertEqual(response['token'], self.payment_method_token)

    def test_get_transaction_list(self):
        response = self.client.get_transaction_list()
        self.assertIsNot(len(response), 0)

    def test_get_payment_method_transaction_list(self):
        response = self.client.get_payment_method_transaction_list(
            self.payment_method_token)

        self.assertIsNot(len(response), 0)

    def test_get_gateway_transaction_list(self):
        response = self.client.get_gateway_transaction_list(self.gateway_token)
        self.assertIsNot(len(response), 0)


if __name__ == '__main__':
    main()
