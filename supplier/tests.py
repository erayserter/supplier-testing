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
        max_amount = 10000
        self.data['amount'] = max_amount + 1
        self.data['signature'] = "8e26f7e33d1f5a73c97ec608cc2d07d7d9aeace03debba45bc59a3293c681905"
        bad_request(self, post=True)

    def test_amount_lt_boundary(self):
        min_amount = 1
        self.data['amount'] = min_amount - 1
        self.data['signature'] = "fffc54114f79ceb10fa4cc690895426aa789add451659f1219ef9a90f99e01cc"
        bad_request(self, post=True)

    def test_without_currency(self):
        del self.data['currency']
        self.data['signature'] = 'c2bcf86448b1a99c3503387adff05d0f50889d7aae80219b5aca7bc85d970194'
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
        self.data['email'] = ''
        self.data['signature'] = '15556e887c8bf6c3ee775328f96f43d59d005939d93ef2a08a8d2fd1e787f749'
        bad_request(self, post=True)

    def test_invalid_product_id(self):
        self.data['product_id'] = '-1'
        self.data['signature'] = '9fa976670d75085b229318283d1982c49419daa07577e5a1d4c59c0ef56b7424'
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

    def test_completed(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))
        self.assertIsNotNone(data.get('data').get('amount'))

    def test_pending(self):
        self.data['token'] = '5d62808653ff416c881'
        self.data['signature'] = 'd53c9dffaba98a2108cef5b4019ae0829d7970812d189d7edacc3195a288fa53'

        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))
        self.assertEquals(data.get('data').get('status'), 'pending')
        self.assertIsNone(data.get('data').get('amount'))

    def test_cancelled(self):
        self.data['token'] = 'ae4e985f8a1c4c91b41'
        self.data['signature'] = 'e3cdc904142a0d6d01758dd35f5746e11d0d1f7ad51f44674d95bbd750777f28'

        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))

    def test_valid_data_customer_reference(self):
        del self.data['token']
        self.data['bumper_reference'] = 156284
        self.data['signature'] = '5e7455b616d651ee07350b1688ec234ce16cc9597e72be84b9daa545b8853ef0'
        self.test_completed()

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
        self.data['amount'] = 100001
        self.data['signature'] = "49521483ce984118a78dc30b399acaff62288d898d61ac69590f6d331fdc5224"
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


class CancelApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/cancel_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/cancel/v1/"

    def test_valid(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        print(f"response message: {data.get('message')}")
        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        bad_request(self, post=True)

    def test_failed(self):
        self.data['token'] = '3e601439e4954f82a07'
        self.data['signature'] = '4b6a658f8311d0c9d3061b383521c139854a36802ee522a45edc803c80f691ef'
        bad_request(self, post=True)

    def test_cancelled(self):
        self.data['token'] = '0c15bd3ee2f742b296d'
        self.data['signature'] = 'd77abad67df2f6e6b1fba34c16a34739611a125c34859368df8c8424004700f7'
        bad_request(self, post=True)

    def test_without_signature(self):
        del self.data['signature']
        bad_request(self, post=True)

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        bad_request(self, post=True)

    def test_without_api_key(self):
        del self.data['api_key']
        bad_request(self, post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self, post=True)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '1fe8bac276f93c94639b467841a54b5b6d89a086a9dd5796f27b683c1f7f69a3'
        bad_request(self, post=True)


class PaymentApplicationTest(TestCase):
    longString = "x" * 256

    def setUp(self):
        self.data = json.load(open('supplier/datas/payment_application_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/payment/v1/"

    def test_valid_data(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        print(f"response message: {data.get('message')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data').get('token'))
        self.assertIsNotNone(data.get('data').get('redirect_url'))

    def test_amount_gt_boundary(self):
        max_amount = 10000
        self.data['amount'] = max_amount + 1
        self.data['signature'] = "a7b679bfdab9ec10938d1f1ae18e33bb5b7edebd356a87cf32bfe2b92affe305"
        bad_request(self, post=True)

    def test_amount_lt_boundary(self):
        min_amount = 1
        self.data['amount'] = min_amount - 1
        self.data['signature'] = "5dc0ead2d701c169121371b97d93998d552e2862ff973a20d0d662f98ffcdb37"
        bad_request(self, post=True)

    def test_without_amount(self):
        del self.data['amount']
        self.data['signature'] = 'af4c878c871e5c759ed210c894241892e587ad5ddb087b05e0c5514f1c9af292'
        bad_request(self, post=True)

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

    def test_without_currency(self):
        del self.data['currency']
        self.data['signature'] = '951224e0a6372466d22fca5ce4734a10f625b7ca6b063bb61db8f2368b6a1462'
        bad_request(self, post=True)

    def test_invalid_currency(self):
        self.data['currency'] = 'TL'
        self.data['signature'] = 'b20179b74b7ed54bb8ab3025f8c3eb0862762f86abe7dcdd6c944ce0dcda17da'
        bad_request(self, post=True)

    def test_without_order_reference(self):
        del self.data['order_reference']
        self.data['signature'] = '4900e069a08c89cbd17a9b57448a9c25e0753aebab67521c3c649326cf3aa968'
        bad_request(self, post=True)

    def test_without_registration(self):
        del self.data['registration']
        self.data['signature'] = 'f984ece1fe9154b362b257be8dff4177347f81bc4b1a1c914a32a3b11712edb4'
        bad_request(self, post=True)

    def test_without_product_name(self):
        del self.data['product_name']
        self.data['signature'] = '5e99b28ebc1f9f08f733008886aa26d17450f045f20a5cf5fd884d07dac1abd7'
        bad_request(self, post=True)

    def test_invalid_product_name(self):
        self.data['product_name'] = ''
        self.data['signature'] = '3187d91cd7e2ffa836bd1f170bfb4cbdd85bd89e0e8359e9dfb35df3f48ae208'
        bad_request(self, post=True)

    def test_product_name_len_gt_boundary(self):
        self.data['product_name'] = self.longString
        self.data['signature'] = '9ca0c48b12b37363267628b61893ad4afc9b2933af5ae264d7bcaf8f3a8dab2a'
        bad_request(self, post=True)

    def test_order_reference_len_gt_boundary(self):
        self.data['order_reference'] = self.longString
        self.data['signature'] = '7654e30b151970d800b917bc855b0edccd132a4e9f725b3a35f9bfcfbdff08a4'
        bad_request(self, post=True)

    def test_success_url_len_gt_boundary(self):
        self.data['success_url'] = self.longString
        self.data['signature'] = '2c2df10239b35b4f42a024c322566329bc73e0371c7e53f72fc8a220a973f2a0'
        bad_request(self, post=True)

    def test_failure_url_len_gt_boundary(self):
        self.data['failure_url'] = self.longString
        self.data['signature'] = '4c20442ab297e10a9cb79458ab953daf819d7a42160f369dce75c3853f1ad13b'
        bad_request(self, post=True)

    def test_registration_len_gt_boundary(self):
        self.data['registration'] = "x" * 13
        self.data['signature'] = '822377bea1e860a87c4bcc736226d9e50254e0da2ff651c2c6344e7a1b814978'
        bad_request(self, post=True)


class PaymentStatusApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/payment_status_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/paymentstatus/v1/"

    def test_valid_data(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('data'))

    def test_not_found(self):
        self.data['token'] = 'd4ecf522fe6b42ccb75937fed7e094f5'
        self.data['signature'] = '338cea4e4fb951350ef86ac13408d9e96bf22cb45016edc3e665e88ada0e93c2'

        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.
        self.assertEqual(data.get('success'), False)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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


class PaymentCancelApplicationTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/payment_cancel_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/payment-cancel/v1/"

    def test_valid(self):
        response = request_with_data(self, post=True)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        print(f"response message: {data.get('message')}")
        self.assertEqual(data.get('success'), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancelled(self):
        self.data['token'] = '5799a418e9f142f5819af3bd30972dad'
        self.data['signature'] = 'c6c26e0787e735c7c1466004291e781fdd1bf8d0e44407ed31a31e792e178ae8'
        bad_request(self, post=True)

    def test_without_signature(self):
        del self.data['signature']
        bad_request(self, post=True)

    def test_invalid_signature(self):
        self.data['signature'] = 'e768335bf3f3f7f75a532745ac0cb6af0bd5294fa26627b1b565c77aa516cbfc'
        bad_request(self, post=True)

    def test_without_api_key(self):
        del self.data['api_key']
        bad_request(self, post=True)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self, post=True)

    def test_invalid_token(self):
        self.data['token'] = '123'
        self.data['signature'] = '1fe8bac276f93c94639b467841a54b5b6d89a086a9dd5796f27b683c1f7f69a3'
        bad_request(self, post=True)


class DealershipProductsTest(TestCase):
    def setUp(self):
        self.data = json.load(open('supplier/datas/products_data.json', 'r'))
        self.url = "https://dev.bumper.co.uk/core/api/supplier/products/v1/"

    def test_valid_data(self):
        response = request_with_data(self)
        data = response.json()  # TODO: this will be response.data after request will be implemented with Client class.

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data'))

    def test_without_api_key(self):
        del self.data['api_key']
        bad_request(self)

    def test_invalid_api_key(self):
        self.data['api_key'] = '123'
        bad_request(self)

    def test_without_signature(self):
        del self.data['signature']
        bad_request(self)

    def test_invalid_signature(self):
        self.data['signature'] = '123'
        bad_request(self)

    def test_amount_gt_boundary(self):
        max_amount = 5000
        self.data['amount'] = max_amount + 1
        self.data['signature'] = "6a6e62e0156d12f8e7e40c3311a5f3d91df929835259675a9d484abcb9e40d60"
        bad_request(self)

    def test_amount_lt_boundary(self):
        min_amount = 1
        self.data['amount'] = min_amount - 1
        self.data['signature'] = "cec93742c94c3ce571d726be52865d8ae38b07621604d8bad8fa4dcb048b7b66"
        bad_request(self)

    def test_without_amount(self):
        del self.data['amount']
        self.data['signature'] = 'a7a35e3a9434ad9b4b6617a331964472043fcad3ea3b06b207559b43fe1144a2'
        bad_request(self)
