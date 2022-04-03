import random

from sympy import isprime, nextprime


def order(element, prime):
    for power in range(1, prime):
        if (element ** power) % p == 1:
            return power


def f(x, a, b, p, q, g, y):
    if x % 3 == 1:
        x_new = (x * g) % p
        a_new = (a + 1) % q
        b_new = b
    elif x % 3 == 2:
        x_new = (x * x) % p
        a_new = (2 * a) % q
        b_new = (2 * b) % q
    else:
        x_new = (x * y) % p
        a_new = a
        b_new = (b + 1) % q

    return x_new, a_new, b_new


def pollard_rho(g, y, p, Alpha=0, Beta=0, q=None):
    if g == y: return 1

    T = pow(g, Alpha, p) * pow(y, Beta, p) % p
    if q is None:  # if q is not passed, order is calculated via order func
        q = order(g, p)

    i = 0
    # initializing constant values for Pollard Rho Algorithm
    H, Gamma, Zeta = T, Alpha, Beta
    while True:
        T, Alpha, Beta = f(T, Alpha, Beta, p, q, g, y)
        H, Gamma, Zeta = f(*f(H, Gamma, Zeta, p, q, g, y), p, q, g, y)
        i += 1
        # print(f"{T=}, {Alpha=}, {Beta=}")
        # print(f"{H=}, {Gamma=}, {Zeta=}")
        # print()
        if T % p == H % p:
            if Zeta % q != Beta % q:
                x = (Alpha - Gamma) * pow(Zeta - Beta, -1, q) % q
                return x, i
            else:
                print("Change Alpha and Beta")
                return


def initialize_dlp(n):
    # idea of initializing values for hard dlp
    bottom_number = pow(2, n - 1) + 1

    # generating p
    while True:
        p_dash = nextprime(bottom_number)
        p = 2 * p_dash + 1
        if isprime(p):
            break
        else:
            bottom_number = p_dash
    # generating g
    while True:
        g = random.randint(2, p - 1)
        g_dash = pow(g, 2, p)
        if g_dash % p != 1:
            break

    print(f"{bottom_number=}, {p_dash=}, {p=}, {g_dash=}, {g=}")

    return p_dash, p, g_dash, g


# if __name__ == "__main__":
#     for i in range(2, 40):
#         print(i)
#         p_dash, p, g_dash, g = initialize_dlp(i)
#         x_to_solve = random.randint(2, p_dash)
#         y = pow(g_dash, x_to_solve, p)
#         x = pollard_rho(g=g_dash, y=y, p=p, q=p_dash)
#         print(f"{x_to_solve=}, {x=}, {g_dash=}, {y=}, {p=}, g^x = {pow(g_dash, x, p)}")
#         print()

if __name__ == "__main__":
    p_dash, p, g_dash, g = initialize_dlp(30)
    x_to_solve = random.randint(2, p_dash)
    y = pow(g_dash, x_to_solve, p)
    x, iter_num = pollard_rho(g=g_dash, y=y, p=p, q=p_dash)
    print(f"{x_to_solve=}, {x=}, {g_dash=}, {y=}, {p=}, g^x = {pow(g_dash, x, p)}, {iter_num=}")
