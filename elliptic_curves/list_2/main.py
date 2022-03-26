from EllipticCurve import EllipticCurvePoint, ZeroAtInfinity
from ec_prime_order import generateDomainParameters

def f(R, P, Q, scal_a, scal_b, ord_k):
    if R.x % 3 == 1:
        R_new = R + P
        a_new = (scal_a + 1) % ord_k
        b_new = scal_b
    elif R.x % 3 == 2:
        R_new = 2 * R
        a_new = 2 * scal_a % ord_k
        b_new = 2 * scal_b % ord_k
    else:  # here goes also *zero at infinity*
        R_new = R + Q
        a_new = scal_a
        b_new = (scal_b + 1) % ord_k


def pollard_rho():
    pass


def initialize_dlp_for_EC(n: int):
    generateDomainParameters(n)


if __name__ == "__main__":
    initialize_dlp_for_EC(10)
