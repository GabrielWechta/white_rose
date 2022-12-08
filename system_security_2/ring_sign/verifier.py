from common_protocol import Responder
from klib import jload
from mcl_utils import get_G, get_Fr, mcl_sum, Fr
from parser import parse_args
from ring_sign.ring_signature_utils import GROUP, CONCAT_METHOD


class Verifier(Responder):
    def __init__(self, g: GROUP, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            super().__init__(ip, port)
        self.g = g

    def verify(self, s, Rs, m, As):
        nums = []
        for R, A in zip(Rs, As):
            nums.append(R + (A * get_Fr(CONCAT_METHOD(m, R))))
        if self.g * s == mcl_sum(nums):
            print("Signature verified")
        else:
            print("Signature rejected")


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    verifier = Verifier(g=g, ip=args.ip, port=args.port)

    As_ = verifier.receive_message()
    As = jload({"As": [GROUP]}, As_, True)["As"]

    m_s_Rs_ = verifier.receive_message()
    m_s_Rs = jload({"m": str, "s": Fr, "Rs": [GROUP]}, m_s_Rs_, True)
    m = m_s_Rs["m"]
    s = m_s_Rs["s"]
    Rs = m_s_Rs["Rs"]

    verifier.verify(s=s, Rs=Rs, m=m, As=As)


if __name__ == "__main__":
    main()
