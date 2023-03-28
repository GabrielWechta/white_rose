from typing import List, Union

from matplotlib import pyplot as plt

from list_2.data_stream_utils import define_hash, generate_multiset, HASH_FUNCTIONS_DICT
from list_2.min_count_algorithm import MinCount


def plot_diff_hash_fun(data: List[List[Union[int, float]]]):
    n_range = range(1, len(data[0]) + 1)
    plt.scatter(x=n_range, y=data[0], c='blue', label='sha1', s=2)
    plt.scatter(x=n_range, y=data[1], c='green', label='sha256', s=2)
    plt.scatter(x=n_range, y=data[2], c='olive', label='sha512', s=2)
    plt.scatter(x=n_range, y=data[3], c='magenta', label='blake2b', s=2)
    plt.scatter(x=n_range, y=data[4], c='cyan', label='md5', s=2)
    plt.scatter(x=n_range, y=data[5], c='red', label='badHash', s=2)
    plt.xlabel('n')
    plt.ylabel(r'$\frac{\hat{n}}{n}$', rotation=90)
    plt.title(r'$\frac{\hat{n}}{n}$ for different hash functions. (k=452, b_len=64)')
    plt.legend()
    plt.savefig('figures/task_2_fig_diff_hash.png')
    plt.show()


def plot_diff_bit_length(data: List[List[Union[int, float]]]):
    n_range = range(1, len(data[0]) + 1)
    plt.scatter(x=n_range, y=data[0], c='blue', label='bit_len=8', s=2)
    plt.scatter(x=n_range, y=data[1], c='green', label='bit_len=16', s=2)
    plt.scatter(x=n_range, y=data[2], c='olive', label='bit_len=24', s=2)
    plt.scatter(x=n_range, y=data[3], c='magenta', label='bit_len=28', s=2)
    plt.scatter(x=n_range, y=data[4], c='cyan', label='bit_len=32', s=2)
    plt.xlabel('n')
    plt.ylabel(r'$\frac{\hat{n}}{n}$', rotation=90)
    plt.title(r'$\frac{\hat{n}}{n}$ for different hash functions. (k=452, hash_fun=sha256)')
    plt.legend()
    plt.savefig('figures/task_2_fig_diff_bit_length.png')
    plt.show()


def bad_hash(data):
    hash_value = 0
    for byte in data:
        hash_value += byte
    return hash_value % 2 ** 256


def test_diff_hash_fun():
    # experiment parameters
    k = 452
    hash_bit_length = 64

    plot_data = [[], [], [], [], [], []]
    for i, (hash_function_name, hash_function) in enumerate(HASH_FUNCTIONS_DICT.items()):
        print(f"doing {hash_function_name=}")
        min_count = MinCount(M_length=k,
                             h=define_hash(bit_length=hash_bit_length, hash_function_name=hash_function_name))
        range_start = 1
        for n in range(1, 10 ** 3 + 1):
            range_end = range_start + n + 1
            data_stream = generate_multiset(elements_range=(range_start, range_end),
                                            multiplicity_range=1)
            min_count.set_data_stream(data_stream=data_stream)
            min_count.consume_data_stream()
            n_hat = min_count.estimate_number_of_elements()
            plot_data[i].append(n_hat / n)
            range_start = range_end

    plot_diff_hash_fun(data=plot_data)


def test_diff_bit_length():
    # experiment parameters
    k = 452

    plot_data = [[], [], [], [], [], []]
    for i, hash_bit_length in enumerate([8, 16, 24, 28, 32]):
        print(f"doing {hash_bit_length=}")
        min_count = MinCount(M_length=k,
                             h=define_hash(bit_length=hash_bit_length, hash_function_name="sha256"))
        range_start = 1
        for n in range(1, 5000):
            range_end = range_start + n + 1
            data_stream = generate_multiset(elements_range=(range_start, range_end),
                                            multiplicity_range=1)
            min_count.set_data_stream(data_stream=data_stream)
            min_count.consume_data_stream()
            n_hat = min_count.estimate_number_of_elements()
            plot_data[i].append(n_hat / n)
            range_start = range_end

    plot_diff_bit_length(data=plot_data)
    # It should hold that B=2*log_2(n) to avoid collision


if __name__ == "__main__":
    test_diff_bit_length()
