from mcl_utils import get_G1
from okamoto_is.prover import Prover
from okamoto_is.verifier import Verifier


def main():
    g_1 = get_G1(b"Okamoto IS 1")
    g_2 = get_G1(b"Okamoto IS 2")
    prover = Prover(g_1=g_1, g_2=g_2)
    verifier = Verifier(g_1=g_1, g_2=g_2)

    A = prover.publish_pub_key()
    verifier.receive_pub_key(A=A)

    X = prover.produce_commitment()
    verifier.receive_commitment(X=X)

    c = verifier.produce_challenge()
    prover.receive_challenge(c=c)

    s_1, s_2 = prover.produce_response()
    verifier.receive_response(s_1=s_1, s_2=s_2)

    if verifier.verify_response() is True:
        print("Verification successful.")
    else:
        print("Verification failure.")


if __name__ == "__main__":
    main()
