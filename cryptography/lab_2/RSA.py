import math
import random
from sympy import randprime


class RSA:

    def __init__(self, bit_length):
        self.p = randprime(2 ** bit_length, 2 ** (bit_length + 1))
        self.q = randprime(2 ** bit_length, 2 ** (bit_length + 1))
        self.N = self.p * self.q

        fi = (self.p - 1) * (self.q - 1)
        self.e = 2 ** 16 + 1
        self.d = pow(self.e, -1, fi)

        self.d_bin = list(map(int, "{0:b}".format(self.d)))
        self.e_bin = list(map(int, "{0:b}".format(self.e)))

    def get_public_key(self):
        return self.N, self.e

    def enc(self, m):
        return pow(m, self.e, self.N)

    def dec(self, c):
        return self.fast_pow(c, self.d_bin)

    def blind_dec(self, c):
        # c = (m * r)^e
        # c_2 = (m * r)^e % N
        # c_3 = c_2^d
        # m_r = (c_3) % N = c_2^d % N = (m * r)^ed % N = m * r % N =
        # c_2, r_1 = self.mod_reduce(c)
        c_3, r_2 = self.fast_pow(c, self.d_bin)
        print(f'{c=} {c_3=}')
        m_r, r_3 = self.mod_reduce(c_3)
        print(f'{r_2=} {r_3=}')

        return m_r,  r_2 + r_3

    def get_random_element(self, left=0, right=0):
        if left == 0 and right == 0:
            r = random.randrange(2, self.N)
            while math.gcd(r, self.N) != 1:
                r = random.randrange(2, self.N)
            return r
        else:
            r = random.randrange(left, right)
            while math.gcd(r, self.N) != 1:
                r = random.randrange(left, right)
            return r

    def mod_reduce(self, a):
        reduction = 0
        if a >= self.N:
            a = a % self.N
            reduction = 1
        return a, reduction

    def fast_pow(self, c, bits, n=0):
        bits_work = bits[1:] if n == 0 else bits[1:n]

        reductions = 0
        x = c

        for b in bits_work:
            x, r = self.mod_reduce(x ** 2)
            reductions += r

            if b == 1:
                x, r = self.mod_reduce(x * c)
                reductions += r

        if n == 0:
            return x, reductions
        else:
            x, r = self.mod_reduce(x ** 2)
            reductions += r

            x, r = self.mod_reduce(x * c)
            reductions += r

            return x, reductions

    def power_at_bit(self, bit):
        p = 1

        for b in self.d_bin[1:bit]:
            p *= 2
            if b == 1:
                p += 1

        # Always assuming that the last bit is 1
        p = p * 2 + 1
        return p

    def check_if_will_reduce(self, c, bit):
        x = c

        # check if c will reduce at final bit
        for b in self.d_bin[1:bit]:
            x, r = self.mod_reduce(x ** 2)

            if b == 1:
                x, r = self.mod_reduce(x * c)

        x, r = self.mod_reduce(x ** 2)
        x, r = self.mod_reduce(x * c)
        return r > 0

    def sign(self, m):
        return pow(m, self.d, self.N)

    def verify(self, m, s):
        return m == pow(s, self.e, self.N)

    def dec_partial(self, c, bit):
        return self.fast_pow(c, self.d_bin, n=bit)

    def compare_exponents(self, d_bin):
        correct = 0
        print("[", end="")

        for i, (b, true_b) in enumerate(zip(d_bin, self.d_bin)):
            if b == true_b:
                print(f'{b}', end="")
                correct += 1
            else:
                print(f'{b}*', end="")

            if i != len(d_bin) - 1:
                print(", ", end="")

        print(f"] -> {(correct / len(d_bin)) * 100}%")

        return correct / len(d_bin)
