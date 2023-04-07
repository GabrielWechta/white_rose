import hashlib
import random
from typing import Tuple, List, Callable, Literal

import matplotlib.pyplot as plt


def get_multiplicity(multiplicity_range: int | Tuple[int, int]) -> int:
    if isinstance(multiplicity_range, int):
        multiplicity = multiplicity_range
    elif isinstance(multiplicity_range, tuple) and len(multiplicity_range) == 2:
        multiplicity = random.randint(a=multiplicity_range[0], b=multiplicity_range[1])
    else:
        raise TypeError("Expected int or tuple of 2 ints")
    return multiplicity


def get_in_bands_percent(data, distance=0.1):
    if len(data) == 0:
        return False
    count = len(list(filter(lambda x: abs(x - 1) < distance, data)))
    return count / len(data)


def check_margin(data, delta):
    counter = 0
    for value in data:
        if 1 - delta <= value <= 1 + delta:
            counter += 1
    print(f"{counter/len(data)=}")
    return counter / len(data)


def generate_multiset(elements_range: int | Tuple[int, int], multiplicity_range: int | Tuple[int, int] = 1) -> List[
    int]:
    multiset = []
    if isinstance(elements_range, int):
        for element in range(elements_range):
            multiplicity = get_multiplicity(multiplicity_range=multiplicity_range)
            multiset.extend([element] * multiplicity)
    elif isinstance(elements_range, tuple) and len(elements_range) == 2:
        a, b = elements_range
        for element in range(a, b):
            multiplicity = get_multiplicity(multiplicity_range=multiplicity_range)
            multiset.extend([element] * multiplicity)
    else:
        raise TypeError("Expected int or tuple of 2 ints")
    random.shuffle(multiset)
    return multiset


def disjoint_ranges_generator(upper_bound=10 ** 4 + 1):
    range_start = 1
    for n in range(1, upper_bound):
        range_end = range_start + n  # S1={1}, S2={2,3}, S3={4,5,6}, ...
        yield n, range_start, range_end
        range_start = range_end


class BadHash:
    def __init__(self, data):
        self.data = data

    def hexdigest(self):
        hash_value = 0
        for byte in self.data:
            hash_value += byte
            hash_value = hash_value % 2 ** 256
        hash_value += 2 ** 8
        return format(hash_value, '32x')


HASH_FUNCTIONS_DICT = {
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "blake2b": hashlib.blake2b,
    "md5": hashlib.md5,
    "bad_hash": BadHash
}


def define_hash(bit_length: int, hash_function_name: str,
                return_type: Literal[
                    "truncated_normalized_hash", "truncated_hash"] = "truncated_normalized_hash") -> Callable:
    hash_function = HASH_FUNCTIONS_DICT[hash_function_name]

    if return_type == "truncated_normalized_hash":
        class TruncatedNormalizedHash:
            def __call__(self, data: bytes):
                hash_value = hash_function(data).hexdigest()
                # Convert hash value to binary string
                binary_string = bin(int(hash_value, 16))[3:]
                # Subtract 8 digits from the end of the binary string
                binary_string_cut = binary_string[:bit_length]
                # Convert binary string to float between 0 and 1
                value = int(binary_string_cut, 2) / (2 ** (len(binary_string_cut)))
                return value

        return TruncatedNormalizedHash()
    elif return_type == "truncated_hash":
        class TruncatedHash:
            def __call__(self, data: bytes):
                hash_value = hash_function(data).hexdigest()
                binary_string = bin(int(hash_value, 16))[3:]
                binary_string_cut = binary_string[:bit_length]
                return binary_string_cut

        return TruncatedHash()

    else:
        raise ValueError(f"Unknown argument {return_type=}")


def plot_data(data, xlabel: str, ylabel: str):
    plt.scatter(x=[n for n in range(len(data))], y=data)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def test():
    truncated_ordered_hash = define_hash(10)
    print(truncated_ordered_hash(data=b"abc"))
    print(truncated_ordered_hash(data=b"abc1"))
    print(truncated_ordered_hash(data=b"abc2"))

    multiset = generate_multiset(elements_range=5, multiplicity_range=2)
    print(multiset)
    multiset = generate_multiset(elements_range=5, multiplicity_range=(1, 3))
    print(multiset)
    multiset = generate_multiset(elements_range=(3, 5), multiplicity_range=2)
    print(multiset)
    multiset = generate_multiset(elements_range=(3, 5), multiplicity_range=(2, 5))
    print(multiset)


def test_2():
    for n, range_start, range_end in disjoint_ranges_generator(100):
        print(n)
        print(generate_multiset(elements_range=(range_start, range_end)))


def main():
    ...


if __name__ == "__main__":
    test_2()

# %%
