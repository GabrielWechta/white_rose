import random

from mcl_utils import get_Fr


class RandomnessSource():
    def __init__(self, seed):
        self.prng = random
        self.prng.seed(seed)
        self.toss = None

    def toss_randomness(self):
        self.toss = self.prng.randint(0, 2 ** 64)

    def get_toss(self):
        return self.toss


class HSM:
    def __init__(self, i: int, prng_1: RandomnessSource, prng_2: RandomnessSource):
        self.x_share = get_Fr()
        self.i = i
        self.prng_1 = prng_1
        self.prng_2 = prng_2
        self.reg_size = 64
        self.toss_1 = None
        self.toss_2 = None
        self.toss_sum = None

    def produce_tosses(self):
        self.toss_1 = self.prng_1.get_toss()
        self.toss_2 = self.prng_2.get_toss()
        self.toss_sum = (self.toss_1 + self.toss_2) % self.reg_size

    def get_private_key_share(self):
        if self.i == 1:
            self.x_share = self.pm(self.x_share, self.toss_sum)
        if self.i == 2:
            self.x_share = self.mp(self.x_share, self.toss_sum)
        if self.i == 3:
            self.x_share = self.pm(self.x_share, self.toss_sum)
        if self.i == 4:
            self.x_share = self.mp(self.x_share, self.toss_sum)

    def pm(self, a, b):
        if self.toss_sum % 2 == 0:
            return a + b
        else:
            return a - b

    def mp(self, a, b):
        if self.toss_sum % 2 == 0:
            return a - b
        else:
            return a + b

    def get_x_share(self):
        return self.x_share

    def show_tosses(self):
        print(f"{self.toss_1=}")
        print(f"{self.toss_2=}")


def main():
    prng_1 = RandomnessSource(seed=1)
    prng_2 = RandomnessSource(seed=2)
    hsm_1 = HSM(1, prng_1=prng_1, prng_2=prng_2)
    hsm_2 = HSM(2, prng_1=prng_1, prng_2=prng_2)
    prng_1.toss_randomness()
    prng_2.toss_randomness()
    hsm_1.produce_tosses()
    hsm_2.produce_tosses()
    hsm_1.show_tosses()
    hsm_2.show_tosses()


if __name__ == "__main__":
    main()
