import pathlib
from typing import List, Union, Callable

from PIL import Image
from matplotlib import pyplot as plt

from data_stream_utils import define_hash, generate_multiset
from min_count_algorithm import MinCount

HASH_FUNCTION_NAME = "sha256"
HASH_BIT_LENGTH = 64
PRESENTATION_MODE = False
SAVE_FIGURES = True


def plot_subtask_b(data: List[List[Union[int, float]]]):
    plt.scatter(x=data[0], y=data[1], c='blue', label='k=2', s=5)
    plt.scatter(x=data[0], y=data[2], c='green', label='k=3', s=5)
    plt.scatter(x=data[0], y=data[3], c='olive', label='k=10', s=5)
    plt.scatter(x=data[0], y=data[4], c='magenta', label='k=100', s=5)
    plt.scatter(x=data[0], y=data[5], c='cyan', label='k=400', s=5)
    plt.xlabel('n')
    plt.ylabel(r'$\frac{\hat{n}}{n}$')
    plt.title(r'$\frac{\hat{n}}{n}$ for different k values. (Task 1.b)')
    plt.legend()
    if SAVE_FIGURES is True:
        plt.savefig('figures/subtask_b_fig.png')
    plt.show()


def plot_subtask_c(data: List[List[Union[int, float]]]):
    plt.scatter(x=data[0], y=data[1], c='cyan', s=5)
    plt.xlabel('n')
    plt.ylabel('k')
    plt.title(r'Plotting $k$ such that $|\frac{\hat{n}}{n} - 1| < 0.1$. (Task 1.c)')
    if SAVE_FIGURES is True:
        plt.savefig('figures/subtask_c_fig.png')
    plt.show()


def subtask_a():
    # experiment parameters
    k = 100

    range_start = 1
    min_count = MinCount(M_length=k, h=define_hash(bit_length=HASH_BIT_LENGTH, hash_function_name=HASH_FUNCTION_NAME))
    for n in range(1, 10 ** 4 + 1):
        verification_array = []
        range_end = range_start + n + 1  # S1={1}, S2={2,3}, S3={4,5,6}, ...
        for i, multiplicity_range in enumerate([1, 2, (1, 3)]):
            data_stream = generate_multiset(elements_range=(range_start, range_end),
                                            multiplicity_range=multiplicity_range)
            min_count.set_data_stream(data_stream=data_stream)
            min_count.consume_data_stream()
            n_hat = min_count.estimate_number_of_elements()
            verification_array.append(n_hat)  # add n_hat cord

        # if all elements are equal, thus multiplicity has no impact.
        if not all(elem == verification_array[0] for elem in verification_array):
            raise Exception("Multiplicity have impact.")
        range_start = range_end


def subtask_b():
    # experiment parameters
    multiplicity_range = 1

    range_start = 1
    plot_data = [[], [], [], [], [], []]
    for dim, k in enumerate([2, 3, 10, 100, 400]):
        print(k)
        min_count = MinCount(M_length=k,
                             h=define_hash(bit_length=HASH_BIT_LENGTH, hash_function_name=HASH_FUNCTION_NAME))
        for n in range(1, 10 ** 4 + 1):
            range_end = range_start + n + 1  # S1={1}, S2={2,3}, S3={4,5,6}, ...
            data_stream = generate_multiset(elements_range=(range_start, range_end),
                                            multiplicity_range=multiplicity_range)
            min_count.set_data_stream(data_stream=data_stream)
            min_count.consume_data_stream()
            n_hat = min_count.estimate_number_of_elements()
            if dim == 0:
                plot_data[0].append(n)
            plot_data[dim + 1].append(n_hat / n)
    plot_subtask_b(data=plot_data)


def get_in_bands_percent(data, distance=0.1):
    count = len(list(filter(lambda x: abs(x - 1) < distance, data)))
    return count / len(data)


def subtask_c():
    def get_n_hat():
        min_count = MinCount(M_length=k,
                             h=define_hash(bit_length=HASH_BIT_LENGTH, hash_function_name=HASH_FUNCTION_NAME))
        min_count.set_data_stream(data_stream=data_stream)
        min_count.consume_data_stream()
        n_hat_inside = min_count.estimate_number_of_elements()
        return n_hat_inside

    # experiment parameters
    k = 1
    range_start = 1
    exp_result = []
    plot_data = [[], []]
    for n in range(1, 10 ** 4 + 1):
        print(n)
        range_end = range_start + n  # S1={1}, S2={2,3}, S3={4,5,6}, ...
        data_stream = generate_multiset(elements_range=(range_start, range_end), multiplicity_range=1)
        n_hat = get_n_hat()
        exp_result.append(n_hat / n)
        while get_in_bands_percent(data=exp_result) < 0.95:
            k += 1
            n_hat = get_n_hat()
            exp_result[-1] = (n_hat / n)

        plot_data[0].append(n)
        plot_data[1].append(k)
        range_start = range_end
    plot_subtask_c(data=plot_data)


def present(subtask: Callable, path_to_fig: pathlib.Path):
    if PRESENTATION_MODE is True:
        img = Image.open(str(path_to_fig))
        img.show()
    else:
        subtask()


if __name__ == "__main__":
    present(subtask=subtask_c, path_to_fig=pathlib.Path("figures/subtask_c_fig.png"))
