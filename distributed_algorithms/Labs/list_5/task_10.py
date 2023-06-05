import time
from datetime import datetime
from itertools import product
from typing import List, Tuple

log_file = open(f"task_10_{datetime.now().strftime('%H:%M:%S')}.log", "w")

def tee(*args, **kwargs):
    print(*args, **kwargs)
    print(*args, file=log_file, **kwargs)

class DijkstraMutualExclusionSimulator:
    def __init__(self, n: int) -> None:
        self.n = n
        self.max_steps = 0
        self.legal_configurations = set()
        for configuration in product(range(self.n + 1), repeat=self.n):
            # if configuration has only one possible move it is legal
            if len(self.list_possible_moves(configuration)) == 1:
                self.legal_configurations.add(configuration)

    def list_possible_moves(self, configuration: Tuple[int]) -> List[Tuple[int]]:
        possible_moves = []
        if configuration[0] == configuration[-1]:  # P0 accesses the shared resource
            new_val = (configuration[0] + 1) % (self.n + 1)
            possible_moves.append((new_val, *configuration[1:]))
        for i in range(1, self.n):
            if configuration[i] != configuration[i - 1]:  # Pi accesses the shared resource
                possible_moves.append((*configuration[:i], configuration[i - 1], *configuration[i + 1:]))
        return possible_moves

    def simulate_ring(self, start_configuration: Tuple[int], steps: int = 0) -> None:
        possible_moves = self.list_possible_moves(configuration=start_configuration)
        if len(possible_moves) == 0:
            raise ValueError("Simulation ended with no possible moves")
        else:
            for configuration in possible_moves:
                if configuration in self.legal_configurations:
                    self.max_steps = max(self.max_steps, steps + 1)
                else:
                    self.simulate_ring(start_configuration=configuration, steps=steps + 1)

    def simulate_experiment(self):
        for configuration in product(range(self.n + 1), repeat=self.n):
            if configuration not in self.legal_configurations:
                self.simulate_ring(start_configuration=configuration)


if __name__ == '__main__':
    start_time = time.time()
    N = 6
    for n in range(1, N):
        simulation = DijkstraMutualExclusionSimulator(n=n)
        simulation.simulate_experiment()
        tee(f"For {n=}, max_steps={simulation.max_steps}")
    tee(f"Finished in {time.time() - start_time} seconds")
