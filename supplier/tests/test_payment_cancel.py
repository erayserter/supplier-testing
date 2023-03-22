from supplier.tests.custom_test_case import CustomTestCase

from rest_framework import status

from supplier.tests.helpers import get_bad_request, request_with_data


class PaymentCancelApplicationTest(CustomTestCase):
    data_file = 'payment_cancel_data.json'
    url = "https://dev.bumper.co.uk/core/api/supplier/payment-cancel/v1/"
    post = True

    def test_valid(self):
        response = request_with_data(self, self.post)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        print(f"response message: {data.get('message')}")
        self.assertEqual(True, data.get('success'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_cancelled(self):
        self.data['token'] = '5799a418e9f142f5819af3bd30972dad'
        self.data['signature'] = 'c6c26e0787e735c7c1466004291e781fdd1bf8d0e44407ed31a31e792e178ae8'
        get_bad_request(self, self.post)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '1fe8bac276f93c94639b467841a54b5b6d89a086a9dd5796f27b683c1f7f69a3'
        get_bad_request(self, self.post)
