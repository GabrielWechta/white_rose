from copy import deepcopy


class ProjectiveEllipticCurvePoint:
    def __init__(self, X: int = None, Y: int = None, Z: int = None,
                 p: int = None, A: int = None):
        self.X = X
        self.Y = Y
        self.Z = Z

        self.p = p
        self.A = A

    def __eq__(self, other: 'ProjectiveEllipticCurvePoint'):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __add__(self, other: 'ProjectiveEllipticCurvePoint'):
        if isinstance(self, ProjectiveZeroAtInfinity):
            return ProjectiveZeroAtInfinity()

        if isinstance(other, ProjectiveZeroAtInfinity):
            return ProjectiveZeroAtInfinity()

        A, p = self.A, self.p
        X_1, X_2 = self.X, other.X
        Y_1, Y_2 = self.Y, other.Y
        Z_1, Z_2 = self.Z, other.Z

        U_1 = (X_1 * Z_1) % p
        U_2 = (X_2 * Z_1) % p
        S_1 = (Y_1 * Z_1) % p
        S_2 = (Y_2 * Z_1) % p

        if U_1 == U_2 and S_1 == S_2:  # doubling
            W = (3 * pow(X_1, 2, p) + A * pow(Z_1, 2, p)) % p
            S = (2 * Y_1 * Z_1) % p
            B = (2 * S * X_1 * Y_1) % p
            h = (pow(W, 2, p) - 2 * B) % p

            X_3 = (h * S) % p
            Y_3 = (W * (B - h) - 2 * pow(S * Y_1, 2, p)) % p
            Z_3 = pow(S, 3, p)
            return ProjectiveEllipticCurvePoint(X=X_3, Y=Y_3, Z=Z_3)
        else:  # normal addition
            W = (Z_1 * Z_2) % p
            P = (U_2 - U_1) % p
            R = (S_2 - S_1) % p

            X_3 = (P * (W * pow(R, 2, p) - (U_1 + U_2) * pow(P, 2, p))) % p
            Y_3 = (R * (3 * (U_1 + U_2) * pow(P, 2, p) - 2 * W * pow(R, 2, p))
                   - (S_1 + S_2) * pow(P, 3, p)) % p
            Z_3 = (pow(P, 3, p) * W) % p
            return ProjectiveEllipticCurvePoint(X=2 * X_3, Y=2 * Y_3,
                                                Z=2 * Z_3)

    def __rmul__(self, other: int):
        if other == 0:
            return ProjectiveZeroAtInfinity()

        product = deepcopy(self)
        bin_rep = bin(other)[3:]  # cutting '0b1' from value
        for bit in bin_rep:
            product = product + product
            if bit == '1':
                product = product + self

        return product

    def show(self, name=""):
        print(f"{name}({self.X}, {self.Y}, {self.Y})")


class ProjectiveZeroAtInfinity(ProjectiveEllipticCurvePoint):
    def __init__(self):
        super().__init__()

    def __add__(self, other: 'ProjectiveEllipticCurvePoint'):
        return other

    def show(self, name=""):
        print(f"{name}(\u221e)")


if __name__ == "__main__":
    P_1 = ProjectiveEllipticCurvePoint(X=3, Y=2, Z=1, p=5, A=1)
    P_2 = ProjectiveEllipticCurvePoint(X=3, Y=0, Z=1, p=5, A=1)
    P_3 = (P_1 + P_2)
    P_3.show("P_3")
    D = ProjectiveZeroAtInfinity()
    B = P_2 + P_2
    B.show("B")
