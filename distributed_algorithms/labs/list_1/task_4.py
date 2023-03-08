import math

from list_1.leader_election_utils import LSimulator


def main():
    l_simulator = LSimulator(number_of_experiments=5000)
    success_prob = l_simulator.calculate_success_in_first_round_prob(u=1000)
    print(f"{success_prob=}")


if __name__ == "__main__":
    main()
