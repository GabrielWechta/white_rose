from common_protocol import Initiator
from klib import jstore
from mcl_utils import get_Fr, get_G, mcl_sum
from parser import parse_args
from ring_sign.ring_signature_utils import GROUP, PUB_KEYS_NUM, create_pub_key, CONCAT_METHOD


class Signer(Initiator):
    def __init__(self, g: GROUP, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            super().__init__(ip, port)
        self.g = g
        self.a = get_Fr()
        self.pub_key = self.g * self.a
        self.rs = []
        self.Rs = []
        self.hs = []

        self.pub_keys = [next(create_pub_key(g=g)) for _ in range(PUB_KEYS_NUM)]
        self.pub_keys.append(self.pub_key)
        self.pub_keys_exp = []

    def get_pub_keys(self):
        return self.pub_keys

    def sign(self, m: str):
        for pub_key in self.pub_keys:
            if pub_key == self.pub_key:
                continue

            r = get_Fr()
            while r in self.rs:
                r = get_Fr()

            R = self.g * r
            h = get_Fr(CONCAT_METHOD(m, R))
            self.rs.append(r)
            self.Rs.append(R)
            self.pub_keys_exp.append(pub_key * h)
        r = get_Fr()
        R = (self.g * r) - mcl_sum(self.pub_keys_exp)
        self.Rs.append(R)
        h = get_Fr(CONCAT_METHOD(m, R))
        s = r + mcl_sum(self.rs) + self.a * h
        return s, self.Rs


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)

    signer = Signer(g=g, ip=args.ip, port=args.port)
    As = signer.get_pub_keys()

    m = "In the land of Mordor, in the fires of Mount Doom, " \
        "the Dark Lord Sauron forged in secret a master Ring, " \
        "to control all others. And into this Ring, he poured his " \
        "cruelty, his malice, and his will to dominate all life. " \
        "One Ring to rule them all."
    s, Rs = signer.sign(m=m)
    signer.send_message(message=jstore({"m": m, "s": s, "R": Rs, "A": As}))

    response = signer.receive_message()
    print(response)


if __name__ == "__main__":
    main()
