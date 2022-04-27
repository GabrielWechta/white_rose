import random
import time

from Crypto.Cipher import AES


class Initiator:
    def __init__(self, n: int):
        self.n = n
        self.challenges = {}
        self.max_weak_key = 2 ** self.n - 1
        self.id_bytes = b''
        self.key_bytes = b''

    def set_challenges(self, challenges: dict):
        self.challenges = challenges

    def solve_merkel_puzzle(self):
        # take random challenge from challenge set
        challenge_id = random.randint(0, len(self.challenges) - 1)
        challenge = self.challenges[challenge_id]
        # retrieve ciphertext and tag
        ciphertext, tag = challenge['ciphertext'], challenge['tag']
        # start brute forcing key
        self.brute_force(ciphertext, tag)

    def brute_force(self, ciphertext, tag):
        start = time.time()
        counter = 0
        for weak_key in range(self.max_weak_key):
            weak_key_bytes = weak_key.to_bytes(32, 'big')
            # putting the same nonce as Responder
            aes = AES.new(weak_key_bytes, AES.MODE_GCM, nonce=bytes(16))
            plaintext = aes.decrypt(ciphertext)
            try:
                aes.verify(tag)
                key_id_bytes = plaintext[:32]
                key_bytes = plaintext[32:]
                self.id_bytes, self.key_bytes = key_id_bytes, key_bytes
                print(
                    f"It took {counter} tries and {time.time() - start}s to guess weak_key.")
                return
            except ValueError:
                counter += 1

    def get_key_id(self):
        return self.id_bytes
