import math
import random

from matplotlib import pyplot as plt


def known_n_p_generator(nodes_num: int):
    while True:
        yield 1 / nodes_num


def known_u_p_generator(nodes_num: int):
    m = math.ceil(math.log2(nodes_num))
    while True:
        for i in range(1, m + 1):
            yield (1 / 2) ** i

class Channel:
    def __init__(self):
        self.slots = ["null"]
        self.leader_elected = False
        self.leader_id = None

    def beep(self, slot_ind: int, node_id: int):
        if self.slots[slot_ind] == "null":
            self.slots[slot_ind] = node_id
            self.leader_elected = True
            self.leader_id = node_id
        else:
            self.slots[slot_ind] = "collision"
            self.leader_elected = False
            self.leader_id = None

    def extend_slots(self):
        self.slots.append("null")

    def exists_single(self):
        return self.leader_elected

    def get_leader_id(self):
        return self.leader_id

    def get_slots_length(self):
        return len(self.slots)

    def describe(self):
        print(f"{self.slots=}")
        print(f"{len(self.slots)=}")
        print(f"{self.leader_id=}")


class Node:
    def __init__(self, node_id: int, channel: Channel, p_generator_ref):
        self.node_id = node_id
        self.channel = channel
        self.p_generator = p_generator_ref
        self.node_type = "normal"
        self.i = 0

    def election(self):
        p = next(self.p_generator)
        if random.random() <= p:
            # print(f"{self.i}:{self.node_id}")
            self.channel.beep(slot_ind=self.i, node_id=self.node_id)
        self.i += 1



class LSimulator:
    def __init__(self, number_of_experiments: int):
        self.number_of_experiments = number_of_experiments

    def get_L_known_n(self, n: int):
        L_value = self.perform_experiment(nodes_num=n, p_generator=known_n_p_generator)
        return L_value

    def get_L_known_u(self, u: int):
        n = random.randint(2, u)
        L_value = self.perform_experiment(nodes_num=n, p_generator=known_u_p_generator)
        return L_value

    @staticmethod
    def perform_experiment(nodes_num: int, p_generator):
        channel = Channel()
        nodes = [Node(node_id=node_id, channel=channel, p_generator_ref=p_generator(nodes_num=nodes_num)) for node_id in
                 range(nodes_num)]
        while True:
            for node in nodes:
                node.election()
            if channel.exists_single():
                break
            channel.extend_slots()
        return channel.get_slots_length()

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