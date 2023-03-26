from data_stream_utils import define_hash, generate_multiset
from min_count_algorithm import MinCount


def subtask_a():
    range_start = 1
    k = 900
    for n in range(10 ** 3 + 1):
        range_end = range_start + n + 1
        data_stream = generate_multiset(elements_range=(range_start, range_end), multiplicity_range=1)
        min_count = MinCount(M_length=k, h=define_hash(bit_length=64, hash_function_name="sha256"),
                             data_stream=data_stream)
        min_count.consume_data_stream()
        n_hat = min_count.estimate_number_of_elements()
        print(f"{n_hat=}")
        range_start = range_end


def subtask_b():
    range_start = 1
    range_end = 1
    # for n in range(10 ** 4 + 1):
    for n in range(10 ** 2, 10 ** 2 + 1):
        range_end = range_start + n
        data_stream = generate_multiset(elements_range=(range_start, range_end), multiplicity_range=1)
        for k in [2, 3, 10, 100, 400]:
            min_count = MinCount(M_length=k, h=define_hash(bit_length=256, hash_function_name="sha256"),
                                 data_stream=data_stream)
            min_count.consume_data_stream()
            min_count.plot_data(data=min_count.M)
            n_hat = min_count.estimate_number_of_elements()
            print(f"{n=}:{n_hat=}")
        range_start = range_end + 1


if __name__ == "__main__":
    subtask_a()
