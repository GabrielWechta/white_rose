from typing import List

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from common_protocol import Initiator
from garbled_circuit.garbled_circuit_utils import BC_MODE
from klib import jload, jstore
from mcl_utils import get_G, get_Fr, Fr
from oblivious_polynomial_evaluation.oblivious_polynomial_evaluation_utils import GROUP, HASH_CLS, \
    BYTES_XOR
from parser import parse_args


class Garbler(Initiator):
    def __init__(self, x1: bool, ot_type: str, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Initiator.__init__(self, ip, port)
        self.x1 = x1
        hash_obj = HASH_CLS()

        self.garb_0 = None
        self.garb_1 = None
        self.eval_0 = None
        self.eval_1 = None

        # OT attributes
        self.ot_type = ot_type
        self.Rs = None
        self.Cs = None
        self.W = None

    def produce_labels(self):
        self.garb_0 = get_random_bytes(16)
        self.garb_1 = get_random_bytes(16)
        self.eval_0 = get_random_bytes(16)
        self.eval_1 = get_random_bytes(16)

    def generate_keys(self):
        pass # TODO START HERE

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


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    garbler = Garbler(x1=args.x1, key=args.key, ip=args.ip, port=args.port)

    garbler.send_message(jstore({...}))

    Rs = garbler.produce_Rs()
    garbler.send_message(jstore({"R": Rs}))

    W_ = garbler.receive_message()
    W = jload({"W": GROUP}, W_, True)["W"]
    garbler.set_W(W=W)

    Cs = garbler.produce_Cs()
    garbler.send_message(jstore({"c": Cs}))


if __name__ == "__main__":
    main()
