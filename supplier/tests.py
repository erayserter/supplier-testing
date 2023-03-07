from django.test import TestCase
from django.db.models import Q

from rest_framework import status

from supplier.helpers import bad_request, request_with_data

import json


class CreateSupplierApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/application_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/application/v1/"

    def test_valid_data(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data').get('token'))
        self.assertIsNotNone(data.get('data').get('redirect_url'))

    def test_valid_data_with_preapproval_link(self):
        del self.data['amount']
        self.data['preapproval_link'] = 1
        self.data['signature'] = 'acd740069543c3d2501b3fc2e7e155f90b2f2745b1cb93a2cf059719861bee0e'
        self.test_valid_data()

    def test_valid_data_without_preapproval_link(self):
        self.data['preapproval_link'] = 0
        self.data['signature'] = '2cf31460cc223ffb5bb9c4e9ce347d1eae6a7a46ff8e0bf30b93e06d01e1e072'
        bad_request(self, post=True)

    def test_without_api_key(self):
        del self.data['api_key']
        bad_request(self, post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self, post=True)

    def test_without_signature(self):
        del self.data['signature']
        bad_request(self, post=True)

    def test_invalid_signature(self):
        self.data['signature'] = '123'
        bad_request(self, post=True)

    def test_amount_gt_boundary(self):
        MAX_AMOUNT = 5000
        self.data['amount'] = MAX_AMOUNT + 1
        self.data['signature'] = "3d2479a6ac181a8eb4d8dca019010d9f792d598975cacdf54a649eff9d73e3d2"
        bad_request(self, post=True)

    def test_amount_lt_boundary(self):
        MIN_AMOUNT = 1
        self.data['amount'] = MIN_AMOUNT - 1
        self.data['signature'] = "cdf0ea73558d322a85fb03910df8314e8d88ab3870cc0f4af6e7ae5cd81a3d32"
        bad_request(self, post=True)

    def test_invalid_currency(self):
        self.data['currency'] = 'TL'
        self.data['signature'] = '3dadec9011b16d1fe4f1cccea9ab9a9f49aa0e41bda1ae4ca9dec8b95abfcabf'
        bad_request(self, post=True)

    def test_empty_product_description(self):
        self.data['product_description'] = []
        bad_request(self, post=True)

    def test_without_item_product_description(self):
        self.data['product_description'] = [{
            "quantity": "2",
            "price": "150.00"
        }]
        bad_request(self, post=True)

    def test_without_quantity_product_description(self):
        self.data['product_description'] = [{
            "item": "Pirelli Cinturato P7 Tyre",
            "price": "150.00"
        }]
        bad_request(self, post=True)

    def test_without_price_product_description(self):
        self.data['product_description'] = [{
            "item": "Pirelli Cinturato P7 Tyre",
            "quantity": "2",
        }]
        bad_request(self, post=True)

    def test_invalid_item_product_description(self):
        self.data['product_description'] = [{
            "item": "invalid product item name",
            "quantity": "2",
            "price": "150.00"
        }]
        bad_request(self, post=True)

    def test_national_id_number_len_gt_boundary(self):
        self.data['national_id_number'] = '0123456789101112'  # TODO: length of the id number > 15
        self.data['signature'] = 'c69c429a412bfe75e7d6639d661ac5471d5592bdcf00478e7220f6fbf8b490eb'
        bad_request(self, post=True)

    def test_national_id_number(self):
        self.data['national_id_number'] = '123456789101112'
        self.data['signature'] = '3ceb26ee447dba2aac852f754fc800f19b070fb0b1f45dd97f44d44cf6ee1e6b'
        self.test_valid_data()

    def test_send_email(self):
        self.data['send_email'] = True
        self.data['signature'] = '9d46e8f08f0dd402704627443f350822aeba7adb64229e3d8070efeab3d013b6'
        self.test_valid_data()

    def test_send_sms(self):
        self.data['send_sms'] = True
        self.data['signature'] = '12e0436d9d884040041b56279e8a860e37588b824a1592624520305b0b67f129'
        self.test_valid_data()

    def test_send_email_and_sms(self):
        self.data['send_email'] = True
        self.data['send_sms'] = True
        self.data['signature'] = 'bf50484614ad3f4f1455bd08c2d8cd7cfd38d6016d63b1b54590d042bacb5caa'
        self.test_valid_data()

    def test_invalid_email(self):
        self.data['email'] = 'invalid-email'
        self.data['signature'] = 'ad88d53e638a5cc3673c96487943df99b9dcdf5881756f7abd9cbbba6f3af45c'
        bad_request(self, post=True)

    def test_invalid_product_id(self):
        self.data['product_id'] = '0'
        self.data['signature'] = '4d423521d19e9f15f454723c2fd2dc7f067da9d9dbcf5f977f4ee637fcacd593'
        bad_request(self, post=True)

    def test_invalid_mobile(self):
        self.data['mobile'] = ''
        self.data['signature'] = '8b8c04df32ff4417a4c1affcbae60c46d64cea28ed8ca8ebaec1a3667e5295b9'
        bad_request(self, post=True)


class StatusSupplierApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/status_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/status/v1/"

    def test_valid_data(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))

    def test_valid_data_customer_reference(self):
        del self.data['token']
        self.data['bumper_reference'] = 154085
        self.data['signature'] = '49b5204dd21cad2eca7acdfbc46271b8deeb307cbd6e28dc085d0a1f4cf33847'
        self.test_valid_data()

    def test_invalid_customer_reference(self):
        del self.data['token']
        self.data['bumper_reference'] = 0
        self.data['signature'] = 'a412adc993169bb31d40572a5a472d921da0aa9357e3d5dfee6852d65200c3c4'
        bad_request(self)

    def test_without_signature(self):
        del self.data['signature']
        bad_request(self)

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        bad_request(self)

    def test_without_api_key(self):
        del self.data['api_key']
        bad_request(self)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '3fbb67838aa67f9ab4f9264d9847e62add7d55d3f826f82fdbc7eaa273244949'
        bad_request(self)


class UpdateApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/update_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/update/v1/"

    def test_valid_data(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('success'), True)

    def test_valid_data_bumper_reference(self):
        self.data['bumper_reference'] = "112867"
        self.data['signature'] = '46e3b3e96b1cbd4bf8505af6d072eaebe9cc9bd1e51b330d9981c472e6b57a53'
        del self.data['token']
        self.test_valid_data()

    def test_invalid_bumper_reference(self):
        self.data['bumper_reference'] = "0"
        self.data['signature'] = '4f6a5b81fba4bf83e534aca06ae99356b2812c0cf3caea217b86459ae06c5581'
        del self.data['token']

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        bad_request(self, post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self, post=True)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = 'e967dbcfc9e49fc4879ad84f9302772862891ebda7a48a985c2019da559a5ffb'
        bad_request(self, post=True)

    def test_amount_gt_boundary(self):
        self.data['amount'] = "5001"
        self.data['signature'] = "24644e4c9efdf96dcb1a33713613f7db9802d78daffa59bd05d6ec6cd11faa2a"
        bad_request(self, post=True)

    def test_amount_lt_boundary(self):
        self.data['amount'] = "0"
        self.data['signature'] = "e8e88f4001702fc92607b6ff0273915c5591fbcab15b0552cf915cb3ab558f2b"
        bad_request(self, post=True)
