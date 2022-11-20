from hashlib import sha256
from typing import overload
from collections import Counter
from mcl_utils import Fr, get_Fr, get_G1, G1, pow_Fr


def lagrangian_interpolation_list(x, abscissa_ordinate_list):
    abscissas = [el[0] for el in abscissa_ordinate_list]
    seen = []
    for abscissa in abscissas:
        if abscissa not in seen:
            seen.append(abscissa)

    assert len(seen) == len(abscissas), "There are recurring abscissas in Interpolation set."
    main_sum = G1()
    for i, (x_i, ordinate_i) in enumerate(abscissa_ordinate_list):
        exp_product_i = get_Fr(1)
        for j, (x_j, _) in enumerate(abscissa_ordinate_list):
            if i == j:
                continue
            exp_product_i *= (x - x_j) / (x_i - x_j)
        main_sum += ordinate_i * exp_product_i
    return main_sum


def lagrangian_interpolation_dict(x, abscissa_ordinate_dict):
    main_sum = G1()
    for i, abscissa_ordinate_i in abscissa_ordinate_dict.items():
        x_i = abscissa_ordinate_i["abscissa"]
        ordinate_i = abscissa_ordinate_i["ordinate"]
        exp_product_i = get_Fr(1)
        for j, abscissa_ordinate_j in abscissa_ordinate_dict.items():
            if i == j:
                continue
            x_j = abscissa_ordinate_j["abscissa"]
            exp_product_i *= (x - x_j) / (x_i - x_j)
        main_sum += ordinate_i * exp_product_i
    return main_sum


class Polynomial:
    def __init__(self, coefficients=None):
        if coefficients is None:
            coefficients = []

        self.coefficients = coefficients

    def __call__(self, x):
        pol_val = get_Fr(0)
        for i, a in enumerate(self.coefficients):
            exponent = len(self.coefficients) - i - 1
            pol_val += a * pow_Fr(fr=x, exp=exponent)
        return pol_val

    def __contains__(self, item):
        return item in self.coefficients


class PoPInitGenerator:
    def __init__(self, z, f):
        secret_key, polynomial = self.setup(z, f)
        while get_Fr(0) in polynomial:  # avoiding possibility of a_i = 0
            secret_key, polynomial = self.setup(z, f)
        self.secret_key = secret_key
        self.polynomial = polynomial

    def setup(self, z, f):
        coefficients = []
        secret_key = get_Fr()
        f_id = sha256(f.encode('UTF-8')).digest()
        for i in range(z + 1):
            a = Fr.setHashOf(
                (str(secret_key) + str(f_id) + str(i)).encode('UTF-8'))
            coefficients.append(a)
        polynomial = Polynomial(coefficients=coefficients)
        return secret_key, polynomial


def main():
    with open("block.txt", "r") as file:
        f = file.readlines()
    z = 6
    popig = PoPInitGenerator(z=z, f=str(f))


if __name__ == "__main__":
    main()
