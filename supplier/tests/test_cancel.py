from supplier.tests.custom_test_case import CustomTestCase

from rest_framework import status

from supplier.tests.helpers import get_bad_request, request_with_data


class CancelApplicationTest(CustomTestCase):
    data_file = 'cancel_data.json'
    url = "https://dev.bumper.co.uk/core/api/supplier/cancel/v1/"
    post = True

    def test_valid(self):
        response = request_with_data(self, self.post)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        print(f"response message: {data.get('message')}")
        self.assertEqual(True, data.get('success'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_pending(self):
        self.data['token'] = 'c07a4e3e8fa14280ae6'
        self.data['signature'] = '76c3611c3c82e9b63cb72ff09cbd32a3c8aa43d1f0b16e5f48e0ed4dc2112d43'
        self.test_valid()

    def test_inprogress(self):
        self.data['token'] = 'e0510724f67542acad5'
        self.data['signature'] = '664986aa9ca330b6f40023dde3efe159d02b89500507fc7b89f3db332722bf67'
        self.test_valid()

    def test_completed(self):
        self.data['token'] = '9f5f0294a3164e70a76'
        self.data['signature'] = '5155c1b3ac3b4cda4cd90a6478796e102bb56346cd6a9130a898e3abf7b8d35e'
        get_bad_request(self, self.post)

    def test_failed(self):
        self.data['token'] = '3e601439e4954f82a07'
        self.data['signature'] = '4b6a658f8311d0c9d3061b383521c139854a36802ee522a45edc803c80f691ef'
        get_bad_request(self, self.post)

    def test_cancelled(self):
        self.data['token'] = '0c15bd3ee2f742b296d'
        self.data['signature'] = 'd77abad67df2f6e6b1fba34c16a34739611a125c34859368df8c8424004700f7'
        get_bad_request(self, self.post)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '1fe8bac276f93c94639b467841a54b5b6d89a086a9dd5796f27b683c1f7f69a3'
        get_bad_request(self, self.post)
