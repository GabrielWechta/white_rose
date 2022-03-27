from copy import deepcopy


class EllipticCurvePoint:
    def __init__(self, x: int = None, y: int = None, p: int = None, A: int = None):
        self.x = x
        self.y = y
        self.p = p
        self.A = A

    def __eq__(self, other: 'EllipticCurvePoint'):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __add__(self, other: 'EllipticCurvePoint'):
        if isinstance(other, ZeroAtInfinity):
            return ZeroAtInfinity()

        x_1, y_1 = self.x, self.y
        x_2, y_2 = other.x, other.y
        p, A = self.p, self.A

        if x_1 == x_2 and y_1 != y_2:
            return ZeroAtInfinity()

        if self == other and y_1 == 0:
            return ZeroAtInfinity()

        if x_1 != x_2:
            m = ((y_2 - y_1) * pow(x_2 - x_1, -1, p)) % p
            x_3 = (pow(m, 2, p) - x_1 - x_2) % p
            y_3 = (m * (x_1 - x_3) - y_1) % p
            return EllipticCurvePoint(x=x_3, y=y_3, p=p, A=A)

        if self == other and y_1 != 0:
            m = ((3 * pow(x_1, 2, p) + A) * pow(2 * y_1, -1, p)) % p
            x_3 = (pow(m, 2, p) - 2 * x_1) % p
            y_3 = (m * (x_1 - x_3) - y_1) % p
            return EllipticCurvePoint(x=x_3, y=y_3, p=p, A=A)

    def __rmul__(self, other: int):
        if other == 0:
            return ZeroAtInfinity()

        product = deepcopy(self)
        bin_rep = bin(other)[3:]  # cutting '0b1' from value
        for bit in bin_rep:
            product = product + product
            if bit == '1':
                product = product + self

        return product

    def show(self, name=""):
        print(f"{name}({self.x}, {self.y})")


class ZeroAtInfinity(EllipticCurvePoint):
    def __init__(self):
        super().__init__()

    def __add__(self, other: 'EllipticCurvePoint'):
        return other

    def show(self, name=""):
        print(f"{name}(\u221e)")


if __name__ == "__main__":
    P_1 = EllipticCurvePoint(x=3, y=1, p=5, A=1)
    P_2 = EllipticCurvePoint(x=2, y=0, p=5, A=1)
    P_3 = 2 * (P_1 + P_2)
    P_3.show("P_3")
    D = ZeroAtInfinity()
    B = P_2 + P_2
    B.show("B")
