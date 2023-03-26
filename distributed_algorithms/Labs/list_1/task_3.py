import math

from list_1.leader_election_utils import LSimulator


def main():
    l_simulator = LSimulator(number_of_experiments=5000)

    # Expected value
    expected_value, variance = l_simulator.estimate_expected_value_and_variance(nodes_num=1000)
    print(f"{math.e=}\n")

    # theoretical result: E(L) < e;
    print(f"{expected_value=}")
    # theoretical result:
    print(f"{variance=}")


if __name__ == "__main__":
    main()
