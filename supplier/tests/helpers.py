from rest_framework import status

import requests


def get_bad_request(test_case, post=None):
    response = request_with_data(test_case, post)

    print(f"response status code: {response.status_code}")
    print(f"response data: {response.json()}")

    # TODO: this will be response.data after request will be implemented with Client class.
    test_case.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


def request_with_data(test_case, post=None):
    # TODO: this will be implemented with self.client.get and post.
    if post:
        return requests.post(test_case.url, json=test_case.data)

    return requests.get(test_case.url, params=test_case.data)
