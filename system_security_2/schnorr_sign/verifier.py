from common_protocol import Responder
from klib import jload
from mcl_utils import get_Fr, Fr, std_concat_method, get_G
from parser import parse_args
from schnorr_sign.schnorr_signature_utils import GROUP, HASH_CLS


class Verifier(Responder):
    def __init__(self, g: GROUP, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            super().__init__(ip, port)
        self.g = g

    def verify(self, A, sigma, m):
        X, s = sigma
        h = Fr.setHashOf(std_concat_method(X, m))
        if self.g * s == X + (A * h):
            print("Signature verified")
        else:
            print("Signature rejected")


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    verifier = Verifier(g=g, ip=args.ip, port=args.port)

    sig_ = verifier.receive_message()
    sig = jload({"X": GROUP, "s": Fr, "m": str, "A": GROUP}, sig_, True)

    X, s, m, A = sig["X"], sig["s"], sig["m"], sig["A"],
    sigma = (X, s)

    verifier.verify(A=A, sigma=sigma, m=m)


if __name__ == "__main__":
    main()
