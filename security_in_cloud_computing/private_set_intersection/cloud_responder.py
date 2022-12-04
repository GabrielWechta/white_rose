from common_protocol import Responder
from klib import jload, jstore
from mcl_utils import get_G, GT, G1, G2
from parser import parse_args
from private_set_intersection.cloud import Cloud
from private_set_intersection.private_set_intersection_utils import GROUP


class CloudResponder(Responder, Cloud):
    def __init__(self, g: GROUP, private_set: list, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Responder.__init__(self, ip, port)
        Cloud.__init__(self, g=g, private_set=private_set)


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    cloud_responder = CloudResponder(g=g, private_set=["a", "d", "c", "f"], ip=args.ip, port=args.port)

    A_ = cloud_responder.receive_message()
    A = jload({"A": [GROUP]}, A_, True)
    party_public_set = A["A"]
    cloud_responder.set_party_public_set(party_public_set)

    mine_public_set = cloud_responder.produce_mine_public_set()
    party_public_set_mine = cloud_responder.produce_party_public_set_mine()

    cloud_responder.send_message(message=jstore({"B": mine_public_set, "Ap": party_public_set_mine}))

    mB_ = cloud_responder.receive_message()
    mB = jload({"mB": [GROUP]}, mB_, True)
    mine_public_set_party = mB["mB"]
    cloud_responder.set_mine_public_set_party(mine_public_set_party)

    cloud_responder.calculate_intersection()


if __name__ == "__main__":
    main()
