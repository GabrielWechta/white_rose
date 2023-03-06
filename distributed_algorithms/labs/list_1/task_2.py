import random

import matplotlib.pyplot as plt

from list_1.leader_election_utils import Channel, Node


def known_n_p_generator(nodes_num: int):
    while True:
        yield 1 / nodes_num


def known_u_p_generator(nodes_num: int):
    while True:
        yield 1 / nodes_num


class LSimulator:
    def __init__(self, number_of_experiments: int):
        self.number_of_experiments = number_of_experiments

    @staticmethod
    def get_L_known_n(n: int):
        channel = Channel()
        nodes = [Node(node_id=node_id, channel=channel, p_generator_ref=p0_generator(nodes_num=n)) for node_id in
                 range(n)]
        while True:
            for node in nodes:
                node.election()
            if channel.exists_single():
                break
            channel.extend_slots()
        return channel.get_slots_length()

    def get_L_known_u(self, u: int):
        n = random.randint(1, u)
        return self.get_L_known_n(n=n)

    def plot_histogram(self, n: int = None, u: int = None):
        if n is None and u is None:
            raise ValueError("Specify `n` or `u`.")
        if n is not None:
            experiment_results = []
            for _ in range(self.number_of_experiments):
                experiment_results.append(self.get_L_known_n(n=n))
            bins = sorted(set(experiment_results))
            plt.hist(experiment_results, bins=bins, alpha=0.7, align='left', label=f"{n=}")
        if u is not None:
            experiment_results = []
            for _ in range(self.number_of_experiments):
                experiment_results.append(self.get_L_known_u(u=u))
            bins = sorted(set(experiment_results))
            plt.hist(experiment_results, bins=bins, alpha=0.7, align='left', label=f"{u=}")

        plt.xlabel('Number of slots')
        plt.ylabel('Number of results')
        plt.title('Histogram of the random variable L')
        plt.xticks(bins, bins)
        plt.legend(loc='upper right')
        plt.show()


def main():
    l_simulator = LSimulator(number_of_experiments=10000)
    # case 1: n=2
    n = 2
    l_simulator.plot_histogram(n=n, u=n)
    # case 2: u=n/2
    n = 200
    l_simulator.plot_histogram(n=n, u=n // 2)
    # case 3: u=n
    n = 200
    l_simulator.plot_histogram(n=n, u=n)


if __name__ == "__main__":
    main()
