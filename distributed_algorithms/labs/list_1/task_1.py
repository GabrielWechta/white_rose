from list_1.leader_election_utils import Channel, Node


def p0_generator(nodes_num: int):
    while True:
        yield 1 / nodes_num


def known_n_test(n: int):
    channel = Channel()
    nodes = [Node(node_id=node_id, channel=channel, p_generator_ref=p0_generator(nodes_num=n)) for node_id in range(n)]
    while True:
        for node in nodes:
            node.election()
        if channel.exists_single():
            break
        channel.extend_slots()
    for node in nodes:
        if node.node_id == channel.get_leader_id():
            node.node_type = "leader"
            node.channel.describe()


def main():
    known_n_test(1000)


if __name__ == "__main__":
    main()
