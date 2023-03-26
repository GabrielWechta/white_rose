import hashlib
import random
from typing import Tuple, List, Callable

import matplotlib.pyplot as plt


def get_multiplicity(multiplicity_range: int | Tuple[int, int]) -> int:
    if isinstance(multiplicity_range, int):
        multiplicity = multiplicity_range
    elif isinstance(multiplicity_range, tuple) and len(multiplicity_range) == 2:
        multiplicity = random.randint(a=multiplicity_range[0], b=multiplicity_range[1])
    else:
        raise TypeError("Expected int or tuple of 2 ints")
    return multiplicity


def generate_multiset(elements_range: int | Tuple[int, int], multiplicity_range: int | Tuple[int, int]) -> List[int]:
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


HASH_FUNCTIONS_DICT = {
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
    "blake2b": hashlib.blake2b,
    "blake2s": hashlib.blake2s,
    "md5": hashlib.md5
}


def define_hash(bit_length: int, hash_function_name: str) -> Callable:
    hash_function = HASH_FUNCTIONS_DICT[hash_function_name]

    class TruncatedOrderedHash:
        def __call__(self, data: bytes):
            hash_value = hash_function(data).hexdigest()
            # Convert hash value to binary string
            binary_string = bin(int(hash_value, 16))[3:]
            # Subtract 8 digits from the end of the binary string
            binary_string_cut = binary_string[:bit_length]
            # Convert binary string to float between 0 and 1
            value = int(binary_string_cut, 2) / (2 ** (len(binary_string_cut)))
            return value

    return TruncatedOrderedHash()


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


def main():
    ...


if __name__ == "__main__":
    test()
