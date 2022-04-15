import random

from Crypto.Cipher import AES


class Initiator:
    def __init__(self, n: int):
        self.n = n
        self.challenges = {}
        self.weak_key_length = 2 ** n - 1
        self.id_bytes = b''
        self.key_bytes = b''

    def put_challenges(self, challenges: dict):
        self.challenges = challenges

    def solve_merkel_puzzle(self):
        challenge_id = random.randint(0, len(self.challenges))
        challenge = self.challenges[challenge_id]
        ciphertext, tag = challenge['ciphertext'], challenge['tag']
        self.brute_force(ciphertext, tag)

    def brute_force(self, ciphertext, tag):
        for weak_key in range(self.weak_key_length):
            weak_key_bytes = weak_key.to_bytes(32, 'big')
            aes = AES.new(weak_key_bytes, AES.MODE_GCM, nonce=bytes(16))  # otherwise nonce is generated automatically
            message = aes.decrypt(ciphertext)
            try:
                aes.verify(tag)
                id_bytes = message[:32]
                key_bytes = message[32:]
                self.id_bytes, self.key_bytes = id_bytes, key_bytes
            except ValueError:
                pass

    def get_challenge_id(self):
        return self.id_bytes
