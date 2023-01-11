from common_protocol import Initiator
from klib import jstore, jload
from mcl_utils import get_Fr, get_G, std_concat_method, G1, G2
from naxos_ake.naxos_ake_utils import GROUP, HASH_CLS, LAM
from naxos_ake.naxos_party import NAXOSParty
from parser import parse_args


class AParty(Initiator, NAXOSParty):
    def __init__(self, g: GROUP, lam: int, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Initiator.__init__(self, ip, port)
        NAXOSParty.__init__(self, g=g, lam=lam)

    def produce_session_key(self):
        t1 = self.commitment_y * self.sk_m
        t2 = self.pk_y * self.commitment_exp_m
        t3 = self.commitment_y * self.commitment_exp_m
        concat = std_concat_method(t1, t2, t3, self.pk_m, self.pk_y)
        self.hash_obj.update(concat)
        self.K = self.hash_obj.digest()


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    a_party = AParty(g=g, lam=LAM, ip=args.ip, port=args.port)

    a_party.send_message(message=jstore({"pk_A": a_party.pk_m}))

    pk_B_ = a_party.receive_message()
    pk_B = jload({"pk_B": GROUP}, pk_B_, True)["pk_B"]
    a_party.set_another_party_pk(pk_B)

    a_party.send_message(message=jstore({"X": a_party.produce_commitment()}))

    Y_ = a_party.receive_message()
    Y = jload({"Y": GROUP}, Y_, True)["Y"]
    a_party.set_another_party_commitment(Y)

    a_party.produce_session_key()
    a_party.show_K()


if __name__ == "__main__":
    main()
