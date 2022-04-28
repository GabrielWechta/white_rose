from copy import deepcopy


class ProjectiveEllipticCurvePoint:
    def __init__(self, X: int = None, Y: int = None, Z: int = None,
                 p: int = None, A: int = None):
        self.X = X
        self.Y = Y
        self.Z = Z

        self.p = p
        self.A = A

    @staticmethod
    def create(X: int = None, Y: int = None, Z: int = None,
               p: int = None, A: int = None):
        if X == 0 and Z == 0:
            if Y != 0:
                return ProjectiveZeroAtInfinity(p=p, A=A)
            else:
                raise ValueError
        else:
            return ProjectiveEllipticCurvePoint(X=X, Y=Y, Z=Z, p=p, A=A)

    def __eq__(self, other: 'ProjectiveEllipticCurvePoint'):
        if isinstance(self, ProjectiveZeroAtInfinity) or \
                isinstance(other, ProjectiveZeroAtInfinity):
            return isinstance(self, ProjectiveZeroAtInfinity) and \
                   isinstance(other, ProjectiveZeroAtInfinity)
        else:
            return (self.X * self.Z) % self.p == (
                    other.X * other.Z) % self.p and (
                           self.Y * self.Z) % self.p == (
                           other.Y * other.Z) % self.p

    def __add__(self, other: 'ProjectiveEllipticCurvePoint'):
        if isinstance(self, ProjectiveZeroAtInfinity):
            return other

        if isinstance(other, ProjectiveZeroAtInfinity):
            return self

        A, p = self.A, self.p
        X_1, X_2 = self.X, other.X
        Y_1, Y_2 = self.Y, other.Y
        Z_1, Z_2 = self.Z, other.Z

        U_1 = (X_1 * Z_2) % p
        U_2 = (X_2 * Z_1) % p
        S_1 = (Y_1 * Z_2) % p
        S_2 = (Y_2 * Z_1) % p

        if U_1 == U_2:
            if S_1 == S_2:  # doubling
                W = (3 * pow(X_1, 2, p) + A * pow(Z_1, 2, p)) % p
                S = (2 * Y_1 * Z_1) % p
                B = (2 * S * X_1 * Y_1) % p
                h = (pow(W, 2, p) - 2 * B) % p

                X_3 = (h * S) % p
                Y_3 = (W * (B - h) - 2 * pow(S * Y_1, 2, p)) % p
                Z_3 = pow(S, 3, p)
                return ProjectiveEllipticCurvePoint(X=X_3, Y=Y_3, Z=Z_3, p=p,
                                                    A=A)
            else:
                return ProjectiveZeroAtInfinity()

        else:  # normal addition
            W = (Z_1 * Z_2) % p
            P = (U_2 - U_1) % p
            R = (S_2 - S_1) % p

            X_3 = (P * (W * pow(R, 2, p) - (U_1 + U_2) * pow(P, 2, p))) % p
            Y_3 = ((R * (3 * (U_1 + U_2) * pow(P, 2, p) - 2 * W * pow(R, 2, p))
                    - (S_1 + S_2) * pow(P, 3, p)) * pow(2, -1, p)) % p
            Z_3 = (pow(P, 3, p) * W) % p
            return ProjectiveEllipticCurvePoint(X=X_3, Y=Y_3,
                                                Z=Z_3, p=p, A=A)

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
        print(f"{name}({self.X}: {self.Y}: {self.Z})")


class ProjectiveZeroAtInfinity(ProjectiveEllipticCurvePoint):
    def __init__(self, p: int = None, A: int = None):
        super().__init__(X=0, Y=1, Z=0, p=p, A=A)

    def __add__(self, other: 'ProjectiveEllipticCurvePoint'):
        return other

    def show(self, name=""):
        print(f"{name}(\u221e)")


if __name__ == "__main__":
    P_1 = ProjectiveEllipticCurvePoint.create(X=3, Y=2, Z=1, p=5, A=1)
    P_1.show("P_1")
    P_2 = ProjectiveEllipticCurvePoint.create(X=0, Y=4, Z=0, p=5, A=1)
    P_2.show("P_2")
    P_3 = (P_2 + P_2)
    P_3.show("P_3")
    Z = ProjectiveZeroAtInfinity()
    P_1_2 = P_1 + P_1
    P_1_2.show("P_1_2")
    P_1_2_Z = P_1_2 + Z
    P_1_2_Z.show("P_1_2_Z")

    P = ProjectiveEllipticCurvePoint.create(X=3, Y=2, Z=1, p=5, A=1)
    Q = ProjectiveEllipticCurvePoint.create(X=1, Y=3, Z=2, p=5, A=1)
    assert 2 * P + 3 * P == 2 * 2 * P + 1
    assert 2 * P + 2 * Q == 2 * (P + Q)
