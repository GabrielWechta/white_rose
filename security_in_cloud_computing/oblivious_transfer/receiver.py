import base64
from typing import List

from common_protocol import Initiator
from klib import jload, jstore
from mcl_utils import get_Fr, get_G
from oblivious_transfer.oblivious_transfer_utils import GROUP, BYTES_XOR, HASH_CLS
from oblivious_transfer.parser import parse_args


class Receiver(Initiator):
    def __init__(self, j: int, g: GROUP, ot_type: str, n: int, ip: str, port: int):
        super().__init__(ip, port)
        self.j = j
        self.g = g
        self.ot_type = ot_type
        self.n = n

        self.alpha = None
        self.Rs = None
        self.Cs = None
        self.W = None

    def set_Rs(self, Rs: List[GROUP]):
        self.Rs = Rs

    def produce_W(self):
        self.alpha = get_Fr()
        R = self.Rs[self.j]
        self.W = R * self.alpha
        return self.W

    def set_Cs(self, Cs: List[str]):
        self.Cs = Cs

    def produce_message(self):
        C = self.Cs[self.j]
        hash_obj = HASH_CLS()
        hash_obj.update(bytes(self.g * self.alpha))
        c_bytes = base64.b64decode(C)
        h_bytes = hash_obj.digest()
        m_bytes = BYTES_XOR(base64.b64decode(C), hash_obj.digest())
        print(c_bytes)
        print(h_bytes)
        print(m_bytes)
        # print(m_bytes.decode("ascii"))
        m = base64.b64encode(m_bytes).decode("ascii")
        return m


def main():
    args = parse_args()
    g = get_G(value=b"Oblivious Transfer", group=GROUP)
    receiver = Receiver(j=1, g=g, ot_type=args.ot_type, n=args.n, ip=args.ip, port=args.port)

    Rs_ = receiver.receive_message()
    Rs = jload({"Rs": [GROUP]}, Rs_, True)["Rs"]
    receiver.set_Rs(Rs=Rs)

    W = receiver.produce_W()
    receiver.send_message(jstore({"W": W}))

    Cs_ = receiver.receive_message()
    Cs = jload({"Cs": [str]}, Cs_, True)["Cs"]
    receiver.set_Cs(Cs=Cs)

    m = receiver.produce_message()
    print(m)


if __name__ == "__main__":
    main()
