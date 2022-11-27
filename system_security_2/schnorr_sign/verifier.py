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
        hash_obj = HASH_CLS()
        hash_obj.update(std_concat_method(str(X), m))
        h_bytes = hash_obj.digest()
        h = get_Fr(value=int.from_bytes(h_bytes, "big"))
        if self.g * s == X + (A * h):
            print("Signature verified")
        else:
            print("Signature rejected")


def main():
    args = parse_args()
    g = get_G(value=b"Schnorr Signature", group=GROUP)
    verifier = Verifier(g=g, ip=args.ip, port=args.port)

    A_ = verifier.receive_message()
    A = jload({"A": GROUP}, A_, True)["A"]

    sig_ = verifier.receive_message()
    sig = jload({"sig": (GROUP, Fr, str)}, sig_, True)["sig"]
    X, s, m = sig
    sigma = (X, s)

    verifier.verify(A=A, sigma=sigma, m=m)


if __name__ == "__main__":
    main()
