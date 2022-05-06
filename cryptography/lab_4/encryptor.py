from typing import Union

from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class Encryptor:
    def __init__(self, private_key: bytes, bc_mode: str,
                 do_random_iv: bool = True):
        self.bc_mode = bc_mode
        self.aes = None
        self.iv = bytes(16)
        self.do_random_iv = do_random_iv
        self.private_key = private_key
        if self.bc_mode == "CBC":
            if self.do_random_iv is False:
                self.aes = AES.new(self.private_key, AES.MODE_CBC, iv=self.iv)
            else:
                self.aes = AES.new(self.private_key, AES.MODE_CBC)
        if self.bc_mode == "GCM":
            self.aes = AES.new(self.private_key, AES.MODE_GCM)

    def _create_encryptor(self):
        if self.bc_mode == "CBC":
            if self.do_random_iv is False:
                # incrementing iv
                iv_int = int.from_bytes(self.iv, byteorder='big')
                iv_int += 1
                iv_bytes = int.to_bytes(iv_int, byteorder='big', length=16)
                self.iv = iv_bytes

                # creating new encryptor
                self.aes = AES.new(self.private_key, AES.MODE_CBC, iv=iv_bytes)
            else:
                self.aes = AES.new(self.private_key, AES.MODE_CBC)
        if self.bc_mode == "GCM":
            self.aes = AES.new(self.private_key, AES.MODE_GCM)
            self.aes.update(b"header")

    def encrypt(self, message: Union[str, bytes]):
        self._create_encryptor()

        if self.bc_mode == "CBC":
            if isinstance(message, str):
                message = message.encode()

            if len(message) % 16 != 0:
                message = pad(message, AES.block_size)

            ciphertext = self.aes.encrypt(message)
            result = {'iv': self.aes.iv,
                      'ciphertext': ciphertext}
            return result

        if self.bc_mode == "GCM":
            ciphertext, tag = self.aes.encrypt_and_digest(message)
            result = {'nonce': self.aes.nonce,
                      'header': b"header",
                      'ciphertext': ciphertext,
                      'tag': tag}
            return result

    def decrypt(self, ciphertext):
        locals().update(ciphertext)
        if self.bc_mode == "CBC":
            iv = ciphertext['iv']
            ciphertext = ciphertext['ciphertext']
            decryptor = AES.new(self.private_key, AES.MODE_CBC, iv=iv)
            plaintext = unpad(decryptor.decrypt(ciphertext), AES.block_size)
            return plaintext
        if self.bc_mode == "GCM":
            try:
                nonce = ciphertext['nonce']
                header = ciphertext['header']
                ciphertext = ciphertext['ciphertext']
                tag = ciphertext['tag']
                decryptor = AES.new(self.private_key, AES.MODE_GCM,
                                    nonce=nonce)
                decryptor.update(header)
                plaintext = decryptor.decrypt_and_verify(ciphertext=ciphertext,
                                                         received_mac_tag=tag)
            except (ValueError, KeyError):
                print("Incorrect decryption")
