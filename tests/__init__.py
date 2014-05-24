#!/usr/bin/env python
#
# Copyright 2014-2015 calvin
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import unittest
import spreedly


class SpreedlySdkTest(unittest.TestCase):

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
    unittest.main()
