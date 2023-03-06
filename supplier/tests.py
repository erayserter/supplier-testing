from django.test import TestCase
from django.db.models import Q

from rest_framework import status

from supplier.models import SupplierApplication, AssociatedSupplierDealerships
from supplier.initial_data import CREATE_APPLICATION_DATA, STATUS_DATA, UPDATE_DATA
from supplier.helpers import bad_request, request_with_data


AMOUNT_BOUNDARY = 9999


class CreateSupplierApplicationTests(TestCase):
    def setUp(self):
        self.data = CREATE_APPLICATION_DATA.copy()
        self.url = "https://dev.bumper.co.uk/core/api/supplier/application/v1/"

    def test_valid_data(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('message'), "Application created successfully")
        self.assertIsNotNone(data.get('data').get('token'))
        self.assertIsNotNone(data.get('data').get('redirect_url'))

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self, "API Key provided is Invalid", post=True)

    def test_invalid_signature(self):
        self.data['signature'] = '123'
        bad_request(self, "Signature provided is Invalid", post=True)

    def test_amount_gt_boundary(self):
        self.data['amount'] = f"{AMOUNT_BOUNDARY + 1}.00"
        self.data['signature'] = "488d309ab3dc22d507571920b758f42cec8ad99aa3c4c5e3e63a159a83b7cb1b"
        bad_request(self, "Amount provided is Invalid", post=True)

    def test_invalid_currency(self):
        self.data['currency'] = 'TL'
        self.data['signature'] = '3dadec9011b16d1fe4f1cccea9ab9a9f49aa0e41bda1ae4ca9dec8b95abfcabf'
        bad_request(self, "Currency provided is Invalid", post=True)

    def test_empty_product_description(self):
        self.data['product_description'] = []
        bad_request(self, "Product Description provided is Invalid", post=True)

    def test_invalid_email(self):
        self.data['email'] = 'invalid-email'
        self.data['signature'] = 'ad88d53e638a5cc3673c96487943df99b9dcdf5881756f7abd9cbbba6f3af45c'
        bad_request(self, "Email provided is Invalid", post=True)

    def test_invalid_product_id(self):
        self.data['product_id'] = '0'
        self.data['signature'] = 'fdbf117c629083952c0b3c9d8a4fc587f3a763852c9d0048e217616976706853'
        bad_request(self, "Product ID is Invalid", post=True)

    def test_invalid_mobile(self):
        self.data['mobile'] = ''
        self.data['signature'] = '8b8c04df32ff4417a4c1affcbae60c46d64cea28ed8ca8ebaec1a3667e5295b9'
        bad_request(self, 'mobile not provided correctly', post=True)


class StatusSupplierApplicationTests(TestCase):
    def setUp(self):
        self.data = STATUS_DATA.copy()
        self.url = "https://dev.bumper.co.uk/core/api/supplier/status/v1/"

    def test_valid_data(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))
        self.assertIsNotNone(data.get('data').get('token'))
        self.assertIsNotNone(data.get('data').get('customer_reference'))

    def test_valid_data_customer_reference(self):
        del self.data['token']
        self.data['bumper_reference'] = 154085
        self.data['signature'] = '49b5204dd21cad2eca7acdfbc46271b8deeb307cbd6e28dc085d0a1f4cf33847'
        self.test_valid_data()

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        bad_request(self, 'Signature provided is Invalid')

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self, 'API Key provided is Invalid')

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '3fbb67838aa67f9ab4f9264d9847e62add7d55d3f826f82fdbc7eaa273244949'
        bad_request(self, "Token provided is Invalid")


class UpdateApplicationTests(TestCase):
    def setUp(self):
        self.data = UPDATE_DATA.copy()
        self.url = "https://dev.bumper.co.uk/core/api/supplier/update/v1/"

    def test_valid_data(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('success'), True)
        self.assertEqual(data.get('message'), '')

    def test_valid_data_bumper_reference(self):
        self.data['bumper_reference'] = "112867"
        self.data['signature'] = '46e3b3e96b1cbd4bf8505af6d072eaebe9cc9bd1e51b330d9981c472e6b57a53'
        del self.data['token']
        self.test_valid_data()

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        bad_request(self, 'Signature provided is Invalid', post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self, 'API Key provided is Invalid', post=True)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = 'e967dbcfc9e49fc4879ad84f9302772862891ebda7a48a985c2019da559a5ffb'
        bad_request(self, "Token provided is invalid.", post=True)

    def test_invalid_amount(self):
        self.data['amount'] = AMOUNT_BOUNDARY + 1
        self.data['signature'] = 'faf60089cd887fbf345907b3ca677be3a0fa64f38588f7ec5ba1f090df21b88e'
        bad_request(self, "Amount provided is Invalid", post=True)
