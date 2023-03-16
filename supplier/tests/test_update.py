from django.test import TestCase

from rest_framework import status

from supplier.helpers import get_bad_request, request_with_data

import json


class UpdateApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/update_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/update/v1/"

    def test_pending(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        print(f"response message: {data.get('message')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('success'), True)

    def test_pending_gt_boundary(self):
        self.data['amount'] = 100001
        self.data['signature'] = "49521483ce984118a78dc30b399acaff62288d898d61ac69590f6d331fdc5224"
        get_bad_request(self, post=True)

    def test_pending_lt_boundary(self):
        self.data['amount'] = "0"
        self.data['signature'] = "2338f1c1f05bb8540012da69e7b0ffd5e4d72a0b95331c1d822a89f6af44ce5f"
        get_bad_request(self, post=True)

    def test_completed(self):
        self.data['token'] = '344b73ae65e44b2abbf'
        self.data['signature'] = 'c90403d938cdba9ebf8e05f1d676bd71bed53e7e490e28bee83f67803a0f2924'
        self.data['amount'] = 250
        get_bad_request(self, post=True)

    def test_completed_bumper_reference(self):
        self.data['bumper_reference'] = 156301
        self.data['signature'] = '29da8c4eceefb566ff42d7a588d06cc56878577a0a71b25de9a34776ccccca58'
        self.data['amount'] = 250
        del self.data['token']
        get_bad_request(self, post=True)

    def test_failed(self):
        self.data['token'] = '79d430f2ff164c6db44'
        self.data['signature'] = 'b61d027f8c060f9ae1c8a0e362828b42977892bd3d815a1ef6829242ad0a3206'
        get_bad_request(self, post=True)

    def test_canceled(self):
        self.data['token'] = '36602370aabf46c7abb'
        self.data['signature'] = '28a88167629adfb05527cf9c28d612d7cc5fc56fb07030b909376fddacceb8e1'
        get_bad_request(self, post=True)

    def test_invalid_bumper_reference(self):
        self.data['bumper_reference'] = "0"
        self.data['signature'] = 'd77d843d428cad0b6b50a91066e5ab25309c2cb6e7382b53c90d918fa1c804bd'
        del self.data['token']
        get_bad_request(self, post=True)

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        get_bad_request(self, post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        get_bad_request(self, post=True)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '28afeda6cff7b815e6d658881cfb16c26db085f120af20f91def0b987900e5e3'
        get_bad_request(self, post=True)