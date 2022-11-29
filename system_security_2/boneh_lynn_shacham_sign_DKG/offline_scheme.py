from boneh_lynn_shacham_sign_DKG.signer import Signer
from boneh_lynn_shacham_sign_DKG.verifier import Verifier
from mcl_utils import get_G, G2


def main():
    g2 = get_G(value=b"BLS Signature", group=G2)
    signer = Signer(g2=g2)
    verifier = Verifier(g2=g2)
    X2 = signer.get_pub_key()
    for i in range(4):
        m = f"We are Boneh, Lynn and Shacham, there are {i} of us."
        sigma = signer.sign(m=m)
        print(f"{m=}")
        verifier.verify(X2=X2, sigma=sigma, m=m)


if __name__ == "__main__":
    main()
