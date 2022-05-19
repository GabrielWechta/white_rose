import math
from copy import deepcopy


def cutr(string: str, n: int, sups: str = 'x'):
    if n > len(string):
        return "", '' * (n - len(string)) + string
    else:
        cut = string[-n:]
        remain = string[:-n]
        return remain, cut


class CombMethod:
    def __init__(self, g, e):
        self.g = g
        self.e = e
        # self.e_bin = '11001100101'
        self.e_bin = format(self.e, 'b')
        self.l = len(self.e_bin)

        self.a = 4
        self.b = 2

        self.h = math.ceil(self.l / self.a)
        self.v = math.ceil(self.a / self.b)

        self.a_last = self.l - self.a * (self.h - 1)
        self.v_last = math.ceil(self.a_last / self.b)
        self.b_last = self.a_last - self.b * (self.v_last - 1)

        self.E = self.create_E_matrix()
        self.G = self.create_G_matrix()

        self.show_E()

    def describe(self):
        print(f"{self.g=}")
        print(f"{self.e_bin=}")
        print(f"{self.l=}")
        print(f"{self.a=}")
        print(f"{self.b=}")
        print(f"{self.h=}")
        print(f"{self.v=}")
        print(f"{self.a_last=}")
        print(f"{self.v_last=}")
        print(f"{self.b_last=}")

    #  E Matrix ##############################################################
    def create_E_matrix(self):
        E = [[0 for j in range(self.v)] for i in range(self.h)]
        e_bin = deepcopy(self.e_bin)

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

        return E

    def show_E(self):
        # print(f"{self.e_bin=}")
        for row in self.E:
            for column in reversed(row):
                print(column, end=" ")
            print()

    #  G Matrix ##############################################################
    def get_r_array(self):
        r_array = [self.g ** (2 ** (i * self.a)) for i in range(self.h)]
        r_array.reverse()
        return r_array

    def matmul(self, l_arr, r_arr):
        s = 1
        for l, r in zip(l_arr, r_arr):
            s *= r ** l

        return s

    def create_G_matrix(self):
        r_array = self.get_r_array()
        # print(r_array)

        G = [[1 for i in range(2 ** self.h)] for j in range(self.v)]
        for u in range(1, 2 ** self.h):
            u_bin = format(u, f"0{self.h}b")
            u_bin_array = [int(bit) for bit in u_bin]
            cell_value = self.matmul(u_bin_array, r_array)
            # print(u_bin_array)
            # print(cell_value)
            # print()
            G[0][u] = cell_value
            for j in range(1, self.v):
                # print(2 ** (j * self.b))
                G[j][u] = cell_value ** (2 ** (j * self.b))
        # G = [[0 for x in range(v)] for y in range(2 ** h)]
        # pprint(G)
        return G

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

    def exponentiation(self):
        R = 1
        for k in range(self.b - 1, -1, -1):
            R = R ** 2
            for j in range(self.v - 1, -1, -1):
                I_jk = self.get_I(j=j, k=k)
                G_ijk = self.G[j][I_jk]
                R = R * G_ijk
        return R


def main():
    for e in range(1, 20):
        print(f"g=2, {e=}")
        comb_method = CombMethod(g=3, e=e)
        result = comb_method.exponentiation()
        print(result)
        print()

    # comb_method = CombMethod(g=2, e=16)
    # result = comb_method.exponentiation()
    # print(result)


if __name__ == "__main__":
    main()
