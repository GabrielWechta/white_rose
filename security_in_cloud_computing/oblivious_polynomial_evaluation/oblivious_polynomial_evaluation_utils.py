import hashlib

from mcl_utils import G1, get_Fr, std_concat_method, pow_Fr

GROUP = G1
HASH_CLS = hashlib.sha256


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

    def populate_randomly(self, degree: int, coefficient_0_0: bool):
        coefficients = [get_Fr() for _ in range(degree)]
        if coefficient_0_0 is True:
            coefficients[0] = get_Fr(value=0)
        return self.__init__(coefficients=coefficients)
