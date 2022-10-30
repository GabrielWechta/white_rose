from common_protocol import Responder
from mcl_utils import get_Fr, get_G1, jstore, jload, G1, Fr, monitor_func

HOSTNAME = "localhost"
PORT = 15000
GROUP = G1


class Verifier(Responder):
    def __init__(self, g_1: GROUP, g_2: GROUP, ip: str = None,
                 port: int = None):
        if ip is not None and port is not None:
            super().__init__(ip, port)
        self.g_1 = g_1
        self.g_2 = g_2
        self.A = None
        self.c = None
        self.X = None
        self.s_1 = None
        self.s_2 = None

    @monitor_func
    def produce_challenge(self):
        self.c = get_Fr()
        return self.c

    @monitor_func
    def receive_pub_key(self, A):
        self.A = A

    @monitor_func
    def receive_commitment(self, X):
        self.X = X

    @monitor_func
    def receive_response(self, s_1, s_2):
        self.s_1 = s_1
        self.s_2 = s_2

    @monitor_func
    def verify_response(self):
        if self.g_1 * self.s_1 + self.g_2 * self.s_2 == self.X + (
                self.A * self.c):
            return True
        else:
            return False


def main():
    g_1 = get_G1(b"Okamoto IS 1")
    g_2 = get_G1(b"Okamoto IS 2")
    verifier = Verifier(g_1=g_1, g_2=g_2, ip=HOSTNAME, port=PORT)

    A_ = verifier.receive_message()
    A = jload({"A": G1}, A_)[0]
    verifier.receive_pub_key(A=A)

    X_ = verifier.receive_message()
    X = jload({'X': G1}, X_)[0]
    verifier.receive_commitment(X=X)

    c = verifier.produce_challenge()
    verifier.send_message(message=jstore({"c": c}))

    s_ = verifier.receive_message()
    s_1, s_2 = jload({'s_1': Fr, 's_2': Fr}, s_)
    verifier.receive_response(s_1=s_1, s_2=s_2)

    if verifier.verify_response() is True:
        verifier.send_message("Verification successful.")
        print("Verification successful.")
    else:
        verifier.send_message("Verification failure.")
        print("Verification failure.")


if __name__ == "__main__":
    main()
