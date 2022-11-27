from common_protocol import Initiator
from klib import jstore
from mcl_utils import get_Fr, get_G, std_concat_method
from parser import parse_args
from schnorr_sign.schnorr_signature_utils import HASH_CLS, GROUP

CONCAT_METHOD = std_concat_method


class Signer(Initiator):
    def __init__(self, g: GROUP, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            super().__init__(ip, port)
        self.g = g
        self.a = get_Fr()
        self.A = self.g * self.a

    def get_pub_key(self):
        return self.A

    def sign(self, m: str):
        x = get_Fr()
        X = self.g * x
        hash_obj = HASH_CLS()
        hash_obj.update(std_concat_method(str(X), m))
        h_bytes = hash_obj.digest()
        h = get_Fr(value=int.from_bytes(h_bytes, "big"))
        s = x + self.a * h
        sigma = (X, s)
        return sigma, m


def main():
    args = parse_args()
    g = get_G(value=b"Schnorr Signature", group=GROUP)
    signer = Signer(g=g, ip=args.ip, port=args.port)

    A = signer.get_pub_key()
    signer.send_message(message=jstore({"A": A}))

    m = "I am Claus-Peter Schnorr."
    sigma, _ = signer.sign(m=m)
    signer.send_message(message=jstore({"sig": (sigma[0], sigma[1], m)}))


if __name__ == "__main__":
    main()
