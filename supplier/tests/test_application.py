from django.test import TestCase

from rest_framework import status

from supplier.helpers import get_bad_request, request_with_data

import json


class ApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/application_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/application/v1/"

    def test_valid_data(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        print(f"response message: {data.get('message')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data').get('token'))
        self.assertIsNotNone(data.get('data').get('redirect_url'))

    def test_surname_not_matched(self):
        self.data['first_name'] = 'surnamenotmatchedtest'
        self.data['last_name'] = 'surnamenotmatchedtest'
        self.data['signature'] = '2fdd452e3bde1e5594fa64b5b888a4afd7402858fe776ed01d6d46d7c834bbcd'
        self.test_valid_data()

    def test_surname_matched(self):
        self.data['first_name'] = 'surnamematchedtest'
        self.data['last_name'] = 'surnamematchedtest'
        self.data['signature'] = '6612059734d642bfadab75cc627230cb8eb95288744ae17eda7e4d849c132048'
        self.test_valid_data()

    def test_address_not_matched(self):
        self.data['first_name'] = 'addressnotmatchedtest'
        self.data['last_name'] = 'addressnotmatchedtest'
        self.data['signature'] = 'f85f2d3cd20d2eebdf89da905b22cd261c16a87a7446a7a109a0816b2117049f'
        self.test_valid_data()

    def test_counter_offer(self):
        self.data['first_name'] = 'counteroffertest'
        self.data['last_name'] = 'counteroffertest'
        self.data['signature'] = '207109a750f367aa150175a03e8941be4f4ab6ebde9ce495c53d2d265b7bfe62'
        self.test_valid_data()

    def test_valid_data_with_preapproval_link(self):
        del self.data['amount']
        self.data['preapproval_link'] = True
        self.data['signature'] = '232e3c01c48e57849aab8448d5c5c828adeed9c29cc0b035a9f9320829547e46'
        self.test_valid_data()

    def test_with_preapproval_and_amount(self):
        self.data['preapproval_link'] = True
        self.data['signature'] = '895aea5f8fdf2c37be30778f8c8ce4f477057ad2f5ad5c223e35e30dc92f633a'
        get_bad_request(self, post=True)

    def test_valid_data_without_preapproval_link(self):
        self.data['preapproval_link'] = False
        self.data['signature'] = '7f3b4541362566f3a986fcf2f6059115dabd447fdbe5cbb2f640484514238e59'
        self.test_valid_data()

    def test_without_api_key(self):
        del self.data['api_key']
        get_bad_request(self, post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        get_bad_request(self, post=True)

    def test_without_signature(self):
        del self.data['signature']
        get_bad_request(self, post=True)

    def test_invalid_signature(self):
        self.data['signature'] = '123'
        get_bad_request(self, post=True)

    def test_amount_gt_boundary(self):
        max_amount = 10000
        self.data['amount'] = max_amount + 1
        self.data['signature'] = "8e26f7e33d1f5a73c97ec608cc2d07d7d9aeace03debba45bc59a3293c681905"
        get_bad_request(self, post=True)

    def test_amount_lt_boundary(self):
        min_amount = 1
        self.data['amount'] = min_amount - 1
        self.data['signature'] = "fffc54114f79ceb10fa4cc690895426aa789add451659f1219ef9a90f99e01cc"
        get_bad_request(self, post=True)

    def test_without_currency(self):
        del self.data['currency']
        self.data['signature'] = 'c2bcf86448b1a99c3503387adff05d0f50889d7aae80219b5aca7bc85d970194'
        get_bad_request(self, post=True)

    def test_invalid_currency(self):
        self.data['currency'] = 'TL'
        self.data['signature'] = '4c5863ddd65ea334edb47cae138a6d103469e8c8216c9770b0bcd5a43386a409'
        get_bad_request(self, post=True)

    def test_empty_product_description(self):
        self.data['product_description'] = []
        get_bad_request(self, post=True)

    def test_without_item_product_description(self):
        self.data['product_description'] = [{
            "quantity": "2",
            "price": "150.00"
        }]
        get_bad_request(self, post=True)

    def test_without_quantity_product_description(self):
        self.data['product_description'] = [{
            "item": "Pirelli Cinturato P7 Tyre",
            "price": "150.00"
        }]
        get_bad_request(self, post=True)

    def test_without_price_product_description(self):
        self.data['product_description'] = [{
            "item": "Pirelli Cinturato P7 Tyre",
            "quantity": "2",
        }]
        get_bad_request(self, post=True)

    def test_invalid_item_product_description(self):
        self.data['product_description'] = [{
            "item": "invalid product item name",
            "quantity": "2",
            "price": "150.00"
        }]
        get_bad_request(self, post=True)

    def test_national_id_number_len_gt_boundary(self):
        self.data['national_id_number'] = '0123456789101112'  # TODO: length of the id number > 15
        self.data['signature'] = 'abda2419e2ab28009322d9d497cea506ee8a6274d2a577a9cf692d612fc4d21c'
        get_bad_request(self, post=True)

    def test_national_id_number(self):
        self.data['national_id_number'] = '123456789101112'
        self.data['signature'] = '444bce03427b5a524cc2fecf4d5d86c906e8106eedf9c666358c7b7737fe8afe'
        self.test_valid_data()

    def test_dni_len_gt_boundary(self):
        self.data['dni'] = '0123456789101112'
        self.data['signature'] = 'fd2515f36b1550ef1d0c054741fde5dd79b5bd6a7e69f6e90e8844b7d40d13af'
        get_bad_request(self, post=True)

    def test_dni(self):
        self.data['dni'] = '123456789101112'
        self.data['signature'] = 'c13d68a240f3ea8723a2fe83b7a9086573b7976f2f12245d49d25f22ba4b9475'
        self.test_valid_data()

    def test_send_email(self):
        self.data['send_email'] = True
        self.data['signature'] = '6fb32cc820274f8d6491b0c3d74ef09e195688ad5555ea896c5c8557156edc72'
        self.test_valid_data()

    def test_send_sms(self):
        self.data['send_sms'] = True
        self.data['signature'] = '4243783ed393d931342bacc6cea2de86e0daba41d9963260464e7e7966593a7a'
        self.test_valid_data()

    def test_send_email_and_sms(self):
        self.data['send_email'] = True
        self.data['send_sms'] = True
        self.data['signature'] = '0f44188aaff0c1df482e1b885c6cd19f7c2ea13980044a40646dd397eda50899'
        self.test_valid_data()

    def test_invalid_email(self):
        self.data['email'] = ''
        self.data['signature'] = '15556e887c8bf6c3ee775328f96f43d59d005939d93ef2a08a8d2fd1e787f749'
        get_bad_request(self, post=True)

    def test_invalid_product_id(self):
        self.data['product_id'] = '-1'
        self.data['signature'] = '9fa976670d75085b229318283d1982c49419daa07577e5a1d4c59c0ef56b7424'
        get_bad_request(self, post=True)

    def test_invalid_mobile(self):
        self.data['mobile'] = ''
        self.data['signature'] = '8b8c04df32ff4417a4c1affcbae60c46d64cea28ed8ca8ebaec1a3667e5295b9'
        get_bad_request(self, post=True)

    def test_without_order_reference(self):
        del self.data['order_reference']
        self.data['signature'] = 'e6d7f670229577def1911b0e186ce584c1d3a032f49d0b67682d32993cebcbdb'
        get_bad_request(self, post=True)
