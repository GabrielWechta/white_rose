from list_1.leader_election_utils import LSimulator


def main():
    l_simulator = LSimulator(number_of_experiments=50000)
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
