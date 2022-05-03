import json
from base64 import b64encode

from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad


class Encryptor:
    def __init__(self, private_key: bytes, bc_mode: str):
        self.aes = None
        if bc_mode == "CBC":
            self.aes = AES.new(private_key, AES.MODE_CBC, iv=bytes(16))
        if bc_mode == "GCM":
            self.aes = AES.new(private_key, AES.MODE_GCM, nonce=bytes(16))

    def _increment_iv(self):
        iv_int = int.from_bytes(self.aes.iv, byteorder='big')
        iv_int += 1
        iv_bytes = int.to_bytes(iv_int, byteorder='big', length=16)
        self.aes.iv = iv_bytes

    def encrypt(self, message: bytes):
        print(f"{message=}")
        padded = pad(message, AES.block_size)
        print(f"{padded=}")
        encrypted = self.aes.encrypt(padded)
        print(f"{encrypted=}")
        print(f"{self.aes.iv=}")
        iv = b64encode(self.aes.iv).decode('utf-8')
        ct = b64encode(encrypted).decode('utf-8')
        result = json.dumps({'iv': iv, 'ciphertext': ct})
        print(result)
        self._increment_iv()
        return encrypted
