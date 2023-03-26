from typing import List, Union

from matplotlib import pyplot as plt

from data_stream_utils import define_hash, generate_multiset
from min_count_algorithm import MinCount


def plot_subtask_b(data: List[List[Union[int, float]]]):
    plt.scatter(x=data[0], y=data[1], c='blue', label='k=2', s=5)
    plt.scatter(x=data[0], y=data[2], c='green', label='k=3', s=5)
    plt.scatter(x=data[0], y=data[3], c='olive', label='k=10', s=5)
    plt.scatter(x=data[0], y=data[4], c='magenta', label='k=100', s=5)
    plt.scatter(x=data[0], y=data[5], c='cyan', label='k=400', s=5)
    plt.xlabel('n')
    plt.ylabel(r'$\frac{\hat{n}}{n}$')
    plt.title(r'$\frac{\hat{n}}{n}$ for different k values. Task 1.b.')
    plt.legend()
    plt.show()


# def plot_subtask_b(data: List[List[int, float]]):
#     data_0, data_1, data_2, data_3 = numpy.array(data[0]), numpy.array(data[1]), numpy.array(data[2]), numpy.array(
#         data[3])
#     plt.scatter(data_0, np.subtract(data_0, data_1), c='red', label='y1')
#     plt.scatter(data_0, np.subtract(data_0, data_2), c='green', label='y2')
#     plt.scatter(data_0, np.subtract(data_0, data_3), c='blue', label='y3')
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.title('Scatter Plot with 3 Variables')
#     plt.legend()
#     plt.show()

def subtask_a():
    # experiment parameters
    k = 100
    bit_length = 64
    hash_function_name = "sha256"

    range_start = 1
    min_count = MinCount(M_length=k, h=define_hash(bit_length=bit_length, hash_function_name=hash_function_name))
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
    bit_length = 64
    hash_function_name = "sha256"
    multiplicity_range = 1

    range_start = 1
    plot_data = [[], [], [], [], [], []]
    for dim, k in enumerate([2, 3, 10, 100, 400]):
        min_count = MinCount(M_length=k,
                             h=define_hash(bit_length=bit_length, hash_function_name=hash_function_name))
        for n in range(1, 10 ** 3 + 1):
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


if __name__ == "__main__":
    subtask_b()
