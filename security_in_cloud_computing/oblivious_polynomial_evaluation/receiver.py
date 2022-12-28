from typing import Tuple, List

from common_protocol import Responder
from klib import jload, jstore
from mcl_utils import Fr, get_Fr, get_G
from oblivious_polynomial_evaluation.oblivious_polynomial_evaluation_utils import Polynomial, ConnectedPolynomial, \
    HASH_CLS, BYTES_XOR, GROUP
from parser import parse_args


class Receiver(Responder):
    def __init__(self, n: int, k: int, g: GROUP, ot_type: str, alpha: int, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Responder.__init__(self, ip, port)
        self.n = n
        self.k = k
        self.g = g
        self.ot_type = ot_type
        self.degree_P = (self.n - 1) // self.k
        self.degree_Px = self.n - 1
        self.P = Polynomial(degree=self.degree_P)
        print(f"{self.P(get_Fr(alpha))=}")
        self.Px = Polynomial(degree=self.degree_Px, coefficient_0_0=0)

        self.Q = ConnectedPolynomial(A=self.Px, O=self.P)

        self.commitment_pairs = None
        self.masked_commitment = None
        self.rs = []
        self.Rs = []
        self.Cs = []
        self.W = None

    def set_commitment_pairs(self, commitment_pairs: List[Tuple[Fr, Fr]]):
        self.commitment_pairs = commitment_pairs

    def mask_commitment(self):
        self.masked_commitment = []
        for abscissa, ordinate in self.commitment_pairs:
            self.masked_commitment.append(self.Q(abscissa=abscissa, ordinate=ordinate))

    def produce_Rs(self):
        self.rs = []
        self.Rs = []
        for _ in range(len(self.commitment_pairs)):
            r = get_Fr()
            self.rs.append(r)
            self.Rs.append(self.g * r)
        return self.Rs

    def set_W(self, W: GROUP):
        self.W = W

    def produce_Cs(self):
        self.Cs = []
        for r, R, m_fr in zip(self.rs, self.Rs, self.masked_commitment):
            if self.ot_type == "krzywiecki":
                K = self.W * (get_Fr(1) / r)
            elif self.ot_type == "rev_gr_el":
                K = (self.W - R) * r
            hash_obj = HASH_CLS()
            K_bytes = str(K).encode()
            hash_obj.update(K_bytes)
            h_K_bytes = hash_obj.digest()
            m_bytes = m_fr.serialize()
            C_bytes = BYTES_XOR(m_bytes, h_K_bytes)
            C = C_bytes.hex()
            self.Cs.append(C)
        return self.Cs


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    receiver = Receiver(n=args.n, k=args.k, g=g, ot_type=args.ot_type, alpha=args.alpha, ip=args.ip, port=args.port)

    commitment_pairs_ = receiver.receive_message()
    commitment_pairs = jload({"S": [(Fr, Fr)]}, commitment_pairs_, True)["S"]
    receiver.set_commitment_pairs(commitment_pairs=commitment_pairs)

    receiver.mask_commitment()

    for i in range(receiver.n):
        print(f"Doing {i} OT.")
        Rs = receiver.produce_Rs()
        receiver.send_message(jstore({"Rs": Rs}))

        W_ = receiver.receive_message()
        W = jload({"W": GROUP}, W_, True)["W"]
        receiver.set_W(W=W)

        Cs = receiver.produce_Cs()
        receiver.send_message(jstore({"Cs": Cs}))


if __name__ == "__main__":
    main()
