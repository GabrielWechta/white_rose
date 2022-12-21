from common_protocol import Initiator
from klib import jstore, jload
from mcl_utils import get_Fr, get_G, std_concat_method, Fr
from naxos_ake.naxos_ake_utils import GROUP
from parser import parse_args
from sigma_ake.sigma_party import SIGMAParty

CONCAT_METHOD = std_concat_method


class SIGMAInitiator(Initiator, SIGMAParty):
    def __init__(self, g: GROUP, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Initiator.__init__(self, ip, port)
        self.g = g
        self.a = get_Fr()
        self.A = self.g * self.a

        self.produce_ephemeral(g=self.g)

    def get_pub_key(self):
        return self.A


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    initiator = SIGMAInitiator(g=g, ip=args.ip, port=args.port)

    # s = initiator.produce_session_identifier()
    X = initiator.get_eph_pub_key()
    A = initiator.get_pub_key()
    initiator.send_message(jstore({"X": X, "A": A}))

    Y_sigcommit_sigresponse_MB_B_ = initiator.receive_message()
    Y, sig_commit, sig_response, MB, B = jload({
        "Y": GROUP,
        "sig_commit": GROUP,
        "sig_response": Fr,
        "MB": GROUP,
        "B": GROUP
    }, Y_sigcommit_sigresponse_MB_B_)

    initiator.derive_keys(eph_pub=Y, eph_priv_key=initiator.eph_priv_key)
    # verifying MAC
    if initiator.MAC_verify(mac=MB, key=initiator.K0, cert=B):
        print("MAC verified")
    else:
        print("MAC not verified. Rejecting...")
        raise ValueError("Bad Mac")

    # verifying signature
    if initiator.schnorr_verify(g=g, pub_key=B, sigma=(sig_commit, sig_response), message=("1", X, Y)):
        print("Signature verified")
    else:
        print("Signature not verified. Rejecting...")
        raise ValueError("Bad Signature")

    sigma, mac = initiator.sign_and_mac(g=g, priv_key=initiator.a, message=("0", X, Y), cert=A)
    initiator.send_message(jstore({
        "sig_commit": sigma[0],
        "sig_response": sigma[1],
        "MA": mac
    }))

    print(f"{initiator.K1=}")


if __name__ == "__main__":
    main()
