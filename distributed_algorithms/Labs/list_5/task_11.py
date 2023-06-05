import random

import matplotlib.pyplot as plt
import networkx as nx


class MaximalIndependentSetAlgorithm:
    def __init__(self, graph: nx.Graph) -> None:
        self.graph = graph
        self.nodes_num = len(graph.nodes)
        self.mis = set()

    def accepted(self, v: int):
        return v in self.mis and not self.blocked(v)

    def blocked(self, v: int):
        return any(neighbor in self.mis for neighbor in self.graph[v])

    def candidate(self, v: int):
        return v not in self.mis and not self.blocked(v)

    def invalid(self, v: int):
        return v in self.mis and self.blocked(v)

    def rejected(self, v: int):
        return v not in self.mis and self.blocked(v)

    def valid(self, v: int):
        return self.accepted(v) or self.rejected(v)

    def valid_mis(self):
        return all(self.valid(v) for v in self.graph.nodes)

    def moves_generator(self):
        configuration = tuple(0 for _ in range(self.nodes_num))
        while True:
            moves = []
            if configuration[0] == configuration[-1]:
                new_val = (configuration[0] + 1) % (self.nodes_num + 1)
                moves.append((0, (new_val, *configuration[1:])))
            for i in range(1, self.nodes_num):
                if configuration[i] != configuration[i - 1]:
                    moves.append((i, (*configuration[:i], configuration[i - 1], *configuration[i + 1:])))
            node, configuration = random.choice(moves)
            yield node

    def get_mis(self):
        move = self.moves_generator()
        while not self.valid_mis():
            v = next(move)
            if self.candidate(v):
                self.mis.add(v)
            if self.invalid(v):
                self.mis.remove(v)
        return self.mis


if __name__ == '__main__':
    while True:
        graph: nx.Graph = nx.graph_atlas(random.randint(1, 1000))
        if nx.is_connected(graph):
            break
    simulation = MaximalIndependentSetAlgorithm(graph=graph)

    position = nx.circular_layout(graph)
    labels = {node: str(node) for node in graph.nodes}

    nx.draw(graph, position, node_color='tab:blue', nodelist=sorted(graph.nodes))
    nx.draw_networkx_labels(graph, position, labels=labels, font_color='white', font_size=13)

    maximal_independent_set = simulation.get_mis()
    print(f"{maximal_independent_set = }")
    nx.draw_networkx_nodes(graph, position, nodelist=maximal_independent_set, node_color='tab:red')

    plt.axis('off')
    plt.show()
