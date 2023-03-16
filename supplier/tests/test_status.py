from django.test import TestCase

from rest_framework import status

from supplier.helpers import get_bad_request, request_with_data

import json


class StatusApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/status_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/status/v1/"

    def test_completed(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))
        self.assertIsNotNone(data.get('data').get('amount'))

    def test_pending(self):
        self.data['token'] = '5d62808653ff416c881'
        self.data['signature'] = 'd53c9dffaba98a2108cef5b4019ae0829d7970812d189d7edacc3195a288fa53'

        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))
        self.assertEquals(data.get('data').get('status'), 'pending')
        self.assertIsNone(data.get('data').get('amount'))

    def test_cancelled(self):
        self.data['token'] = 'ae4e985f8a1c4c91b41'
        self.data['signature'] = 'e3cdc904142a0d6d01758dd35f5746e11d0d1f7ad51f44674d95bbd750777f28'

        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))

    def test_valid_data_customer_reference(self):
        del self.data['token']
        self.data['bumper_reference'] = 156284
        self.data['signature'] = '5e7455b616d651ee07350b1688ec234ce16cc9597e72be84b9daa545b8853ef0'
        self.test_completed()

    def test_invalid_customer_reference(self):
        del self.data['token']
        self.data['bumper_reference'] = 0
        self.data['signature'] = '3f8eb5fbea14ef21d823e7d40c2f41c8a1af37bc44a0e4c8e7bfbdffdf856013'
        get_bad_request(self)

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
