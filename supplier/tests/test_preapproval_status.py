from django.test import TestCase

from rest_framework import status

from supplier.helpers import get_bad_request, request_with_data

import json


class PreapprovalStatusTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/preapproval_status_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/preapprovalstatus/v1/"

    def test_valid_data(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))
        self.assertEquals(data.get('data').get('token'), 'eraytesttoken')

    def test_without_token(self):
        del self.data['preapproval_token']
        response = request_with_data(self)

        print(f"response message: {response.json().get('message')}")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

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
        self.data['preapproval_token'] = '123'
        get_bad_request(self)