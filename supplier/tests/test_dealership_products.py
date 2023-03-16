from django.test import TestCase

from rest_framework import status

from supplier.helpers import get_bad_request, request_with_data

import json


class DealershipProductsTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/products_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/products/v1/"

    def test_valid_data(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data'))

    def test_without_api_key(self):
        del self.data['api_key']
        get_bad_request(self)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        get_bad_request(self)

    def test_without_signature(self):
        del self.data['signature']
        get_bad_request(self)

    def test_invalid_signature(self):
        self.data['signature'] = '123'
        get_bad_request(self)

    def test_without_amount(self):
        del self.data['amount']
        self.data['signature'] = 'a7a35e3a9434ad9b4b6617a331964472043fcad3ea3b06b207559b43fe1144a2'
        self.test_valid_data()
