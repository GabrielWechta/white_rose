from common_protocol import Initiator
from klib import jstore, jload
from mcl_utils import std_concat_method, get_G, get_Fr
from parser import parse_args
from private_set_intersection.cloud import Cloud
from private_set_intersection.private_set_intersection_utils import GROUP

CONCAT_METHOD = std_concat_method


class CloudInitiator(Initiator, Cloud):
    def __init__(self, g: GROUP, private_set: list, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Initiator.__init__(self, ip, port)
        Cloud.__init__(self, g=g, private_set=private_set)


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    cloud_initiator = CloudInitiator(g=g, private_set=["a", "b", "c", "d"], ip=args.ip, port=args.port)

    mine_public_set = cloud_initiator.produce_mine_public_set()
    cloud_initiator.send_message(message=jstore({"A": mine_public_set}))

    B_C_ = cloud_initiator.receive_message()
    B_C = jload({"B": [GROUP], "C": [GROUP]}, B_C_, True)

    party_public_set = B_C["B"]
    mine_public_set_party = B_C["C"]
    cloud_initiator.set_party_public_set(party_public_set)
    cloud_initiator.set_mine_public_set_party(mine_public_set_party)

    party_public_set_mine = cloud_initiator.produce_party_public_set_mine()
    cloud_initiator.send_message(message=jstore({"D": party_public_set_mine}))

    cloud_initiator.calculate_intersection()


if __name__ == "__main__":
    main()
