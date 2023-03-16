from django.test import TestCase

from rest_framework import status

from supplier.helpers import get_bad_request, request_with_data

import json


class PaymentApplicationTest(TestCase):
    longString = "x" * 256

    def setUp(self):
        self.data = json.load(open('supplier/datas/payment_application_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/payment/v1/"

    def test_valid_data(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        print(f"response message: {data.get('message')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data').get('token'))
        self.assertIsNotNone(data.get('data').get('redirect_url'))

    def test_amount_gt_boundary(self):
        max_amount = 10000
        self.data['amount'] = max_amount + 1
        self.data['signature'] = "a7b679bfdab9ec10938d1f1ae18e33bb5b7edebd356a87cf32bfe2b92affe305"
        get_bad_request(self, post=True)

    def test_amount_lt_boundary(self):
        min_amount = 1
        self.data['amount'] = min_amount - 1
        self.data['signature'] = "5dc0ead2d701c169121371b97d93998d552e2862ff973a20d0d662f98ffcdb37"
        get_bad_request(self, post=True)

    def test_without_amount(self):
        del self.data['amount']
        self.data['signature'] = 'af4c878c871e5c759ed210c894241892e587ad5ddb087b05e0c5514f1c9af292'
        get_bad_request(self, post=True)

    def test_without_api_key(self):
        del self.data['api_key']
        get_bad_request(self, post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        get_bad_request(self, post=True)

    def test_without_signature(self):
        del self.data['signature']
        get_bad_request(self, post=True)

    def test_invalid_signature(self):
        self.data['signature'] = '123'
        get_bad_request(self, post=True)

    def test_without_currency(self):
        del self.data['currency']
        self.data['signature'] = '951224e0a6372466d22fca5ce4734a10f625b7ca6b063bb61db8f2368b6a1462'
        get_bad_request(self, post=True)

    def test_invalid_currency(self):
        self.data['currency'] = 'TL'
        self.data['signature'] = 'b20179b74b7ed54bb8ab3025f8c3eb0862762f86abe7dcdd6c944ce0dcda17da'
        get_bad_request(self, post=True)

    def test_without_order_reference(self):
        del self.data['order_reference']
        self.data['signature'] = '4900e069a08c89cbd17a9b57448a9c25e0753aebab67521c3c649326cf3aa968'
        get_bad_request(self, post=True)

    def test_without_registration(self):
        del self.data['registration']
        self.data['signature'] = 'f984ece1fe9154b362b257be8dff4177347f81bc4b1a1c914a32a3b11712edb4'
        get_bad_request(self, post=True)

    def test_without_product_name(self):
        del self.data['product_name']
        self.data['signature'] = '5e99b28ebc1f9f08f733008886aa26d17450f045f20a5cf5fd884d07dac1abd7'
        get_bad_request(self, post=True)

    def test_invalid_product_name(self):
        self.data['product_name'] = ''
        self.data['signature'] = '3187d91cd7e2ffa836bd1f170bfb4cbdd85bd89e0e8359e9dfb35df3f48ae208'
        get_bad_request(self, post=True)

    def test_product_name_len_gt_boundary(self):
        self.data['product_name'] = self.longString
        self.data['signature'] = '9ca0c48b12b37363267628b61893ad4afc9b2933af5ae264d7bcaf8f3a8dab2a'
        get_bad_request(self, post=True)

    def test_order_reference_len_gt_boundary(self):
        self.data['order_reference'] = self.longString
        self.data['signature'] = '7654e30b151970d800b917bc855b0edccd132a4e9f725b3a35f9bfcfbdff08a4'
        get_bad_request(self, post=True)

    def test_success_url_len_gt_boundary(self):
        self.data['success_url'] = self.longString
        self.data['signature'] = '2c2df10239b35b4f42a024c322566329bc73e0371c7e53f72fc8a220a973f2a0'
        get_bad_request(self, post=True)

    def test_failure_url_len_gt_boundary(self):
        self.data['failure_url'] = self.longString
        self.data['signature'] = '4c20442ab297e10a9cb79458ab953daf819d7a42160f369dce75c3853f1ad13b'
        get_bad_request(self, post=True)

    def test_registration_len_gt_boundary(self):
        self.data['registration'] = "x" * 13
        self.data['signature'] = '822377bea1e860a87c4bcc736226d9e50254e0da2ff651c2c6344e7a1b814978'
        get_bad_request(self, post=True)
