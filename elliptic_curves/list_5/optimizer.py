import math

class CombMethodOptimizer:
    def __init__(self, l, S):
        self.l = l
        self.S = S

        self.a = None
        self.b = None
        self.h = None
        self.v = None
        self.a_last = None
        self.v_last = None
        self.b_last = None

        self.best = {"P": float('Inf'),
                     "a": 0,
                     "b": 0
                     }

    def update_a_b(self, a, b):
        self.a = a
        self.b = b

        self.h = math.ceil(self.l / self.a)
        self.v = math.ceil(self.a / self.b)

        self.a_last = self.l - self.a * (self.h - 1)
        self.v_last = math.ceil(self.a_last / self.b)
        self.b_last = self.a_last - self.b * (self.v_last - 1)

    def start_search(self):
        for a in range(1, 10000):
            for b in range(1, 10000):
                self.update_a_b(a=a, b=b)

                if self.get_number_of_elements_in_G() > self.S:
                    break

                P = self.average_computation_cost()
                if self.best["P"] > P:
                    self.best["P"] = P
                    self.best["a"] = a
                    self.best["b"] = b

    def get_number_of_elements_in_G(self):
        # return (2 ** self.h) * self.v
        return ((2 ** self.h) - 1) * self.v + ((2 ** (self.h - 1)) - 1) * (
                self.v - self.v_last)

    def average_computation_cost(self):
        multiplication_cost = (((2 ** (self.h - 1)) - 1) / (2 ** (self.h - 1))) * (
                    self.a - self.a_last) + (((2 ** (self.h)) - 1) / (2 ** (self.h))) * (
                                          self.a_last - 1)
        squaring_cost = self.b - 1

        # cost from the paper - not good
        # P = self.a * (self.h - 1) + self.b * (self.v_last - 1) + self.v * (
        #         2 ** (self.h - 1) - self.h) + self.v_last * (
        #             2 ** (self.h - 1) - 1)
        # return P

        return multiplication_cost + squaring_cost

    def get_best(self):
        return self.best
