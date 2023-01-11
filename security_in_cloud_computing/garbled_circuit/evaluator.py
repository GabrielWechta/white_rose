from typing import Tuple, List

from common_protocol import Responder
from klib import jload, jstore
from mcl_utils import Fr, get_Fr, get_G
from oblivious_polynomial_evaluation.oblivious_polynomial_evaluation_utils import Polynomial, ConnectedPolynomial, \
    HASH_CLS, BYTES_XOR, GROUP
from parser import parse_args


class Evaluator(Responder):
    def __init__(self, x2: bool, ot_type: str, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Responder.__init__(self, ip, port)
        self.x2 = x2
        self.ot_type = ot_type

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
    evaluator = Evaluator(x2=args.x2, ot_type=args.ot_type, ip=args.ip, port=args.port)

    commitment_pairs_ = evaluator.receive_message()
    commitment_pairs = jload({"S": [(Fr, Fr)]}, commitment_pairs_, True)["S"]
    evaluator.set_commitment_pairs(commitment_pairs=commitment_pairs)

    evaluator.mask_commitment()

    Rs_ = evaluator.receive_message()
    Rs = jload({"R": [GROUP]}, Rs_, True)["R"]
    evaluator.set_Rs(Rs=Rs)

    W = evaluator.produce_W(...)
    evaluator.send_message(jstore({"W": W}))

    Cs_ = evaluator.receive_message()
    Cs = jload({"c": [str]}, Cs_, True)["c"]
    evaluator.set_Cs(Cs=Cs)


if __name__ == "__main__":
    main()
