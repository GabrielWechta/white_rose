from broadcast_encryption.broadcast_encryption_utils import Polynomial
from common_protocol import Responder
from mcl_utils import get_Fr, get_G1, monitor_func, std_concat_method

HOSTNAME = "localhost"
PORT = 15000
CONCAT_METHOD = std_concat_method


class Broadcaster(Responder):
    def __init__(self, z: int, ip: str = None, port: int = None):
        # super().__init__(ip, port)
        self.sk = get_G1()
        self.z = z
        self.g = None
        self.polynomial = None
        self.phi = None

    @monitor_func
    def setup(self, g):
        self.g = g
        coefficients = []
        for i in range(self.z + 1):
            a_i = get_Fr(CONCAT_METHOD(self.sk, i))
            coefficients.append(a_i)
        self.polynomial = Polynomial(coefficients=coefficients)

    @monitor_func
    def register_user(self, i):
        x_i = get_Fr(CONCAT_METHOD(i, self.sk))
        y_i = Polynomial(x_i)
        return x_i, y_i

    @monitor_func
    def make_header(self, target_users_ids):
        phi = []
        r = get_Fr()
        for j in target_users_ids:
            x_j = get_Fr(CONCAT_METHOD(j, self.sk))
            y_j = self.g * (r * self.polynomial(x_j))
            phi.append((x_j, y_j))
        x_c = get_Fr()
        return self.g * r, phi, x_c


def main():
    ...


if __name__ == "__main__":
    main()
