import random

from EllipticCurve import EllipticCurvePoint
from main import initialize_dlp_for_ec, pollard_rho
from projective_elliptic_curve import ProjectiveEllipticCurvePoint
from matplotlib import pyplot as plt
from affine_main import pollard_rho_affine


def test_projective_ec(k_to_guess, A_coefficient, field_size, curve_order,
                       base_point):
    P_point = ProjectiveEllipticCurvePoint.create(X=base_point[0],
                                                  Y=base_point[1],
                                                  Z=base_point[2],
                                                  p=field_size,
                                                  A=A_coefficient)
    Q_point = k_to_guess * P_point
    k_solution, iter_num = pollard_rho(P=P_point, Q=Q_point,
                                       curve_order=curve_order)
    assert k_solution == k_to_guess
    return iter_num


def test_affine_ec(k_to_guess, A_coefficient, field_size, curve_order,
                   base_point):
    P_point = EllipticCurvePoint(x=base_point[0], y=base_point[1],
                                 p=field_size, A=A_coefficient)
    Q_point = k_to_guess * P_point
    k_solution, iter_num = pollard_rho_affine(P=P_point, Q=Q_point,
                                              curve_order=curve_order)

    assert k_solution == k_to_guess
    return iter_num


def main():
    n_arr, affine_iter_arr, projective_iter_arr = [], [], []
    for n in range(10, 20):
        n_arr.append(n)

        A_coefficient, B_coefficient, field_size, curve_order, base_point = initialize_dlp_for_ec(
            n)
        k_to_guess = random.randint(2, curve_order - 1)

        # affine
        affine_iter = test_affine_ec(k_to_guess, A_coefficient,
                                     field_size,
                                     curve_order, base_point)
        affine_iter_arr.append(affine_iter)

        # projective
        projective_iter = test_projective_ec(k_to_guess, A_coefficient,
                                             field_size,
                                             curve_order, base_point)
        projective_iter_arr.append(projective_iter)

    print(f"{affine_iter_arr=}")
    print(f"{projective_iter_arr=}")
    plt.scatter(n_arr, affine_iter_arr)
    plt.scatter(n_arr, projective_iter_arr)
    plt.show()
    plt.savefig("comparison.png")


if __name__ == "__main__":
    main()
