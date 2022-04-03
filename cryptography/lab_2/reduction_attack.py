from RSA import RSA
from random import randint
from decimal import Decimal


def get_reductions_for_set(rsa, c_set, blind=False):
    reductions = 0
    if blind is False:
        for c in c_set:
            _, r = rsa.dec(c)
            reductions += r
    else:
        for c in c_set:
            rand = rsa.get_random_element()
            c_blinded = c * rand % rsa.N
            _, r = rsa.dec(c_blinded)
            reductions += r

    return reductions


def generate_reduction_sets(rsa, bit, samples_num):
    # TODO maybe sets?
    set_no_extra_reduction = []
    set_extra_reduction = []

    N, e = rsa.get_public_key()

    power = rsa.power_at_bit(bit)
    if bit < 2:
        prev_power = 2
    else:
        prev_power = rsa.power_at_bit(bit - 1)

    left_border_value = int(Decimal(N) ** Decimal(1 / power))
    right_border_value = int(Decimal(N) ** Decimal(1 / prev_power))

    if 2 >= left_border_value or left_border_value >= right_border_value:
        return [], [], left_border_value, right_border_value

    # trying two times more than wanted sample_count
    try_count = samples_num * 2
    while len(set_no_extra_reduction) < samples_num and try_count > 0:
        random_c = randint(2, left_border_value)
        if not rsa.check_if_will_reduce(random_c, bit):
            set_no_extra_reduction.append(random_c)
        try_count -= 1

    try_count = samples_num * 2
    while len(set_extra_reduction) < samples_num and try_count > 0:
        random_c = randint(left_border_value, right_border_value)
        if rsa.check_if_will_reduce(random_c, bit):
            set_extra_reduction.append(random_c)
        try_count -= 1

    return set_no_extra_reduction, set_extra_reduction, left_border_value, right_border_value


def reduction_attack(rsa, samples_num, bits_num, blind=False):
    if blind is True:
        print("Doing blinded version...")

    previous_bits = [1]

    accuracy = 0

    for bit in range(1, bits_num):
        print(f"Analyzing for bit {bit}...")

        set_no_extra_reduction, set_extra_reduction, _, _ = generate_reduction_sets(rsa, bit, samples_num)

        print("Calculating reductions...")
        ner_reductions = get_reductions_for_set(rsa, set_no_extra_reduction, blind)
        er_reductions = get_reductions_for_set(rsa, set_extra_reduction, blind)

        # Reduction based guess
        if ner_reductions < er_reductions:
            previous_bits.append(1)
        else:
            previous_bits.append(0)

        print(f"Result: {ner_reductions=}, {er_reductions=}")
        accuracy = rsa.compare_exponents(previous_bits)

    return accuracy


if __name__ == "__main__":
    accuracies = []

    for _ in range(10):
        print("Getting RSA object")
        rsa = RSA(128)
        accuracy = reduction_attack(rsa, 7500, 6)
        accuracies.append(accuracy)

    print(f"Reduction accuracy: {(sum(accuracies) / len(accuracies)) * 100}%")
