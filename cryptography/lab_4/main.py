import argparse

import OpenSSL
from jks import jks

from encryptor import Encryptor


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Program for encrypting message and playing CPA game, "
                    "using AES-CBC and AES-GCM."
    )

    parser.add_argument(
        "--mode",
        dest="mode",
        type=str,
        choices=["enc_oracle", "challenge"],
        help="encryption oracle - on input consisting q messages: m_1, m_2, "
             "..., m_q it returns it ciphertexts. \n "
             "challenge - on input m_0, m_1 program picks independently, "
             "uniformly random bit b from {0, 1} and returns a ciphertext c_b "
             "of a message m_b."
    )

    parser.add_argument(
        "--bc_mode",
        dest="bc_mode",
        type=str,
        choices=["CBC", "GCM"],
        help="Block cipher mode of operation, from {CBC, GCM}",
    )

    parser.add_argument(
        "--keystore_path",
        dest="keystore_path",
        type=str,
        help="Path to the keystore file location.",
    )

    parser.add_argument(
        "--key_identifier",
        dest="key_identifier",
        type=str,
        help="Identifier for key in keystore file.",
    )

    parser.add_argument(
        "--keystore_password",
        dest="keystore_password",
        type=str,
        help="Password for keystore.",
    )

    return parser.parse_args()


def get_privkey_from_keystore(keystore_path: str, key_identifier: str,
                              keystore_password: str):
    keystore = jks.KeyStore.load(keystore_path, keystore_password)
    privkey_entry = keystore.private_keys[key_identifier]

    # if the key could not be decrypted using the store password,
    # decrypt with a custom password now
    if not privkey_entry.is_decrypted():
        privkey_entry.decrypt(keystore_password)

    privkey = privkey_entry.pkey
    privkey += bytes(1)
    print(f"{privkey=}")
    return privkey


def main():
    args = _parse_args()
    mode, bc_mode = args.mode, args.bc_mode
    keystore_path, key_identifier = args.keystore_path, args.key_identifier
    keystore_password = args.keystore_password

    privkey = get_privkey_from_keystore(keystore_path=keystore_path,
                                        key_identifier=key_identifier,
                                        keystore_password=keystore_password)

    encryptor = Encryptor(private_key=privkey, bc_mode=bc_mode)

    if mode == "enc_oracle":



if __name__ == "__main__":
    main()
