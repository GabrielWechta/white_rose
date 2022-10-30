from common_protocol import Responder
from mcl_utils import get_Fr, jstore, jload, G1, G2, Fr, monitor_func, \
    std_concat_method, get_G, GT

HOSTNAME = "localhost"
PORT = 15000
GROUP_G = G1
GROUP_G_HAT = G2
CONCAT_METHOD = std_concat_method


class Verifier(Responder):
    def __init__(self, g: GROUP_G, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            super().__init__(ip, port)
        self.g = g
        self.g_hat = None
        self.A = None
        self.c = None
        self.X = None
        self.S = None

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
    def receive_response(self, S):
        self.S = S

    @monitor_func
    def compute_g_hat(self):
        self.g_hat = get_G(value=CONCAT_METHOD(self.X, self.c),
                           group=GROUP_G_HAT)

    @monitor_func
    def verify_response(self):
        if GT.pairing(self.g, self.S) == GT.pairing(self.X + self.A * self.c,
                                                    self.g_hat):
            return True
        else:
            return False


def main():
    g = get_G(value=b"Modified Schnorr IS", group=GROUP_G)
    verifier = Verifier(g=g, ip=HOSTNAME, port=PORT)

    A_ = verifier.receive_message()
    A = jload({"A": G1}, A_)[0]
    verifier.receive_pub_key(A=A)

    X_ = verifier.receive_message()
    X = jload({'X': G1}, X_)[0]
    verifier.receive_commitment(X=X)

    c = verifier.produce_challenge()
    verifier.send_message(message=jstore({"c": c}))

    verifier.compute_g_hat()

    S_ = verifier.receive_message()
    S = jload({'S': GROUP_G_HAT}, S_)[0]
    verifier.receive_response(S=S)

    if verifier.verify_response() is True:
        verifier.send_message("Verification successful.")
        print("Verification successful.")
    else:
        verifier.send_message("Verification failure.")
        print("Verification failure.")


if __name__ == "__main__":
    main()
