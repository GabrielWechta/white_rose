import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Responder:
    def __init__(self, n: int):
        self.n = n
        self.secrets = {}
        self.generate_secrets_messages(n, n, 1)
        self.key_bytes = b''

    def generate_secrets_messages(self, weak_key_length, id_length, num_of_messages):
        weak_key_set = random.sample(range(2 ** weak_key_length - 1), num_of_messages)
        id_set = random.sample(range(2 ** id_length - 1), num_of_messages)
        for id, weak_key in zip(id_set, weak_key_set):
            key_bytes = get_random_bytes(32)
            weak_key_bytes = weak_key.to_bytes(32, 'big')
            id_bytes = id.to_bytes(32, 'big')
            message = id_bytes + key_bytes
            aes = AES.new(weak_key_bytes, AES.MODE_GCM, nonce=bytes(16))  # otherwise nonce is generated automatically
            ciphertext, tag = aes.encrypt_and_digest(message)
            self.secrets[id_bytes] = {'key': key_bytes, 'ciphertext': ciphertext, 'tag': tag}

    def get_challenges(self):
        challenges = {}
        for challenge_id, secret in enumerate(self.secrets.values()):
            challenges[challenge_id] = {'ciphertext': secret['ciphertext'], 'tag': secret['tag']}

        return challenges

    def put_challenge_id(self, id_bytes: bytes):
        self.key_bytes = self.secrets[id_bytes]['key']

    def __str__(self):
        return str(vars(self))
