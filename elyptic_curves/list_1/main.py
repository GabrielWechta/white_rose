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


def pollard_rho(g, y, p, Alpha=0, Beta=0):
    if g == y: return 1

    T = pow(g, Alpha, p) * pow(y, Beta, p)
    q = order(g, p)
    print(f'{q=}')

    H, Gamma, Zeta = T, Alpha, Beta
    while True:
        T, Alpha, Beta = f(T, Alpha, Beta, p, q, g, y)
        H, Gamma, Zeta = f(*f(H, Gamma, Zeta, p, q, g, y), p, q, g, y)
        print(f"{T=}, {Alpha=}, {Beta=}")
        print(f"{H=}, {Gamma=}, {Zeta=}")
        print()
        if T % p == H % p:
            if Zeta % q != Beta % q:
                x = (Alpha - Gamma) * pow(Zeta - Beta, -1, q) % q
                return x
            else:
                print("Change Alpha and Beta")
                return


def test():

    strong_prime =


if __name__ == "__main__":
    test()