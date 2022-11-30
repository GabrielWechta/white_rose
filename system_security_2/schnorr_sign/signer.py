from common_protocol import Initiator
from klib import jstore
from mcl_utils import get_Fr, get_G, std_concat_method, Fr
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
        h = Fr.setHashOf(std_concat_method(X, m))
        s = x + self.a * h
        return X, s, m


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    signer = Signer(g=g, ip=args.ip, port=args.port)

    public_key = signer.get_pub_key()

    message = "I am Claus-Peter Schnorr."
    commitment, response, _ = signer.sign(m=message)
    signer.send_message(message=jstore({"X": commitment, "s": response, "m": message, "A": public_key}))


if __name__ == "__main__":
    main()
