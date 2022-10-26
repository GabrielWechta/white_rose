from common_protocol import Initiator
from mcl_utils import get_Fr, get_G1, jstore, jload, Fr, monitor_func

HOSTNAME = "localhost"
PORT = 15000


class Prover(Initiator):
    def __init__(self, g, ip: str = None, port: int = None):
        super().__init__(ip, port)
        self.g = g
        self.a = get_Fr()
        self.x = None
        self.X = None
        self.A = self.g * self.a
        self.c = None
        self.s = None

    @monitor_func
    def publish_pub_key(self):
        # print(f"Publishing public key:\n{self.A=}.")
        return self.A

    @monitor_func
    def produce_commitment(self):
        self.x = get_Fr()
        self.X = self.g * self.x
        # print(f"Producing commitment:\n{self.X=}.")
        return self.X

    @monitor_func
    def receive_challenge(self, c):
        self.c = c
        # print(f"Receiving challenge:\n{self.c=}.")

    @monitor_func
    def produce_response(self):
        self.s = self.x + self.a * self.c
        # print(f"Producing response:\n{self.s=}.")
        return self.s


def main():
    g = get_G1(b"Schnorr IS")
    prover = Prover(g=g, ip=HOSTNAME, port=PORT)

    A = prover.publish_pub_key()
    prover.send_message(message=jstore({"A": A}))

    X = prover.produce_commitment()
    prover.send_message(message=jstore({"X": X}))

    c_ = prover.receive_message()
    c = jload({'c': Fr}, c_)[0]
    prover.receive_challenge(c=c)

    s = prover.produce_response()
    prover.send_message(message=jstore({"s": s}))


if __name__ == "__main__":
    main()
