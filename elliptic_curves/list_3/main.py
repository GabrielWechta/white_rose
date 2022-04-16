import random
import sympy


def initialize_problem(s_exponent: int, t: int):
    iter_count = 0
    while True:
        iter_count += 1
        s = random.randint(2 ** s_exponent + 1, 2 ** (s_exponent + 1) - 1)
        if s % 2 == 0:
            s += 1
        p = 2 ** t * s + 1

        if sympy.isprime(p):
            p_binary = "{0:b}".format(p)
            print(f"It took: {iter_count} iter, to generate prime {p=},\t{p_binary}")
            return p


def initialize_quadratic_residue(p: int):
    r = random.randint(1, p - 1)
    n = pow(r, 2, p)
    print(f"Square root to guess: {r=}")
    print(f"Corresponding square: {n=}")
    print(f" Such as {((r ** 2) % p)=}")

    return r, n


def find_quadratic_non_residue(p: int):
    iter_count = 0
    a = random.randint(1, p - 1)
    while pow(a, (p - 1) // 2, p) == 1 % p:
        iter_count += 1
        a = random.randint(1, p - 1)

    assert pow(a, (p - 1) // 2, p) == -1 % p
    print(f"It took: {iter_count} iter, to find QNR {a=}")
    return a


def main():
    p = initialize_problem(s_exponent=99, t=150)
    r_to_guess, n = initialize_quadratic_residue(p=p)
    a = find_quadratic_non_residue(p=p)


if __name__ == "__main__":
    main()
