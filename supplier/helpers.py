from rest_framework import status

import requests


def bad_request(test_case, field, replacement, message, post=False):
    test_case.data[field] = replacement

    response = request_with_data(test_case, post)
    response_data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

    test_case.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    test_case.assertFalse(response_data.get('success'))
    test_case.assertEqual(response_data.get("message"), message)


def request_with_data(test_case, post=False):
    # TODO: this will be implemented with self.client.get and post.
    if post:
        return requests.post(test_case.url, json=test_case.data)

    return requests.get(test_case.url, params=test_case.data)
