from supplier.tests.custom_test_case import CustomTestCase

from rest_framework import status

from supplier.tests.helpers import get_bad_request, request_with_data


class PreapprovalStatusTest(CustomTestCase):
    data_file = 'preapproval_status_data.json'
    url = "https://dev.bumper.co.uk/core/api/supplier/preapprovalstatus/v1/"
    post = False

    def test_valid_data(self):
        response = request_with_data(self, self.post)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(True, data.get('success'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(data.get('data'))
        self.assertEquals('eraytesttoken', data.get('data').get('token'))

    def test_without_token(self):
        self.data.pop('preapproval_token')
        response = request_with_data(self, self.post)

        print(f"response message: {response.json().get('message')}")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_invalid_token(self):
        self.data['preapproval_token'] = '123'
        get_bad_request(self, self.post)
