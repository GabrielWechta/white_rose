import random


class Attacker:
    def __init__(self):
        self.stage_one_ciphertexts = None
        self.challenge_ciphertext = None
        self.stage_two_ciphertexts = None
        self.zeros = bytes([0] * 16)
        self.ones = bytes([255] * 16)

    @staticmethod
    def bytes_xor(bytes_1: bytes, bytes_2: bytes):
        xored = bytes(
            [l_byte ^ r_byte for l_byte, r_byte in zip(bytes_1, bytes_2)])
        return xored

    @staticmethod
    def produce_stage_one_messages(messages_count):
        stage_one_messages = []
        for i in range(messages_count):
            stage_one_messages.append(i.to_bytes(length=16, byteorder='big'))

        return stage_one_messages

    def set_stage_one_ciphertexts(self, stage_one_ciphertexts):
        self.stage_one_ciphertexts = stage_one_ciphertexts

    def set_challenge_ciphertext(self, challenge_ciphertext):
        self.challenge_ciphertext = challenge_ciphertext

    def set_stage_two_ciphertexts(self, stage_two_ciphertexts):
        self.stage_two_ciphertexts = stage_two_ciphertexts
        pass

    def produce_challenge_messages(self):
        return self.zeros, self.ones

    def produce_stage_two_messages(self):
        latest_iv = self.challenge_ciphertext['iv']
        latest_iv_int = int.from_bytes(latest_iv, byteorder='big')
        next_iv_int = latest_iv_int + 1
        next_iv = next_iv_int.to_bytes(length=16, byteorder='big')
        next_next_iv_int = next_iv_int + 1
        next_next_iv = next_next_iv_int.to_bytes(length=16, byteorder='big')

        zeros_mid = self.bytes_xor(self.zeros, latest_iv)
        ones_mid = self.bytes_xor(self.ones, latest_iv)

        zeros_message = self.bytes_xor(zeros_mid, next_iv)
        ones_message = self.bytes_xor(ones_mid, next_next_iv)

        return zeros_message, ones_message

    def decide_b(self):
        c_b = self.challenge_ciphertext['ciphertext']
        c_1, c_2 = self.stage_two_ciphertexts[0]['ciphertext'], \
                   self.stage_two_ciphertexts[1]['ciphertext']
        if c_b == c_1:
            return 1
        if c_b == c_2:
            return 2

        return "What happened?"
