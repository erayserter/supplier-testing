from django.test import TestCase

from rest_framework import status

from supplier.helpers import get_bad_request, request_with_data

import json


class PaymentStatusApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/payment_status_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/paymentstatus/v1/"

    def test_valid_data(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))

    def test_not_found(self):
        self.data['token'] = 'd4ecf522fe6b42ccb75937fed7e094f5'
        self.data['signature'] = '338cea4e4fb951350ef86ac13408d9e96bf22cb45016edc3e665e88ada0e93c2'

        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.
        self.assertEqual(data.get('success'), False)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_without_signature(self):
        del self.data['signature']
        get_bad_request(self)

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        get_bad_request(self)

    def test_without_api_key(self):
        del self.data['api_key']
        get_bad_request(self)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        get_bad_request(self)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '1fe8bac276f93c94639b467841a54b5b6d89a086a9dd5796f27b683c1f7f69a3'
        get_bad_request(self)
