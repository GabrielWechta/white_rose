import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Responder:
    def __init__(self, n: int, num_of_challenges: int = None):
        self.n = n
        self.secrets = {}
        self.max_weak_key = 2 ** self.n - 1
        self.max_key_id = 2 ** 256 - 1
        if num_of_challenges is None:
            self.num_of_challenges = 2 ** self.n
        else:
            self.num_of_challenges = num_of_challenges
        self.__generate_secrets_messages(max_weak_key=self.max_weak_key,
                                         max_key_id=self.max_key_id,
                                         num_of_challenges=self.num_of_challenges)
        self.key_bytes = b''

    def __generate_secrets_messages(self, max_weak_key: int, max_key_id: int,
                                    num_of_challenges: int):
        # generate set of random weak_keys
        weak_key_set = random.sample(range(max_weak_key),
                                     num_of_challenges)
        # generate set of random weak_keys
        key_id_set = set()
        while len(key_id_set) < num_of_challenges:
            key_id_set.add(get_random_bytes(32))

        for key_id_bytes, weak_key in zip(key_id_set, weak_key_set):
            # cast weak_key to bytes
            weak_key_bytes = weak_key.to_bytes(32, 'big')
            # random bytes for key
            key_bytes = get_random_bytes(32)

            # concatenate id_bytes and key_bytes, this will be encrypted
            plaintext = key_id_bytes + key_bytes
            aes = AES.new(weak_key_bytes, AES.MODE_GCM, nonce=bytes(
                16))  # otherwise nonce is generated automatically

            ciphertext, tag = aes.encrypt_and_digest(plaintext)
            self.secrets[key_id_bytes] = {'key': key_bytes,
                                          'ciphertext': ciphertext, 'tag': tag}

    def get_challenges(self):
        challenges = {}
        for challenge_id, secret in enumerate(self.secrets.values()):
            challenges[challenge_id] = {'ciphertext': secret['ciphertext'],
                                        'tag': secret['tag']}

        return challenges

    def set_challenge_id(self, id_bytes: bytes):
        self.key_bytes = self.secrets[id_bytes]['key']

    def __str__(self):
        return str(vars(self))
