from rest_framework import status

import requests


def bad_request(test_case, post=None):
    response = request_with_data(test_case, post)
    print(f"response message: {response.json().get('message')}")
    # TODO: this will be response.data after request will be implemented with Client class.
    test_case.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


def request_with_data(test_case, post=None):
    # TODO: this will be implemented with self.client.get and post.
    if post:
        return requests.post(test_case.url, json=test_case.data)

    return requests.get(test_case.url, params=test_case.data)
