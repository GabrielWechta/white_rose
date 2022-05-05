from typing import Union

from Cryptodome.Cipher import AES


class Encryptor:
    def __init__(self, private_key: bytes, bc_mode: str):
        self.aes = None
        self.iv = bytes(16)
        self.private_key = private_key
        if bc_mode == "CBC":
            self.aes = AES.new(self.private_key, AES.MODE_CBC, iv=self.iv)
        if bc_mode == "GCM":
            self.aes = AES.new(private_key, AES.MODE_GCM, nonce=bytes(16))

    def _create_encryptor(self):
        # incrementing iv
        iv_int = int.from_bytes(self.iv, byteorder='big')
        iv_int += 1
        iv_bytes = int.to_bytes(iv_int, byteorder='big', length=16)
        self.iv = iv_bytes

        # creating new encryptor
        self.aes = AES.new(self.private_key, AES.MODE_CBC, iv=iv_bytes)

    def encrypt(self, message: Union[str, bytes]):
        self._create_encryptor()

        if isinstance(message, str):
            message = message.encode()

        # print(f"{message=}")
        # padded = pad(message, AES.block_size)
        # print(f"{padded=}")
        ciphertext = self.aes.encrypt(message)
        result = {'iv': self.aes.iv,
                  'ciphertext': ciphertext}
        # print(result)
        return result
