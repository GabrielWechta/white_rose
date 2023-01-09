import random
from random import shuffle
from typing import List

from common_protocol import Initiator
from klib import jload, jstore
from mcl_utils import get_G, G1, get_Fr, Fr
from oblivious_polynomial_evaluation.oblivious_polynomial_evaluation_utils import Polynomial, GROUP, HASH_CLS, \
    BYTES_XOR, lagrangian_interpolation_list
from parser import parse_args


class Sender(Initiator):
    def __init__(self, n: int, m: int, k: int, g: GROUP, ot_type: str, alpha: int, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Initiator.__init__(self, ip, port)
        self.n = n
        self.m = m
        self.k = k
        self.alpha = alpha
        self.g = g
        self.ot_type = ot_type
        self.S = Polynomial(degree=self.k, coefficient_0_0=self.alpha)

        self.I = []
        self.interpolation_pairs = []
        self.xs = []
        self.rand_exp = None
        self.Rs = None
        self.Cs = None
        self.W = None

    def produce_commitment_pairs(self):
        self.xs = [get_Fr() for _ in range(self.n * self.m)]
        while len(self.I) < self.n:
            rand_ind = random.randint(a=0, b=self.n * self.m - 1)
            if rand_ind not in self.I:
                self.I.append(rand_ind)

        commitment_pairs = [None] * self.n * self.m
        for ind in range(self.n * self.m):
            if ind in self.I:
                x = self.xs[ind]
                commitment_pairs[ind] = (x, self.S(x))
            else:
                x = self.xs[ind]
                commitment_pairs[ind] = (x, get_Fr())
        print(f"{self.I=}")
        assert len(self.I) == self.n, "Wrong indexes (self.I) length."
        return commitment_pairs

    def set_Rs(self, Rs: List[GROUP]):
        self.Rs = Rs

    def set_Cs(self, Cs: List[str]):
        self.Cs = Cs

    def produce_W(self, j: int):
        self.rand_exp = get_Fr()
        R = self.Rs[j]
        if self.ot_type == "krzywiecki":
            self.W = R * self.rand_exp
        elif self.ot_type == "rev_gr_el":
            self.W = R + (self.g * self.rand_exp)

        return self.W

    def produce_message(self, j: int):
        C = self.Cs[j]
        hash_obj = HASH_CLS()
        if self.ot_type == "krzywiecki":
            g_a_bytes = str(self.g * self.rand_exp).encode()
            hash_obj.update(g_a_bytes)
        elif self.ot_type == "rev_gr_el":
            R = self.Rs[j]
            R_a_bytes = str(R * self.rand_exp).encode()
            hash_obj.update(R_a_bytes)

        h_g_bytes = hash_obj.digest()
        C_bytes = bytes.fromhex(C)
        m_bytes = BYTES_XOR(C_bytes, h_g_bytes)
        m = Fr()
        m.deserialize(m_bytes)
        return m

    def append_interpolation_pair(self, interpolation_pair):
        self.interpolation_pairs.append(interpolation_pair)

    def interpolate_polynomial_P(self):
        value = lagrangian_interpolation_list(x=get_Fr(value=0), abscissa_ordinate_list=self.interpolation_pairs)
        print(f"P(alpha)= {value}")


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    sender = Sender(n=args.n, m=args.m, k=args.k, g=g, ot_type=args.ot_type, alpha=args.alpha, ip=args.ip,
                    port=args.port)

    commitment_pairs = sender.produce_commitment_pairs()
    sender.send_message(jstore({"S": commitment_pairs}))

    for i, ind in enumerate(sender.I):
        print(f"Doing {i} OT.")
        Rs_ = sender.receive_message()
        Rs = jload({"R": [GROUP]}, Rs_, True)["R"]
        sender.set_Rs(Rs=Rs)

        W = sender.produce_W(j=ind)
        sender.send_message(jstore({"W": W}))

        Cs_ = sender.receive_message()
        Cs = jload({"c": [str]}, Cs_, True)["c"]
        sender.set_Cs(Cs=Cs)

        interpolation_ordinate = sender.produce_message(j=ind)
        sender.append_interpolation_pair((sender.xs[ind], interpolation_ordinate))
    sender.interpolate_polynomial_P()


if __name__ == "__main__":
    main()
