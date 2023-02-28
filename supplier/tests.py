from django.test import TestCase

from rest_framework import status

import requests

AMOUNT_BOUNDARY = 9999


class CreateSupplierApplicationTests(TestCase):
    def setUp(self):
        self.data = {
            "amount": "300.00",
            "api_key": "8SY7cxabh5GRLr8GHbrGvsR9",
            "success_url": "http://www.supplier.com/success/",
            "failure_url": "http://www.supplier.com/failure/",
            "currency": "GBP",
            "order_reference": "26352",
            "signature": "82c1c78b4c7e776de2d30dd888298c8812757aa4265f47258a9146e56ea1858c",  # TODO: signature i al
            "first_name": "Rejecttest",
            "last_name": "Rejecttest",
            "product_description": [
                {
                    "item": "Pirelli Cinturato P7 Tyre",
                    "quantity": "2",
                    "price": "150.00"
                },
                {
                    "item": "Pirelli Cinturato P8 Tyre",
                    "quantity": "1",
                    "price": "150.00"
                }
            ],
            "email": "erayserter@gmail.com",
            "product_id": "7",
            "mobile": "0778879989",
            "vehicle_reg": "yg18kub",
            "flat_number": "23",
            "building_name": "ABC Building",
            "building_number": "39",
            "street": "DEF way",
            "town": "Southampton",
            "county": "Hampshire",
            "postcode": "SO14 3AB",
            "country": "UK"
        }

    # ------------------- TESTS -------------------

    def test_valid_data(self):
        response = self.post_data()
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('message'), "Application created successfully")
        self.assertIsNotNone(data.get('data').get('token'))
        self.assertIsNotNone(data.get('data').get('redirect_url'))

    def test_invalid_api_key(self):
        self.bad_request('api_key', '123', "API Key provided is Invalid")

    def test_invalid_signature(self):
        self.bad_request('signature', '123', "Signature provided is Invalid")

    def test_amount_gt_boundary(self):
        self.bad_request('amount', f"{AMOUNT_BOUNDARY + 1}.00", "Amount provided is Invalid")

    def test_invalid_currency(self):
        self.bad_request('currency', "TL", "Currency provided is Invalid")

    def test_empty_product_description(self):
        self.bad_request('product_description', [], "Product Description provided is Invalid")

    # ------------------- TEST HELPERS -------------------

    def bad_request(self, field, replacement, message):
        self.data[field] = replacement

        response = self.post_data()
        response_data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response_data.get('success'))
        self.assertEqual(response_data.get("message"), message)

    def post_data(self):
        # TODO: this will be implemented with self.client.post.
        return requests.post("https://dev.bumper.co.uk/core/api/supplier/application/v1/", json=self.data)
