from common_protocol import Initiator
from klib import jstore
from mcl_utils import get_Fr, get_G, std_concat_method, G1, G2
from parser import parse_args

CONCAT_METHOD = std_concat_method


class Signer(Initiator):
    def __init__(self, g2: G2, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            super().__init__(ip, port)
        self.g2 = g2
        self.x2 = get_Fr()
        self.X2 = self.g2 * self.x2

    def get_pub_key(self):
        return self.X2

    def sign(self, m: str):
        h1 = get_G(value=m.encode(), group=G1)
        sigma = h1 * self.x2
        return sigma


def main():
    args = parse_args()
    g2 = get_G(value=b"genQ", group=G2)
    signer = Signer(g2=g2, ip=args.ip, port=args.port)

    X2 = signer.get_pub_key()
    # signer.send_message(message=jstore({"X2": X2}))

    m = "We are Boneh, Lynn and Shacham."
    sigma = signer.sign(m=m)
    signer.send_message(message=jstore({"S": sigma, "m": m, "X": X2}))


if __name__ == "__main__":
    main()
