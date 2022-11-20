from hashlib import sha256

from broadcast_encryption.broadcast_encryption_utils import lagrangian_interpolation
from common_protocol import Initiator
from mcl_utils import get_Fr, Fr, monitor_func, get_G1
from proof_of_possession.proof_of_possession_utils import Polynomial

HOSTNAME = "localhost"
PORT = 15002


def split_gen(l, z):
    k, m = divmod(len(l), z)
    return (l[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(z))


class User(Initiator):
    def __init__(self, g, ip: str = None, port: int = None):
        # super().__init__(ip, port)
        self.g = g
        self.g_r = None
        self.x_c = None
        self.x_user = None
        self.y_user = None
        self.polynomial = None
        self.K = None
        self.phi = None
        self.I = None

    @monitor_func
    def receive_register_response(self, x, y):
        self.x_user = x
        self.y_user = y

    @monitor_func
    def generate_fresh_K(self):
        self.I = self.phi
        ordinate = self.g_r * self.y_user
        self.I[len(self.I)] = {"abscissa": self.x_user, "ordinate": ordinate}
        self.polynomial = lagrangian_interpolation(x=self.x_c, abscissa_ordinate_dict=self.I)


def main():
    ...


if __name__ == "__main__":
    main()
