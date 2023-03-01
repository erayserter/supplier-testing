from django.test import TestCase
from django.db.models import Q

from rest_framework import status

from supplier.models import SupplierApplication, AssociatedSupplierDealerships
from supplier.initial_data import CREATE_APPLICATION_DATA, STATUS_DATA
from supplier.helpers import bad_request, request_with_data

AMOUNT_BOUNDARY = 9999


class CreateSupplierApplicationTests(TestCase):
    def setUp(self):
        self.data = CREATE_APPLICATION_DATA.copy()
        self.url = "https://dev.bumper.co.uk/core/api/supplier/application/v1/"

    def test_valid_data(self):
        response = request_with_data(self, "https://dev.bumper.co.uk/core/api/supplier/application/v1/", post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('message'), "Application created successfully")
        self.assertIsNotNone(data.get('data').get('token'))
        self.assertIsNotNone(data.get('data').get('redirect_url'))

    def test_invalid_api_key(self):
        bad_request(self, 'api_key', '123', "API Key provided is Invalid", post=True)

    def test_invalid_signature(self):
        bad_request(self, 'signature', '123', "Signature provided is Invalid", post=True)

    def test_amount_gt_boundary(self):
        bad_request(self, 'amount', f"{AMOUNT_BOUNDARY + 1}.00", "Amount provided is Invalid", post=True)

    def test_invalid_currency(self):
        bad_request(self, 'currency', "TL", "Currency provided is Invalid", post=True)

    def test_empty_product_description(self):
        bad_request(self, 'product_description', [], "Product Description provided is Invalid", post=True)

    def test_invalid_email(self):
        bad_request(self, 'email', 'invalidemail', "Email provided is Invalid", post=True)

    def test_invalid_product_id(self):
        bad_request(self, 'product_id', '0', "Product ID is Invalid", post=True)

    def test_invalid_mobile(self):
        bad_request(self, 'mobile', '', 'mobile not provided correctly', post=True)


class StatusSupplierApplicationTests(TestCase):
    def setUp(self):
        self.data = STATUS_DATA.copy()
        self.url = "https://dev.bumper.co.uk/core/api/supplier/status/v1/"

    def test_valid_data(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)

        try:
            token = data['data']['token']
            customer_reference = data['data']['customer_reference']
        except Exception as e:
            self.fail("Malformed response")

        try:
            dealership = AssociatedSupplierDealerships.objects.get(apikey=self.data.get('api_key')).dealership
        except Exception as e:
            self.fail("API Key is not associated with a supplier and dealership")

        try:
            supplier_app = SupplierApplication.objects.get(
                Q(
                    token=token,
                    token__isnull=False
                ) | Q(
                    application__id=customer_reference,
                    application__isnull=False,
                    application__dealership=dealership
                )
            )
        except Exception as e:
            self.fail("Supplier Application Not Found")

    def test_invalid_signature(self):
        bad_request(
            self,
            'signature',
            'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc',
            'Signature provided is Invalid'
        )

    def test_invalid_api_key(self):
        bad_request(self, 'api_key', '123', 'API Key provided is Invalid')
