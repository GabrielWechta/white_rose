import math
from pprint import pprint

import numpy as np

import numpy


class CombMethod:
    def __init__(self):
        self.e = 122250
        self.h = 5
        print(f"{self.h=}")
        self.v = 2
        print(f"{self.v=}")
        self.g = 2
        print(f"{self.g=}")

        self.e_bin = format(self.e, 'b')
        print(f"{self.e_bin=}")
        self.l = len(self.e_bin)
        print(f"{self.l=}")
        self.a = math.ceil(self.l / self.h)
        print(f"{self.a=}")
        self.b = math.ceil(self.a / self.v)
        print(f"{self.b=}")

        self.E = self.create_exp_table()
        self.G = self.create_G_matrix()

    def create_exp_table(self):
        E = [[0 for j in range(self.v)] for i in range(self.h)]

        print(self.e_bin)
        e_bin = self.e_bin.rjust(self.a * self.h, '0')
        print(e_bin)
        for i in range(self.h):
            e_bin_i = e_bin[self.a * self.h - (
                    i + 1) * self.a:self.a * self.h - i * self.a]
            for j in range(self.v):
                e_bin_i_j = e_bin_i[self.b * self.v - (
                        j + 1) * self.b: self.b * self.v - j * self.b]
                E[i][j] = e_bin_i_j

        print(E)
        return E

    def get_I(self, j, k):
        I = 0
        for i in range(self.h):
            I += int(self.E[i][j][(self.b - 1) - k]) * 2 ** i
        return I

    def get_r_array(self):
        r_array = [self.g ** (2 ** (i * self.a)) for i in range(self.h)]
        r_array.reverse()
        return numpy.array(r_array)

    def create_G_matrix(self):
        r_array = self.get_r_array()
        print(r_array)

        G = [[0 for i in range(2 ** self.h)] for j in range(self.v)]
        for u in range(1, 2 ** self.h):
            u_bin = format(u, f"0{self.h}b")
            u_bin_array = numpy.array([int(bit) for bit in u_bin])
            cell_value = np.matmul(u_bin_array, r_array)
            print(u_bin_array)
            print(cell_value)
            print()
            G[0][u] = cell_value
            for j in range(1, self.v):
                print(2 ** (j * self.b))
                G[j][u] = cell_value ** (2 ** (j * self.b))
        # G = [[0 for x in range(v)] for y in range(2 ** h)]
        pprint(G)
        return G


def main():
    comb_method = CombMethod()


if __name__ == "__main__":
    main()
