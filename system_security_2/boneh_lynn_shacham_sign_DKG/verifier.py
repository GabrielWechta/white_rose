from common_protocol import Responder
from klib import jload
from mcl_utils import get_G, GT, G1, G2
from parser import parse_args


class Verifier(Responder):
    def __init__(self, g2: G2, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            super().__init__(ip, port)
        self.g2 = g2

    def verify(self, X2, sigma, m):
        h1 = get_G(value=m.encode("utf-8"), group=G1)
        if GT.pairing(sigma, self.g2) == GT.pairing(h1, X2):
            print("Signature verified")
        else:
            print("Signature rejected")


def main():
    args = parse_args()
    g2 = get_G(value=b"BLS Signature", group=G2)
    verifier = Verifier(g2=g2, ip=args.ip, port=args.port)

    X2_ = verifier.receive_message()
    X2 = jload({"X2": G2}, X2_, True)["X2"]

    sig_ = verifier.receive_message()
    sigma, m = jload({"sig": (G1, str)}, sig_, True)["sig"]

    verifier.verify(X2=X2, sigma=sigma, m=m)


if __name__ == "__main__":
    main()
