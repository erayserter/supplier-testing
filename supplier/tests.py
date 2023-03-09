from django.test import TestCase

from rest_framework import status

from supplier.helpers import bad_request, request_with_data

import json


class CreateApplicationTest(TestCase):
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

    def test_valid_data_with_preapproval_link(self):
        del self.data['amount']
        self.data['preapproval_link'] = True
        self.data['signature'] = '232e3c01c48e57849aab8448d5c5c828adeed9c29cc0b035a9f9320829547e46'
        self.test_valid_data()

    def test_with_preapproval_and_amount(self):
        self.data['preapproval_link'] = True
        self.data['signature'] = '895aea5f8fdf2c37be30778f8c8ce4f477057ad2f5ad5c223e35e30dc92f633a'
        bad_request(self, post=True)

    def test_valid_data_without_preapproval_link(self):
        self.data['preapproval_link'] = False
        self.data['signature'] = '7f3b4541362566f3a986fcf2f6059115dabd447fdbe5cbb2f640484514238e59'
        self.test_valid_data()

    def test_without_api_key(self):
        del self.data['api_key']
        bad_request(self, post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self, post=True)

    def test_without_signature(self):
        del self.data['signature']
        bad_request(self, post=True)

    def test_invalid_signature(self):
        self.data['signature'] = '123'
        bad_request(self, post=True)

    def test_amount_gt_boundary(self):
        max_amount = 5000
        self.data['amount'] = max_amount + 1
        self.data['signature'] = "c049c2ebd4e97978da10588bd3be826470ea20b1d3ee993e2a36c5bff35e272d"
        bad_request(self, post=True)

    def test_amount_lt_boundary(self):
        min_amount = 1
        self.data['amount'] = min_amount - 1
        self.data['signature'] = "fffc54114f79ceb10fa4cc690895426aa789add451659f1219ef9a90f99e01cc"
        bad_request(self, post=True)

    def test_invalid_currency(self):
        self.data['currency'] = 'TL'
        self.data['signature'] = '4c5863ddd65ea334edb47cae138a6d103469e8c8216c9770b0bcd5a43386a409'
        bad_request(self, post=True)

    def test_empty_product_description(self):
        self.data['product_description'] = []
        bad_request(self, post=True)

    def test_without_item_product_description(self):
        self.data['product_description'] = [{
            "quantity": "2",
            "price": "150.00"
        }]
        bad_request(self, post=True)

    def test_without_quantity_product_description(self):
        self.data['product_description'] = [{
            "item": "Pirelli Cinturato P7 Tyre",
            "price": "150.00"
        }]
        bad_request(self, post=True)

    def test_without_price_product_description(self):
        self.data['product_description'] = [{
            "item": "Pirelli Cinturato P7 Tyre",
            "quantity": "2",
        }]
        bad_request(self, post=True)

    def test_invalid_item_product_description(self):
        self.data['product_description'] = [{
            "item": "invalid product item name",
            "quantity": "2",
            "price": "150.00"
        }]
        bad_request(self, post=True)

    def test_national_id_number_len_gt_boundary(self):
        self.data['national_id_number'] = '0123456789101112'  # TODO: length of the id number > 15
        self.data['signature'] = 'abda2419e2ab28009322d9d497cea506ee8a6274d2a577a9cf692d612fc4d21c'
        bad_request(self, post=True)

    def test_national_id_number(self):
        self.data['national_id_number'] = '123456789101112'
        self.data['signature'] = '444bce03427b5a524cc2fecf4d5d86c906e8106eedf9c666358c7b7737fe8afe'
        self.test_valid_data()

    def test_dni_len_gt_boundary(self):
        self.data['dni'] = '0123456789101112'
        self.data['signature'] = 'fd2515f36b1550ef1d0c054741fde5dd79b5bd6a7e69f6e90e8844b7d40d13af'
        bad_request(self, post=True)

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
        self.data['email'] = 'invalid-email'
        self.data['signature'] = '4cb76db042828a022b777ea334cd7839784f231ba9c0de5ddce8f413a41a4e2e'
        bad_request(self, post=True)

    def test_invalid_product_id(self):
        self.data['product_id'] = '0'
        self.data['signature'] = '76a6935f5b31fcf185be1aea2904bee6920cbb5331c465971121ee8962958ad1'
        bad_request(self, post=True)

    def test_invalid_mobile(self):
        self.data['mobile'] = ''
        self.data['signature'] = '8b8c04df32ff4417a4c1affcbae60c46d64cea28ed8ca8ebaec1a3667e5295b9'
        bad_request(self, post=True)

    def test_without_order_reference(self):
        del self.data['order_reference']
        self.data['signature'] = 'e6d7f670229577def1911b0e186ce584c1d3a032f49d0b67682d32993cebcbdb'
        bad_request(self, post=True)


class StatusApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/status_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/status/v1/"

    def test_valid_data_completed(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))
        self.assertIsNotNone(data.get('data').get('amount'))

    def test_valid_data_pending(self):
        self.data['token'] = '5d62808653ff416c881'
        self.data['signature'] = 'd53c9dffaba98a2108cef5b4019ae0829d7970812d189d7edacc3195a288fa53'

        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))
        self.assertEquals(data.get('data').get('status'), 'pending')
        self.assertIsNone(data.get('data').get('amount'))

    def test_valid_data_customer_reference(self):
        del self.data['token']
        self.data['bumper_reference'] = 156284
        self.data['signature'] = '5e7455b616d651ee07350b1688ec234ce16cc9597e72be84b9daa545b8853ef0'
        self.test_valid_data_completed()

    def test_invalid_customer_reference(self):
        del self.data['token']
        self.data['bumper_reference'] = 0
        self.data['signature'] = '3f8eb5fbea14ef21d823e7d40c2f41c8a1af37bc44a0e4c8e7bfbdffdf856013'
        bad_request(self)

    def test_without_signature(self):
        del self.data['signature']
        bad_request(self)

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        bad_request(self)

    def test_without_api_key(self):
        del self.data['api_key']
        bad_request(self)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '1fe8bac276f93c94639b467841a54b5b6d89a086a9dd5796f27b683c1f7f69a3'
        bad_request(self)


class PreapprovalStatusTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/preapproval_status_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/preapprovalstatus/v1/"

    def test_valid_data(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))
        self.assertEquals(data.get('data').get('token'), 'eraytesttoken')
        self.assertEquals(data.get('data').get('credit_limit'), 1613)

    def test_without_token(self):
        del self.data['preapproval_token']
        response = request_with_data(self)

        print(f"response message: {response.json().get('message')}")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_without_signature(self):
        del self.data['signature']
        bad_request(self)

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        bad_request(self)

    def test_without_api_key(self):
        del self.data['api_key']
        bad_request(self)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self)

    def test_invalid_token(self):
        self.data['preapproval_token'] = '123'
        bad_request(self)


class UpdateApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/update_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/update/v1/"

    def test_pending(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        print(f"response message: {data.get('message')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('success'), True)

    def test_pending_gt_boundary(self):
        self.data['amount'] = "5001"
        self.data['signature'] = "bc956431d43096ad2be4699723ab02721fcc2ff25ea496cfb0e367c74b69048f"
        bad_request(self, post=True)

    def test_pending_lt_boundary(self):
        self.data['amount'] = "0"
        self.data['signature'] = "2338f1c1f05bb8540012da69e7b0ffd5e4d72a0b95331c1d822a89f6af44ce5f"
        bad_request(self, post=True)

    def test_completed(self):
        self.data['token'] = '344b73ae65e44b2abbf'
        self.data['signature'] = 'c90403d938cdba9ebf8e05f1d676bd71bed53e7e490e28bee83f67803a0f2924'
        self.data['amount'] = 250
        bad_request(self, post=True)

    def test_completed_bumper_reference(self):
        self.data['bumper_reference'] = 156301
        self.data['signature'] = '29da8c4eceefb566ff42d7a588d06cc56878577a0a71b25de9a34776ccccca58'
        self.data['amount'] = 250
        del self.data['token']
        bad_request(self, post=True)

    def test_failed(self):
        self.data['token'] = '79d430f2ff164c6db44'
        self.data['signature'] = 'b61d027f8c060f9ae1c8a0e362828b42977892bd3d815a1ef6829242ad0a3206'
        bad_request(self, post=True)

    def test_invalid_bumper_reference(self):
        self.data['bumper_reference'] = "0"
        self.data['signature'] = 'd77d843d428cad0b6b50a91066e5ab25309c2cb6e7382b53c90d918fa1c804bd'
        del self.data['token']
        bad_request(self, post=True)

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        bad_request(self, post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self, post=True)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '28afeda6cff7b815e6d658881cfb16c26db085f120af20f91def0b987900e5e3'
        bad_request(self, post=True)
