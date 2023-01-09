import hashlib

from mcl_utils import get_Fr, pow_Fr, Fr, G2

GROUP = G2
HASH_CLS = hashlib.sha256


def bytes_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


BYTES_XOR = bytes_xor


def lagrangian_interpolation_list(x, abscissa_ordinate_list):
    abscissas = [el[0] for el in abscissa_ordinate_list]
    seen = []
    for abscissa in abscissas:
        if abscissa not in seen:
            seen.append(abscissa)

    assert len(seen) == len(abscissas), "There are recurring abscissas in Interpolation set."
    main_sum = get_Fr(0)
    for i, (x_i, ordinate_i) in enumerate(abscissa_ordinate_list):
        exp_product_i = get_Fr(1)
        for j, (x_j, _) in enumerate(abscissa_ordinate_list):
            if i == j:
                continue
            exp_product_i *= (x - x_j) / (x_i - x_j)
        main_sum += ordinate_i * exp_product_i

    return main_sum


class Polynomial:
    def __init__(self, degree: int, coefficient_0_0: int = None):
        coefficients = [get_Fr() for _ in range(degree + 1)]
        if coefficient_0_0 is not None:
            coefficients[-1] = get_Fr(value=coefficient_0_0)
        self.coefficients = coefficients

    def __call__(self, x):
        pol_val = get_Fr(0)
        for i, a in enumerate(self.coefficients):
            exponent = len(self.coefficients) - i - 1
            pol_val += a * pow_Fr(fr=x, exp=exponent)
        return pol_val

    def __contains__(self, item):
        return item in self.coefficients

class ConnectedPolynomial:
    def __init__(self, A: Polynomial, O: Polynomial):
        self.A = A
        self.O = O

    def __call__(self, abscissa: Fr, ordinate: Fr):
        return self.A(abscissa) + self.O(ordinate)
