from django.test import TestCase

from rest_framework import status

from supplier.helpers import get_bad_request, request_with_data

import json


class PaymentCancelApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/payment_cancel_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/payment-cancel/v1/"

    def test_valid(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        print(f"response message: {data.get('message')}")
        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancelled(self):
        self.data['token'] = '5799a418e9f142f5819af3bd30972dad'
        self.data['signature'] = 'c6c26e0787e735c7c1466004291e781fdd1bf8d0e44407ed31a31e792e178ae8'
        get_bad_request(self, post=True)

    def test_without_signature(self):
        del self.data['signature']
        get_bad_request(self, post=True)

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        get_bad_request(self, post=True)

    def test_without_api_key(self):
        del self.data['api_key']
        get_bad_request(self, post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        get_bad_request(self, post=True)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '1fe8bac276f93c94639b467841a54b5b6d89a086a9dd5796f27b683c1f7f69a3'
        get_bad_request(self, post=True)
