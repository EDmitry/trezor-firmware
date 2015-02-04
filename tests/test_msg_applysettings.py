import time
import unittest
import common

from trezorlib import messages_pb2 as proto

class TestMsgApplysettings(common.TrezorTest):

    def test_apply_settings(self):
        self.setup_mnemonic_pin_passphrase()
        self.assertEqual(self.client.features.label, 'test')

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.PinMatrixRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(label='new label')

        self.assertEqual(self.client.features.label, 'new label')

    def test_invalid_language(self):
        self.setup_mnemonic_pin_passphrase()
        self.assertEqual(self.client.features.language, 'english')

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.PinMatrixRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(language='nonexistent')

        self.assertEqual(self.client.features.language, 'english')

    def test_apply_settings_passphrase(self):
        self.setup_mnemonic_pin_nopassphrase()

        self.assertEqual(self.client.features.passphrase_protection, False)

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.PinMatrixRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(use_passphrase=True)

        self.assertEqual(self.client.features.passphrase_protection, True)

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(use_passphrase=False)

        self.assertEqual(self.client.features.passphrase_protection, False)

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(use_passphrase=True)

        self.assertEqual(self.client.features.passphrase_protection, True)

    def test_apply_homescreen(self):
        self.setup_mnemonic_pin_passphrase()

        img = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00?\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\xff\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00?\xff\xff\xff\xff\xff\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x1f\xff\xff\xff\xff\xff\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\x1f\xff\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x01\xff\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x01\xe7\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x01\xe7\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x01\xe3\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x03\xc7\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x07\x87\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x07\x07\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x0f\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\xff\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\xf9\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xff\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xff\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f?\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        with self.client:
            self.client.set_expected_responses([proto.ButtonRequest(),
                                                proto.PinMatrixRequest(),
                                                proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(homescreen=img)

if __name__ == '__main__':
    unittest.main()
