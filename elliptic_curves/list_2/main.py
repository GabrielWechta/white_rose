import math
import random

from EllipticCurve import EllipticCurvePoint
from ec_prime_order import generateDomainParameters


def f(R, a_scal, b_scal, P, Q, k_ord):
    if R.x % 3 == 1:
        R_new = R + P
        a_new = (a_scal + 1) % k_ord
        b_new = b_scal
    elif R.x % 3 == 2:
        R_new = 2 * R
        a_new = 2 * a_scal % k_ord
        b_new = 2 * b_scal % k_ord
    else:  # here goes also *zero at infinity*
        R_new = R + Q
        a_new = a_scal
        b_new = (b_scal + 1) % k_ord

    return R_new, a_new, b_new


def pollard_rho(P, Q, curve_order, Alpha=1, Beta=0):
    i = 0
    if P == Q:
        return 1, i

    T = Alpha * P
    H, Gamma, Zeta = T, Alpha, Beta
    while True:
        i += 1
        T, Alpha, Beta = f(T, Alpha, Beta, P, Q, curve_order)
        H, Gamma, Zeta = f(*f(H, Gamma, Zeta, P, Q, curve_order), P, Q, curve_order)
        if T == H:
            if math.gcd(Zeta - Beta, curve_order) == 1:
                k = (Alpha - Gamma) * pow(Zeta - Beta, -1, curve_order) % curve_order
                return k, i
            else:
                print("Change Alpha and Beta")
                return


def initialize_dlp_for_ec(bit_length: int):
    elliptic_curve, curve_order, base = generateDomainParameters(bit_length)
    ec_split = str(elliptic_curve).split(" ")
    A_coefficient = ec_split[8].split("*")[0]
    B_coefficient = ec_split[10]
    field_size = ec_split[-1]

    base = str(base)
    base_point = (int(base.split(" : ")[0].replace("(", "")), int(base.split(" : ")[1]))
    return int(A_coefficient), int(B_coefficient), int(field_size), int(curve_order), base_point


if __name__ == "__main__":
    A_coefficient, B_coefficient, field_size, curve_order, base_point = initialize_dlp_for_ec(40)
    k_to_guess = random.randint(2, curve_order - 1)
    P_point = EllipticCurvePoint(x=base_point[0], y=base_point[1], p=field_size, A=A_coefficient)
    Q_point = k_to_guess * P_point
    Q_point.show("Q_point")
    k_solution, iter_num = pollard_rho(P=P_point, Q=Q_point, curve_order=curve_order)
    print(f"P({P_point.x}, {P_point.y}), {k_to_guess=}, Q({Q_point.x}, {Q_point.y}), {k_solution=}, {iter_num=}")
