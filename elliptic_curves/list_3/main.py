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
            print(
                f"It took: {iter_count} iter, to generate prime {p=},\t{p_binary}")
            return p, s


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
    while is_quadratic_residue(a, p):
        iter_count += 1
        a = random.randint(1, p - 1)

    assert pow(a, (p - 1) // 2, p) == -1 % p
    print(f"It took: {iter_count} iter, to find QNR {a=}")
    return a


def is_quadratic_residue(n: int, p: int):
    if n % p == 0 or pow(n, (p - 1) // 2, p) == 1:
        return True
    else:
        return False


def find_i_squaring(t: int, p: int):
    i = 0
    t_temp = t
    while t_temp != 1:
        i += 1
        t_temp = pow(t_temp, 2, p)

    return i


def find_square_root(n: int, S: int, Q: int, z: int, p: int):
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)

    M = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    R = pow(n, (Q + 1) // 2, p)

    if t == 0:
        return 0

    counter = 0
    while True:
        if t == 1:
            print(f"It took {counter} iter, to find Solution:")
            return R

        i = find_i_squaring(t=t, p=p)

        b = pow(c, pow(2, M - i - 1), p)
        M = i
        c = pow(b, 2, p)
        t = (t * c) % p
        R = (R * b) % p
        counter += 1


def main():
    S = 150
    p, Q, = initialize_problem(s_exponent=99, t=S)
    r_to_guess, n = initialize_quadratic_residue(p=p)
    z = find_quadratic_non_residue(p=p)
    r = find_square_root(n=n, p=p, Q=Q, S=S, z=z)
    print(f"{r=}")
    print(f"{n=}")
    print(f"x={(r ** 2) % p}")


if __name__ == "__main__":
    main()
