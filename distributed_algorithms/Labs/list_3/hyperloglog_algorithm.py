import math

from counting_algorithm_interface import CountingAlgorithmInterface
from list_3.data_stream_utils import define_hash, generate_multiset


class HyperLogLog(CountingAlgorithmInterface):
    def __init__(self, M_length, h, data_stream=None):
        self.M_length = M_length
        self.b = math.ceil(math.log2(M_length))
        self.h = h
        self.data_stream = data_stream
        self.M = [float('-inf') for _ in range(M_length)]

    def refresh_M(self):
        self.M = [1 for _ in range(self.M_length)]
        self.b = math.ceil(math.log2(self.M_length))

    def replace_data_stream(self, data_stream):
        self.data_stream = data_stream
        self.refresh_M()

    def replace_M_length(self, M_length):
        self.M_length = M_length
        self.refresh_M()

    @staticmethod
    def first_one(bit_string):
        return next((i for i, char in enumerate(bit_string) if char == "1"), len(bit_string))

    def consume_data_stream(self):
        for e in self.data_stream:
            e_bytes = e.to_bytes((e.bit_length() + 7) // 8, 'big')
            h_e_bits = self.h(e_bytes)
            address_bits = h_e_bits[:self.b]
            value_bits = h_e_bits[self.b + 1:]

            address = int(address_bits, 2)
            first_one_index = self.first_one(bit_string=value_bits)
            self.M[address] = max(self.M[address], first_one_index)

    def estimate_number_of_elements(self):
        harmon_mean = 0
        for M_i in self.M:
            harmon_mean += 2 ** (-M_i)

        return self.alpha * self.M_length ** 2 * 1 / harmon_mean


def test():
    min_count = HyperLogLog(M_length=4,
                            h=define_hash(bit_length=8, hash_function_name="sha256", return_type="truncated_hash"),
                            data_stream=generate_multiset(elements_range=3, multiplicity_range=1))
    min_count.consume_data_stream()


if __name__ == "__main__":
    test()
