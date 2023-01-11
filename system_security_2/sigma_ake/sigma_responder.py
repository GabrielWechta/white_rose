from common_protocol import Responder
from klib import jload, jstore
from mcl_utils import get_G, get_Fr, Fr
from naxos_ake.naxos_ake_utils import GROUP
from parser import parse_args
from sigma_ake.sigma_party import SIGMAParty


class SIGMAResponder(Responder, SIGMAParty):
    def __init__(self, g: GROUP, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Responder.__init__(self, ip, port)
        self.g = g
        self.b = get_Fr()
        self.B = self.g * self.b

        self.produce_ephemeral(g=self.g)

    def get_pub_key(self):
        return self.B


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    responder = SIGMAResponder(g=g, ip=args.ip, port=args.port)
    Y = responder.get_eph_pub_key()
    B = responder.get_pub_key()

    X_A_ = responder.receive_message()
    X, A = jload({"X": GROUP, "A": GROUP}, X_A_)
    responder.derive_keys(eph_pub=X, eph_priv_key=responder.eph_priv_key)

    sigma, mac = responder.sign_and_mac(g=g, priv_key=responder.b, message=(X, Y, "1"), cert=B)
    responder.send_message(jstore({
        "Y": Y,
        "sig_commit": sigma[0],
        "sig_response": sigma[1],
        "MB": mac,
        "B": B
    }))

    sigcommit_sigresponse_MA_ = responder.receive_message()
    sig_commit, sig_response, MA = jload({
        "sig_commit": GROUP,
        "sig_response": Fr,
        "MA": GROUP,
    }, sigcommit_sigresponse_MA_)

    # verifying MAC
    if responder.MAC_verify(mac=MA, key=responder.K0, cert=A):
        print("MAC verified")
    else:
        print("MAC not verified. Rejecting...")
        raise ValueError("Bad Mac")

    # verifying signature
    if responder.schnorr_verify(g=g, pub_key=A, sigma=(sig_commit, sig_response), message=(X, Y, "0")):
        print("Signature verified")
    else:
        print("Signature not verified. Rejecting...")
        raise ValueError("Bad Signature")

    print(f"{responder.K1=}")


if __name__ == "__main__":
    main()
