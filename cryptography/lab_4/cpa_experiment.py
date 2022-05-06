import random
from typing import List
from encryptor import Encryptor


class CPAExperiment:
    def __init__(self, privkey, bc_mode):
        self.encryptor = Encryptor(private_key=privkey, bc_mode=bc_mode,
                                   do_random_iv=False)
        self.privkey = privkey
        self.bc_mode = bc_mode
        self.b = None

    def refresh_encryptor(self):
        self.encryptor = Encryptor(private_key=self.privkey,
                                   bc_mode=self.bc_mode)

    def conduct_stage_one(self, messages: List[bytes]):
        query_dict = {}
        for i, message in enumerate(messages):
            result = self.encryptor.encrypt(message)
            query_dict[i] = result
        return query_dict

    def get_challenge(self, message1: bytes, message2: bytes):
        self.b = random.randint(1, 2)
        if self.b == 1:
            result = self.encryptor.encrypt(message1)
        else:
            result = self.encryptor.encrypt(message2)

        return result

    def conduct_stage_two(self, messages: List[bytes]):
        query_dict = {}
        for i, message in enumerate(messages):
            result = self.encryptor.encrypt(message)
            query_dict[i] = result
        return query_dict

    def check_b(self, b_guessed):
        if b_guessed == self.b:
            return True
        else:
            return False
