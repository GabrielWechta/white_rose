import random

import pytest

from encryptor import Encryptor


@pytest.mark.parametrize("plaintext, expected_ciphertext",
                         [
                             ("message",
                              {
                                  'ciphertext': b'?\x92\xe5:\x1d\x93UB\xf6(\x08s\xab\x8e\x87\xdf',
                                  'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
                              }
                              ),
                             ("whatever",
                              {
                                  'ciphertext': b'_\xe1\xb0\xb5\x13#\xef\x8b\xd2\xa2\rS\xd4\xef\xdf\xd2',
                                  'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
                              }
                              ),
                             ("it may not be enough",
                              {
                                  'ciphertext': b'1\n\x1c\xef\xdcP\x88\xd9\x1f\x9b\n\r\x1cZ\xcb\xcf,\tF\x06'
                                                b'\xb7o\x00\xb9\x96\xe3\xe3 \xb5\xdeC\xf9',
                                  'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
                              }
                              )
                         ]
                         )
def test_encryption_CBC(plaintext, expected_ciphertext):
    private_key = bytes([i for i in range(32)])
    encryptor = Encryptor(private_key=private_key, bc_mode="CBC",
                          do_random_iv=False)
    ciphertext = encryptor.encrypt(plaintext)
    # print(ciphertext)

    assert ciphertext == expected_ciphertext


@pytest.mark.parametrize("ciphertext, expected_plaintext",
                         [
                             (
                                     {
                                         'ciphertext': b'?\x92\xe5:\x1d\x93UB\xf6(\x08s\xab\x8e\x87\xdf',
                                         'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
                                     },
                                     b"message",
                             ),
                             (
                                     {
                                         'ciphertext': b'_\xe1\xb0\xb5\x13#\xef\x8b\xd2\xa2\rS\xd4\xef\xdf\xd2',
                                         'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
                                     },
                                     b"whatever",
                             ),
                             (
                                     {
                                         'ciphertext': b'1\n\x1c\xef\xdcP\x88\xd9\x1f\x9b\n\r\x1cZ\xcb\xcf,\tF\x06'
                                                       b'\xb7o\x00\xb9\x96\xe3\xe3 \xb5\xdeC\xf9',
                                         'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
                                     }, b"it may not be enough",
                             )
                         ]
                         )
def test_decryption_CBC(ciphertext, expected_plaintext):
    private_key = bytes([i for i in range(32)])
    encryptor = Encryptor(private_key=private_key, bc_mode="CBC",
                          do_random_iv=False)
    plaintext = encryptor.decrypt(ciphertext)
    # print(plaintext)

    assert plaintext == expected_plaintext


@pytest.mark.parametrize("plaintext, expected_ciphertext",
                         [
                             (b"message",
                              {'ciphertext': b'\xfb\xd6\x88Q\xc2,j',
                               'header': b'header',
                               'nonce': b"\xeb\x18\xb5}\x94'\x9d\xfa)T\xf0\xc8[\xcb\xbdD",
                               'tag': b'&7R\xea\xb2\xa7\xd7\x05Tn-\x11\x87\t\xe6\x92'} != {
                                  'ciphertext': b'?\x92\xe5:\x1d\x93UB\xf6(\x08s\xab\x8e\x87\xdf',
                                  'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'}
                              ),
                             (b"whatever",
                              {'ciphertext': b'\xef~\x94\xe9Ce\xf6\xba',
                               'header': b'header',
                               'nonce': b'\r\xd1\xbf\xee\xa6G\xcd)v$\n\x1c7#\xb9\x18',
                               'tag': b'\x8b\xf8~\x8bk\xf9?x\x04\x99L`w\xe6y\xd0'} != {
                                  'ciphertext': b'_\xe1\xb0\xb5\x13#\xef\x8b\xd2\xa2\rS\xd4\xef\xdf\xd2',
                                  'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'}
                              ),
                             (b"it may not be enough",
                              {
                                  'ciphertext': b'\x928\xe9\x8f\x03\xd9C\x80n`\xf6\xa5\x9d\xd0poR\xc2\x85\\',
                                  'header': b'header',
                                  'nonce': b'_?\x94\x90\x8d\xf7.\xd4Q\xb7E_\xc2\xdf\x84\xa3',
                                  'tag': b'\x87o\x96\xee\xa9;\x8a\xf2\x96\xa7\xa8\x12y\xaf\x161'} != {
                                  'ciphertext': b'1\n\x1c\xef\xdcP\x88\xd9\x1f\x9b\n\r\x1cZ\xcb\xcf,\tF\x06'
                                                b'\xb7o\x00\xb9\x96\xe3\xe3 \xb5\xdeC\xf9',
                                  'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'}
                              )
                         ]
                         )
def test_encryption_GCM(plaintext, expected_ciphertext):
    private_key = bytes([i for i in range(32)])
    encryptor = Encryptor(private_key=private_key, bc_mode="GCM",
                          do_random_iv=False)
    ciphertext = encryptor.encrypt(plaintext)
    print(ciphertext)

    assert ciphertext != expected_ciphertext


@pytest.mark.parametrize("ciphertext, expected_plaintext",
                         [
                             (
                                     {
                                         'ciphertext': b'?\x92\xe5:\x1d\x93UB\xf6(\x08s\xab\x8e\x87\xdf',
                                         'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
                                     },
                                     b"message",
                             ),
                             (
                                     {
                                         'ciphertext': b'_\xe1\xb0\xb5\x13#\xef\x8b\xd2\xa2\rS\xd4\xef\xdf\xd2',
                                         'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
                                     },
                                     b"whatever",
                             ),
                             (
                                     {
                                         'ciphertext': b'1\n\x1c\xef\xdcP\x88\xd9\x1f\x9b\n\r\x1cZ\xcb\xcf,\tF\x06'
                                                       b'\xb7o\x00\xb9\x96\xe3\xe3 \xb5\xdeC\xf9',
                                         'iv': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
                                     }, b"it may not be enough",
                             )
                         ]
                         )
def test_decryption_GCM(ciphertext, expected_plaintext):
    private_key = bytes([i for i in range(32)])
    encryptor = Encryptor(private_key=private_key, bc_mode="GCM",
                          do_random_iv=False)
    plaintext = encryptor.decrypt(ciphertext)
    # print(plaintext)

    assert plaintext != expected_plaintext
