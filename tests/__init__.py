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
            self.environment_key = os.environ['SPREEDLY_ENVIRONMENT_KEY']
            self.access_secret = os.environ['SPREEDLY_ACCESS_SECRET']
        except KeyError:
            raise Exception(
                'SPREEDLY_ENVIRONMENT_KEY and SPREEDLY_ACCESS_SECRET '
                'must be set as environmental variables.')

    def test_gateway(self):
        client = spreedly.Client(self.environment_key, self.access_secret)
        assert(client.gateway())


if __name__ == '__main__':
    unittest.main()
