from rest_framework import status

import requests


def bad_request(test_case, message, post=False):
    response = request_with_data(test_case, post)
    # TODO: this will be response.data after request will be implemented with Client class.
    response_data = response.json()

    test_case.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    test_case.assertFalse(response_data.get('success'))
    test_case.assertEqual(response_data.get("message"), message)


def request_with_data(test_case, post=False):
    # TODO: this will be implemented with self.client.get and post.
    if post:
        return requests.post(test_case.url, json=test_case.data)

    return requests.get(test_case.url, params=test_case.data)
