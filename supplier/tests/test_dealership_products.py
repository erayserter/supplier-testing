from supplier.tests.custom_test_case import CustomTestCase

from rest_framework import status

from supplier.tests.helpers import get_bad_request, request_with_data


class DealershipProductsTest(CustomTestCase):
    data_file = 'products_data.json'
    url = "https://dev.bumper.co.uk/core/api/supplier/products/v1/"
    post = False

    def test_valid_data(self):
        response = request_with_data(self, self.post)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data'))

    def test_without_amount(self):
        self.data.pop('amount')
        self.data['signature'] = 'a7a35e3a9434ad9b4b6617a331964472043fcad3ea3b06b207559b43fe1144a2'
        self.test_valid_data()
