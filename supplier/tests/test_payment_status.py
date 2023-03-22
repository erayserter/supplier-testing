from supplier.tests.custom_test_case import CustomTestCase

from rest_framework import status

from supplier.tests.helpers import get_bad_request, request_with_data


class PaymentStatusApplicationTest(CustomTestCase):
    data_file = 'payment_status_data.json'
    url = "https://dev.bumper.co.uk/core/api/supplier/paymentstatus/v1/"
    post = False

    def test_valid_data(self):
        response = request_with_data(self, self.post)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(True, data.get('success'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(data.get('data'))

    def test_not_found(self):
        self.data['token'] = 'd4ecf522fe6b42ccb75937fed7e094f5'
        self.data['signature'] = '338cea4e4fb951350ef86ac13408d9e96bf22cb45016edc3e665e88ada0e93c2'

        response = request_with_data(self, self.post)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.
        self.assertEqual(data.get('success'), False)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '1fe8bac276f93c94639b467841a54b5b6d89a086a9dd5796f27b683c1f7f69a3'
        get_bad_request(self, self.post)
