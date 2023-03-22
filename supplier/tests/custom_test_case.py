from unittest import TestCase

from supplier.tests.helpers import get_bad_request

import json


class CustomTestCase(TestCase):
    data_file = None
    url = None
    post = None

    def setUp(self):
        with open(f'../datas/{self.data_file}', 'r') as f:
            self.data = json.load(f)

    def test_without_api_key(self):
        self.data.pop('api_key')
        print(self.data)
        get_bad_request(self, self.post)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        get_bad_request(self, self.post)

    def test_without_signature(self):
        self.data.pop('signature')
        get_bad_request(self, self.post)

    def test_invalid_signature(self):
        self.data['signature'] = '123'
        get_bad_request(self, self.post)
