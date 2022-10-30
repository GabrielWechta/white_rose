from mcl_utils import get_G, G1, G2, std_concat_method
from schnorr_modified_is.prover import Prover
from schnorr_modified_is.verifier import Verifier

GROUP_G = G1
GROUP_G_HAT = G2
CONCAT_METHOD = std_concat_method


def main():
    g = get_G(value=b"Modified Schnorr IS", group=GROUP_G)
    prover = Prover(g=g)
    verifier = Verifier(g=g)

    A = prover.publish_pub_key()
    verifier.receive_pub_key(A=A)

    X = prover.produce_commitment()
    verifier.receive_commitment(X=X)

    c = verifier.produce_challenge()
    prover.receive_challenge(c=c)

    prover.compute_g_hat()
    verifier.compute_g_hat()

    S = prover.produce_response()
    verifier.receive_response(S=S)

    if verifier.verify_response() is True:
        print("Verification successful.")
    else:
        print("Verification failure.")


if __name__ == "__main__":
    main()
