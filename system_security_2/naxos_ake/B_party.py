from common_protocol import Responder
from klib import jload, jstore
from mcl_utils import get_G, GT, G1, G2, std_concat_method
from naxos_ake.naxos_ake_utils import GROUP, LAM
from naxos_ake.naxos_party import NAXOSParty
from parser import parse_args


class BParty(Responder, NAXOSParty):
    def __init__(self, g: GROUP, lam: int, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Responder.__init__(self, ip, port)
        NAXOSParty.__init__(self, g=g, lam=lam)

    def produce_session_key(self):
        t1 = self.pk_y * self.commitment_exp_m
        t2 = self.commitment_y * self.sk_m
        t3 = self.commitment_y * self.commitment_exp_m
        concat = std_concat_method(t1, t2, t3, self.pk_y, self.pk_m)
        self.hash_obj.update(concat)
        self.K = self.hash_obj.digest()


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    b_party = BParty(g=g, lam=LAM, ip=args.ip, port=args.port)

    pk_A_ = b_party.receive_message()
    pk_A = jload({"pk_A": GROUP}, pk_A_, True)["pk_A"]
    b_party.set_another_party_pk(pk_A)

    b_party.send_message(message=jstore({"pk_B": b_party.pk_m}))

    X_ = b_party.receive_message()
    X = jload({"X": GROUP}, X_, True)["X"]
    b_party.set_another_party_commitment(X)

    b_party.send_message(message=jstore({"Y": b_party.produce_commitment()}))

    b_party.produce_session_key()
    b_party.show_K()


if __name__ == "__main__":
    main()
