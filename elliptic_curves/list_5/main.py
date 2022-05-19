import functools
import math
from copy import deepcopy
from random import randrange

from Crypto.PublicKey import ECC
from sympy import randprime, isprime

from optimizer import CombMethodOptimizer
import operator


def cutr(string: str, n: int):
    if n > len(string):
        return "", '' * (n - len(string)) + string
    else:
        cut = string[-n:]
        remain = string[:-n]
        return remain, cut


class CombMethod:
    def __init__(self, a, b, l, S):
        self.l = l
        self.S = S

        self.a = a
        self.b = b

        self.h = math.ceil(self.l / self.a)
        self.v = math.ceil(self.a / self.b)

        self.a_last = self.l - self.a * (self.h - 1)
        self.v_last = math.ceil(self.a_last / self.b)
        self.b_last = self.a_last - self.b * (self.v_last - 1)

        self.E = None
        self.G = None

    def describe(self):
        print(f"{self.l=}")
        print(f"{self.a=}")
        print(f"{self.b=}")
        print(f"{self.h=}")
        print(f"{self.v=}")
        print(f"{self.a_last=}")
        print(f"{self.v_last=}")
        print(f"{self.b_last=}")

    #  E Matrix ##############################################################
    def create_E_matrix(self, e_bin):
        E = [[0 for j in range(self.v)] for i in range(self.h)]
        e_bin = deepcopy(e_bin)

        for i in range(self.h):
            if i != self.h - 1:
                e_bin, e_bin_i = cutr(e_bin, self.a)
            else:
                e_bin, e_bin_i = cutr(e_bin, self.a_last)

            for j in range(self.v):
                if i == self.h - 1 and j == self.v - 1:
                    e_bin_i, e_bin_i_j = cutr(e_bin_i, self.b_last)
                else:
                    e_bin_i, e_bin_i_j = cutr(e_bin_i, self.b)

                E[i][j] = e_bin_i_j

        self.E = E

    def show_E(self):
        # print(f"{self.e_bin=}")
        for row in self.E:
            for column in reversed(row):
                print(column, end=" ")
            print()

    #  G Matrix ##############################################################
    def precompute(self, g):
        self.create_G_matrix(g)

    def get_r_array(self, g):
        r_array = [g * (2 ** (i * self.a)) for i in range(self.h)]
        r_array.reverse()
        return r_array

    def matmul(self, l_arr, r_arr):
        return functools.reduce(operator.add,
                                map(lambda x, y: x * y, l_arr, r_arr))

    def create_G_matrix(self, g):
        r_array = self.get_r_array(g=g)
        G = [[1 for _ in range(2 ** self.h)] for _ in range(self.v)]

        for u in range(1, 2 ** self.h):
            u_bin = format(u, f"0{self.h}b")
            u_bin_array = [int(bit) for bit in u_bin]

            cell_value = self.matmul(u_bin_array, r_array)
            G[0][u] = cell_value

            for j in range(1, self.v):
                G[j][u] = cell_value * (2 ** (j * self.b))

        self.G = G

    #  Exponentiation ########################################################
    def get_I(self, j, k):
        I = 0
        for i in range(self.h):
            e_cell = self.E[i][j]

            if i < self.h - 1:
                if j < self.v - 1:
                    index = self.b - 1 - k
                if j == self.v - 1:
                    index = len(e_cell) - 1 - k

            if i == self.h - 1:
                if j < self.v_last - 1:
                    index = self.b - 1 - k
                if j == self.v_last - 1:
                    index = self.b_last - 1 - k
                if j > self.v_last - 1:
                    continue

            if index < 0:
                continue

            bit = e_cell[index]

            if bit == '0' or bit == '1':
                I += int(bit) * (2 ** i)
                # I += 2 ** i
        return I

    def exponentiation(self, e):
        e_bin = "{0:b}".format(e)
        self.create_E_matrix(e_bin=e_bin)

        R = ECC.EccPoint(0, 0,
                         curve="NIST P-521")  # neutral element of addition
        for k in range(self.b - 1, -1, -1):
            R = R.double()
            for j in range(self.v - 1, -1, -1):
                I_jk = self.get_I(j=j, k=k)
                if I_jk > 0:
                    G_ijk = self.G[j][I_jk]
                    R = R + G_ijk
        return R


def gen_prime(min, max):
    p = 0
    min_v = min
    max_v = max
    while not isprime(p):
        p = randprime(2 ** min_v, 2 ** max_v)
    return p


def search(l, S):
    comb_method_optimizer = CombMethodOptimizer(l=l, S=S)
    comb_method_optimizer.start_search()
    best = comb_method_optimizer.get_best()
    print(best)

    return best["a"], best["b"]


def main(e, a, b, S):
    g = ECC.generate(curve="NIST P-521").pointQ

    comb_method = CombMethod(a=a, b=b, l=e.bit_length(), S=S)
    comb_method.precompute(g=g)
    result = comb_method.exponentiation(e=e)

    print(f"{result.xy=}")
    print(f"{(g * e).xy=}")


def test(test_count, S_min, S_max, S_step):
    for S in range(S_min, S_max, S_step):
        for i in range(test_count):
            e = randrange(1, 2 ** 100)
            a, b = search(l=e.bit_length(), S=S)
            main(e=e, a=a, b=b)


if __name__ == "__main__":
    a, b = search()
    a = 10
    b = 3
    main(a, b)
