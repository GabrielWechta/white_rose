from list_1.leader_election_utils import LSimulator


def main():
    l_simulator = LSimulator(number_of_experiments=50000)
    # case 1: n=2
    n = 2
    l_simulator.plot_histogram(n=n, u=n)
    u = 200
    l_simulator.plot_histogram(n=2, u=u)
    # case 2: u=n/2
    u = 200
    l_simulator.plot_histogram(n=u // 2, u=u)
    # case 3: u=n
    u = 200
    l_simulator.plot_histogram(n=u, u=n)


if __name__ == "__main__":
    main()
