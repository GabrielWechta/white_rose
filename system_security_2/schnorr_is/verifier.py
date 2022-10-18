from common_protocol import Responder
from mcl_utils import get_Fr, get_G1, jstore, jload, G1, Fr

HOSTNAME = "localhost"
PORT = 15000


class Verifier(Responder):
    def __init__(self, g, ip: str, port: int):
        super().__init__(ip, port)
        self.g = g
        self.A = None
        self.c = None
        self.X = None
        self.s = None

    def produce_challenge(self):
        self.c = get_Fr()
        print(f"Producing challenge:\n{self.c=}.")
        return self.c

    def receive_pub_key(self, A):
        self.A = A
        print(f"Receiving public key:\n{self.A=}.")

    def receive_commitment(self, X):
        self.X = X
        print(f"Receiving commitment:\n{self.X=}.")

    def receive_response(self, s):
        self.s = s
        print(f"Receiving response:\n{self.s=}.")

    def verify_response(self):
        print(
            f"Verifying response: {self.g * self.s == self.X + (self.A * self.c)=}")
        if self.g * self.s == self.X + (self.A * self.c):
            return True
        else:
            return False


def main():
    g = get_G1(b"Schnorr IS")
    verifier = Verifier(g=g, ip=HOSTNAME, port=PORT)

    A_ = verifier.receive_message()
    A = jload({'A': G1}, A_)[0]
    verifier.receive_pub_key(A=A)

    X_ = verifier.receive_message()
    X = jload({'X': G1}, X_)[0]
    verifier.receive_commitment(X=X)

    c = verifier.produce_challenge()
    verifier.send_message(message=jstore({"c": c}))

    s_ = verifier.receive_message()
    s = jload({'s': Fr}, s_)[0]
    verifier.receive_response(s=s)

    if verifier.verify_response() is True:
        print("Verification successful.")
    else:
        print("Verification failure.")


if __name__ == "__main__":
    main()
