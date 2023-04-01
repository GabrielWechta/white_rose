from typing import List, Union

from matplotlib import pyplot as plt

from list_2.data_stream_utils import define_hash, generate_multiset
from list_2.min_count_algorithm import MinCount


def plot_task_7(data: List[List[Union[int, float]]], title=r'$\frac{\hat{n}}{n}$ for different hash'):
    n_range = range(1, len(data[0]) + 1)
    plt.scatter(x=n_range, y=data[0], c='blue', label='sha1', s=2)
    # plt.scatter(x=n_range, y=data[1], c='green', label='sha256', s=2)
    # plt.scatter(x=n_range, y=data[2], c='olive', label='sha512', s=2)
    # plt.scatter(x=n_range, y=data[3], c='magenta', label='blake2b', s=2)
    # plt.scatter(x=n_range, y=data[4], c='cyan', label='md5', s=2)
    # plt.scatter(x=n_range, y=data[5], c='red', label='badHash', s=2)
    plt.xlabel('n')
    plt.ylabel(r'$\frac{\hat{n}}{n}$', rotation=90)
    plt.title(title)
    plt.legend()
    plt.axhline(y=1.1, color='gray', linestyle='dotted')

    # plt.savefig(f'figures/task_7_delta_{delta}.png')
    plt.show()


def task_7():
    # experiment parameters
    k = 400
    hash_bit_length = 64
    min_count = MinCount(M_length=k,
                         h=define_hash(bit_length=hash_bit_length, hash_function_name="sha256"))
    plot_data = [[], [], [], []]
    # for i, alpha in enumerate([0.05, 0.01, 0.005]):
    for i, alpha in enumerate([0.05]):
        print(f"doing {alpha=}")
        range_start = 1
        for n in range(1, 10 ** 3 + 1):

            range_end = range_start + n
            data_stream = generate_multiset(elements_range=(range_start, range_end),
                                            multiplicity_range=1)
            min_count.set_data_stream(data_stream=data_stream)
            min_count.consume_data_stream()
            n_hat = min_count.estimate_number_of_elements()
            plot_data[i].append(n_hat / n)
            range_start = range_end
            print(n_hat, n)

    plot_task_7(data=plot_data)


if __name__ == "__main__":
    task_7()
