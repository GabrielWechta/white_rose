import sys
from hashlib import sha256

sys.path.insert(1, '/home/gabriel/opt/mcl-python')

from mcl import Fr, G1, G2


def get_Fr(value=None):
    fr = Fr()
    if value is None:
        fr.setByCSPRNG()
    else:
        fr.setInt(value)
    return fr


class Polynomial:
    def __init__(self, coefficients=None):
        if coefficients is None:
            coefficients = []

        self.coefficients = coefficients

    def __call__(self, x):
        pol_val = get_Fr(0)
        for i, a in enumerate(self.coefficients):
            exponent = get_Fr(len(self.coefficients) - i - 1)
            pol_val += a * x ** exponent
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
