from common_protocol import Initiator
from mcl_utils import get_Fr, jstore, jload, Fr, monitor_func, G1, G2, \
    get_G, std_concat_method

HOSTNAME = "0.0.0.0"
PORT = 15000
GROUP_G = G2
GROUP_G_HAT = G1
CONCAT_METHOD = std_concat_method


class Prover(Initiator):
    def __init__(self, g: GROUP_G, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            super().__init__(ip, port)
        self.g = g
        self.g_hat = None
        self.a = get_Fr()
        self.x = None
        self.X = None
        self.A = self.g * self.a
        self.c = None
        self.S = None

    @monitor_func
    def publish_pub_key(self):
        return self.A

    @monitor_func
    def produce_commitment(self):
        self.x = get_Fr()
        self.X = self.g * self.x
        return self.X

    @monitor_func
    def receive_challenge(self, c):
        self.c = c

    @monitor_func
    def compute_g_hat(self):
        self.g_hat = get_G(value=CONCAT_METHOD(self.X, self.c),
                           group=GROUP_G_HAT)

    @monitor_func
    def produce_response(self):
        self.S = self.g_hat * (self.x + self.a * self.c)
        return self.S


def main():
    g = get_G(value=b"Modified Schnorr IS", group=GROUP_G)
    prover = Prover(g=g, ip=HOSTNAME, port=PORT)

    A = prover.publish_pub_key()
    # prover.send_message(message=jstore({"A": A}))

    X = prover.produce_commitment()
    prover.send_message(message=jstore({"X": X, "A": A}))

    c_ = prover.receive_message()
    c = jload({'c': Fr}, c_)[0]
    prover.receive_challenge(c=c)

    prover.compute_g_hat()

    S = prover.produce_response()
    prover.send_message(message=jstore({"S": S}))

    status = prover.receive_message()
    print(status)


if __name__ == "__main__":
    main()
