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
        self.users_abscissa_dict = {}
        self.x_c = None

    @monitor_func
    def setup(self, g):
        self.g = g
        coefficients = []
        for i in range(self.z + 1):
            # a_i = get_Fr(CONCAT_METHOD(self.sk, i))
            a_i = get_Fr()
            coefficients.append(a_i)
        self.polynomial = Polynomial(coefficients=coefficients)

    @monitor_func
    def register_user(self, i):
        # x_i = get_Fr(CONCAT_METHOD(i, self.sk))
        x_i = get_Fr()
        y_i = self.polynomial(x_i)
        self.users_abscissa_dict[i] = x_i
        return x_i, y_i

    @monitor_func
    def make_header(self, excluded_users_ids):
        phi = []
        r = get_Fr()
        for j, abscissa in self.users_abscissa_dict.items():
            if j in excluded_users_ids:
                x_j = abscissa
            else:
                x_j = get_Fr()
            y_j = self.g * (r * self.polynomial(x_j))
            phi.append((x_j, y_j))
        self.x_c = get_Fr()
        return self.g * r, phi, self.x_c

    @monitor_func
    def calculate_fresh_K(self):
        K = self.polynomial(self.x_c)



def main():
    ...


if __name__ == "__main__":
    main()