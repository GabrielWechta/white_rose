from common_protocol import Initiator
from mcl_utils import get_Fr, get_G1, jstore, jload, Fr, monitor_func, G1

HOSTNAME = "localhost"
PORT = 15000
GROUP = G1


class Prover(Initiator):
    def __init__(self, g_1: GROUP, g_2: GROUP, ip: str = None,
                 port: int = None):
        if ip is not None and port is not None:
            super().__init__(ip, port)
        self.g_1 = g_1
        self.g_2 = g_2
        self.a_1 = get_Fr()
        self.a_2 = get_Fr()
        self.x_1 = None
        self.x_2 = None
        self.X = None
        self.A = self.g_1 * self.a_1 + self.g_2 * self.a_2
        self.c = None
        self.s_1 = None
        self.s_2 = None

    @monitor_func
    def publish_pub_key(self):
        return self.A

    @monitor_func
    def produce_commitment(self):
        self.x_1 = get_Fr()
        self.x_2 = get_Fr()
        self.X = self.g_1 * self.x_1 + self.g_2 * self.x_2
        return self.X

    @monitor_func
    def receive_challenge(self, c):
        self.c = c

    @monitor_func
    def produce_response(self):
        self.s_1 = self.x_1 + self.a_1 * self.c
        self.s_2 = self.x_2 + self.a_2 * self.c
        return self.s_1, self.s_2


def main():
    g_1 = get_G1(b"Okamoto IS 1")
    g_2 = get_G1(b"Okamoto IS 2")
    prover = Prover(g_1=g_1, g_2=g_2, ip=HOSTNAME, port=PORT)

    A = prover.publish_pub_key()
    prover.send_message(message=jstore({"A": A}))

    X = prover.produce_commitment()
    prover.send_message(message=jstore({"X": X}))

    c_ = prover.receive_message()
    c = jload({'c': Fr}, c_)[0]
    prover.receive_challenge(c=c)

    s_1, s_2 = prover.produce_response()
    prover.send_message(message=jstore({"s_1": s_1, "s_2": s_2}))

    status = prover.receive_message()
    print(status)


if __name__ == "__main__":
    main()
