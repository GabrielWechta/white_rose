from common_protocol import Responder
from klib import jload, jstore
from mcl_utils import get_Fr, get_G
from oblivious_transfer.oblivious_transfer_utils import GROUP, HASH_CLS, BYTES_XOR
from parser import parse_args
import base64


class Sender(Responder):
    def __init__(self, g: GROUP, ot_type: str, n: int, ip: str, port: int):
        super().__init__(ip, port)
        self.g = g
        self.ot_type = ot_type
        self.n = n
        self.messages = [f"I am {i} message." for i in range(self.n)]

        self.rs = []
        self.Rs = []
        self.Cs = []
        self.W = None

    def produce_Rs(self):
        for _ in range(self.n):
            r = get_Fr()
            self.rs.append(r)
            self.Rs.append(self.g * r)
        return self.Rs

    def set_W(self, W: GROUP):
        self.W = W

    def produce_Cs(self):
        for r, R, m in zip(self.rs, self.Rs, self.messages):
            if self.ot_type == "krzywiecki":
                K = self.W * (get_Fr(1) / r)
            elif self.ot_type == "rev_gr_el":
                K = (self.W - R) * r
            hash_obj = HASH_CLS()
            K_bytes = str(K).encode("utf-8")
            hash_obj.update(K_bytes)
            h_K_bytes = hash_obj.digest()
            m_bytes = m.encode("utf-8")
            C_bytes = BYTES_XOR(m_bytes, h_K_bytes)
            C = C_bytes.hex()
            self.Cs.append(C)
        return self.Cs


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    sender = Sender(g=g, ot_type=args.ot_type, n=args.n, ip=args.ip, port=args.port)

    Rs = sender.produce_Rs()
    sender.send_message(jstore({"Rs": Rs}))

    W_ = sender.receive_message()
    W = jload({"W": GROUP}, W_, True)["W"]
    sender.set_W(W=W)

    Cs = sender.produce_Cs()
    sender.send_message(jstore({"Cs": Cs}))


if __name__ == "__main__":
    main()
