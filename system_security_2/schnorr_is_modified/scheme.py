from schnorr_is.prover import Prover
from schnorr_is.verifier import Verifier
from mcl_utils import get_G1


def main():
    g = get_G1()

    prover = Prover(g=g)
    verifier = Verifier(g=g, A=prover.A)

    # commitment
    X = prover.produce_commitment()
    verifier.receive_commitment(X=X)

    # challenge
    c = verifier.produce_challenge()
    prover.receive_challenge(c=c)

    # response
    s = prover.produce_response()
    verifier.receive_response(s=s)

    # verification
    if verifier.verify_response() is True:
        print("Verification successful.")
    else:
        print("Failed verification.")


if __name__ == "__main__":
    main()
