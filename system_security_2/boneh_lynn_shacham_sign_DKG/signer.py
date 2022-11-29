from boneh_lynn_shacham_sign_DKG.hsm import RandomnessSource, HSM
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
        self.prng_1 = RandomnessSource(seed=33)
        self.prng_2 = RandomnessSource(seed=222)
        self.HSMs = []
        self.initiate_HSMs()
        self.X2 = self.g2 * self.get_private_key()

    def initiate_HSMs(self):
        self.prng_1.toss_randomness()
        self.prng_2.toss_randomness()
        self.HSMs = [HSM(i, prng_1=self.prng_1, prng_2=self.prng_2) for i in range(1, 5)]

    def get_private_key(self):
        self.prng_1.toss_randomness()
        self.prng_2.toss_randomness()

        x_sum = get_Fr(0)
        for hsm in self.HSMs:
            hsm.produce_tosses()
            x_sum += hsm.get_private_key_share()
        return x_sum

    def get_pub_key(self):
        return self.X2

    def sign(self, m: str):
        h1 = get_G(value=m.encode("utf-8"), group=G1)
        sigma = h1 * self.get_private_key()
        return sigma


def main():
    args = parse_args()
    g2 = get_G(value=b"BLS Signature", group=G2)
    signer = Signer(g2=g2, ip=args.ip, port=args.port)

    X2 = signer.get_pub_key()
    signer.send_message(message=jstore({"X2": X2}))

    m = "We are Boneh, Lynn and Shacham."
    sigma = signer.sign(m=m)
    signer.send_message(message=jstore({"sig": (sigma, m)}))


if __name__ == "__main__":
    main()
