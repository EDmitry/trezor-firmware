from unittest import mock

import pytest
import shamir_mnemonic as shamir

from trezorlib import device, messages as proto
from trezorlib.messages import BackupType, ButtonRequestType as B

from .common import TrezorTest, generate_entropy

EXTERNAL_ENTROPY = b"zlutoucky kun upel divoke ody" * 2


@pytest.mark.skip_t1
class TestMsgResetDeviceT2(TrezorTest):
    # TODO: test with different options
    @pytest.mark.setup_client(uninitialized=True)
    def test_reset_device_supershamir(self, client):
        strength = 128
        member_threshold = 3
        all_mnemonics = []

        def input_flow():
            # Confirm Reset
            btn_code = yield
            assert btn_code == B.ResetDevice
            client.debug.press_yes()

            # Backup your seed
            btn_code = yield
            assert btn_code == B.ResetDevice
            client.debug.press_yes()

            # Confirm warning
            btn_code = yield
            assert btn_code == B.ResetDevice
            client.debug.press_yes()

            # shares info
            btn_code = yield
            assert btn_code == B.ResetDevice
            client.debug.press_yes()

            # Set & Confirm number of groups
            btn_code = yield
            assert btn_code == B.ResetDevice
            client.debug.press_yes()

            # threshold info
            btn_code = yield
            assert btn_code == B.ResetDevice
            client.debug.press_yes()

            # Set & confirm group threshold value
            btn_code = yield
            assert btn_code == B.ResetDevice
            client.debug.press_yes()

            for _ in range(5):
                # Set & Confirm number of share
                btn_code = yield
                assert btn_code == B.ResetDevice
                client.debug.press_yes()

                # Set & confirm share threshold value
                btn_code = yield
                assert btn_code == B.ResetDevice
                client.debug.press_yes()

            # Confirm show seeds
            btn_code = yield
            assert btn_code == B.ResetDevice
            client.debug.press_yes()

            # show & confirm shares for all groups
            for g in range(5):
                for h in range(5):
                    words = []
                    btn_code = yield
                    assert btn_code == B.ResetDevice

                    # mnemonic phrases
                    # 20 word over 6 pages for strength 128, 33 words over 9 pages for strength 256
                    for i in range(6):
                        words.extend(client.debug.read_reset_word().split())
                        if i < 5:
                            client.debug.swipe_down()
                        else:
                            # last page is confirmation
                            client.debug.press_yes()

                    # check share
                    for _ in range(3):
                        index = client.debug.read_reset_word_pos()
                        client.debug.input(words[index])

                    all_mnemonics.extend([" ".join(words)])

                    # Confirm continue to next share
                    btn_code = yield
                    assert btn_code == B.Success
                    client.debug.press_yes()

            # safety warning
            btn_code = yield
            assert btn_code == B.Success
            client.debug.press_yes()

        os_urandom = mock.Mock(return_value=EXTERNAL_ENTROPY)
        with mock.patch("os.urandom", os_urandom), client:
            client.set_expected_responses(
                [
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.EntropyRequest(),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(
                        code=B.ResetDevice
                    ),  # group #1 shares& thresholds
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(
                        code=B.ResetDevice
                    ),  # group #2 shares& thresholds
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(
                        code=B.ResetDevice
                    ),  # group #3 shares& thresholds
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(
                        code=B.ResetDevice
                    ),  # group #4 shares& thresholds
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(
                        code=B.ResetDevice
                    ),  # group #5 shares& thresholds
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.ResetDevice),  # show seeds
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),
                    proto.ButtonRequest(code=B.ResetDevice),
                    proto.ButtonRequest(code=B.Success),  # show seeds ends here
                    proto.ButtonRequest(code=B.Success),
                    proto.Success(),
                    proto.Features(),
                ]
            )
            client.set_input_flow(input_flow)

            # No PIN, no passphrase, don't display random
            device.reset(
                client,
                display_random=False,
                strength=strength,
                passphrase_protection=False,
                pin_protection=False,
                label="test",
                language="english",
                backup_type=BackupType.Slip39_Advanced,
            )

        # generate secret locally
        internal_entropy = client.debug.state().reset_entropy
        secret = generate_entropy(strength, internal_entropy, EXTERNAL_ENTROPY)

        # validate that all combinations will result in the correct master secret
        validate_mnemonics(all_mnemonics, member_threshold, secret)

        # Check if device is properly initialized
        assert client.features.initialized is True
        assert client.features.needs_backup is False
        assert client.features.pin_protection is False
        assert client.features.passphrase_protection is False
        assert client.features.backup_type is BackupType.Slip39_Advanced


def validate_mnemonics(mnemonics, threshold, expected_ems):
    # 3of5 shares 3of5 groups
    # TODO: test all possible group+share combinations?
    test_combination = mnemonics[0:3] + mnemonics[5:8] + mnemonics[10:13]
    ms = shamir.combine_mnemonics(test_combination)
    identifier, iteration_exponent, _, _, _ = shamir._decode_mnemonics(test_combination)
    ems = shamir._encrypt(ms, b"", iteration_exponent, identifier)
    assert ems == expected_ems