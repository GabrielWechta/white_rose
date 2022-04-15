"""Pretty nice code, absolutely not useful"""
import math
import random

import numpy
import numpy as np


class Knapsack:
    def __init__(self, n: int):
        self.n = n
        self.m = random.randint(2 ** (n + 1) + 1, 2 ** (2 * (n + 1)) - 1)  # TODO maybe two primes here?
        self.w_prim = random.randint(2, self.m - 2)
        self.w = self.w_prim // math.gcd(self.w_prim, self.m)
        self.a_prim = self.generate_knapsack_vector()
        self.a = numpy.mod(self.a_prim * self.w, self.m)
        self.x = numpy.random.choice(2, n)  # random bool vector

    def generate_knapsack_vector(self):
        knap_vec = np.zeros(self.n)
        knap_sum = 0
        for i in range(self.n):
            a = random.randint(((2 ** i) - 1) * (2 ** self.n) + 1, (2 ** i) * (2 ** self.n))
            knap_vec[i] = a
            assert knap_sum < a, f"{knap_sum=}, {a=}"
            knap_sum += a
        return knap_vec

    def __str__(self):
        return str(vars(self))
