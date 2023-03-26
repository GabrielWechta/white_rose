from data_stream_utils import define_hash, generate_multiset


class MinCount:
    def __init__(self, M_length, h, data_stream=None):
        self.M_length = M_length
        self.h = h
        self.data_stream = data_stream
        self.M = [1 for _ in range(M_length)]
        # self.hashes = []

    def set_data_stream(self, data_stream):
        self.data_stream = data_stream

    def consume_data_stream(self):
        for s in self.data_stream:
            s_bytes = s.to_bytes((s.bit_length() + 7) // 8, 'big')
            h_s = self.h(s_bytes)
            # self.hashes.append(h_s)
            if h_s not in self.M and h_s < self.M[-1]:
                self.M[-1] = h_s
                self.M.sort()
            # print(self.M[0])

    def estimate_number_of_elements(self):
        if self.M[-1] == 1:
            return len(list(filter(lambda x: x != 1, self.M)))
        else:
            return (self.M_length - 1) / self.M[-1]


def test():
    min_count = MinCount(M_length=4, h=define_hash(bit_length=8, hash_function_name="sha256"),
                         data_stream=generate_multiset(elements_range=3, multiplicity_range=(1, 2)))
    min_count.consume_data_stream()


if __name__ == "__main__":
    test()
