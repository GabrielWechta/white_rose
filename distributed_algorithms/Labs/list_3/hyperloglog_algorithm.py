import math

import numpy as np
from scipy.integrate import quad

HASH_BIT_LENGTH = 32
HASH_FUNCTION_NAME = "sha256"

from counting_algorithm_interface import CountingAlgorithmInterface


class HyperLogLog(CountingAlgorithmInterface):
    def __init__(self, M_length, h, data_stream=None):
        self.M_length = M_length
        self.estimator_lower_bound = 5 / 2 * self.M_length
        self.b = math.ceil(math.log2(M_length))
        self.h = h
        self.data_stream = data_stream
        self.M = [0 for _ in range(M_length)]
        self.alpha_m = self.calculate_alpha_m()
        self.H = 2 ** 32
        self.estimator_upper_bound = self.H / 30

    @staticmethod
    def alpha_m_integrand(u, m):
        return np.power(np.log2(np.divide((2 + u), (1 + u))), m)

    def calculate_alpha_m(self):
        integration_result, _ = quad(self.alpha_m_integrand, 0, np.inf, args=[self.M_length])
        final_result = 1 / (integration_result * self.M_length)
        return final_result

    def refresh_M(self):
        self.M = [0 for _ in range(self.M_length)]

    def replace_data_stream(self, data_stream):
        self.data_stream = data_stream
        self.refresh_M()

    def replace_M_length(self, M_length):
        self.M_length = M_length
        self.alpha_m = self.calculate_alpha_m()
        self.b = math.ceil(math.log2(self.M_length))
        self.estimator_lower_bound = 5 / 2 * self.M_length

        self.refresh_M()

    @staticmethod
    def first_one(bit_string):
        return next((1 + i for i, char in enumerate(bit_string) if char == "1"), len(bit_string))

    def consume_data_stream(self):
        for e in self.data_stream:
            e_bytes = e.to_bytes((e.bit_length() + 7) // 8, 'big')
            h_e_bits = self.h(e_bytes)
            address_bits = h_e_bits[:self.b]
            value_bits = h_e_bits[self.b:]

            address = int(address_bits, 2)
            first_one_index = self.first_one(bit_string=value_bits)
            self.M[address] = max(self.M[address], first_one_index)

    def estimate_number_of_elements(self):
        Z = 1 / sum([(1 / 2) ** x for x in self.M])
        n_estimator = self.alpha_m * self.M_length ** 2 * Z

        if n_estimator <= self.estimator_lower_bound:
            V = len([x for x in self.M if x == 0])
            if V != 0:
                n_estimator = self.M_length * math.log(self.M_length / V)
        else:
            if n_estimator > self.estimator_upper_bound:
                n_estimator = self.H * math.log(self.H / (self.H - n_estimator))
        return n_estimator


def test():
    ...


if __name__ == "__main__":
    test()
