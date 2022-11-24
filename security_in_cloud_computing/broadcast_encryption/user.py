import hashlib
from hashlib import sha256

from broadcast_encryption import klib
from broadcast_encryption.broadcast_encryption_utils import lagrangian_interpolation_dict, \
    lagrangian_interpolation_list
from common_protocol import Initiator
from mcl_utils import get_Fr, Fr, monitor_func, get_G1, G1
from proof_of_possession.proof_of_possession_utils import Polynomial

HOSTNAME = "172.20.10.6"
PORT = 20016
USER_ID = 0


def split_gen(l, z):
    k, m = divmod(len(l), z)
    return (l[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(z))


class User(Initiator):
    def __init__(self, id, g, ip: str = None, port: int = None):
        super().__init__(ip, port)
        self.id = id
        self.g = g
        self.g_r = None
        self.x_c = None
        self.x_user = None
        self.y_user = None
        self.polynomial = None
        self.K = None
        self.phi = None
        self.I = []

    # @monitor_func
    def receive_register_response(self, x, y):
        self.x_user = x
        self.y_user = y

    # @monitor_func
    def receive_header(self, header):
        self.g_r, self.phi, self.x_c = header

    # @monitor_func
    def generate_fresh_K(self):
        self.I.extend(self.phi)
        ordinate = self.g_r * self.y_user
        self.I.append((self.x_user, ordinate))
        try:
            K = lagrangian_interpolation_list(x=self.x_c, abscissa_ordinate_list=self.I)
            print(K)
            print(f"User {self.id} computed {hashlib.sha256(K).hexdigest()=}.")
            print(f"User {self.id} computed {hashlib.sha256(bytes(str(K), 'UTF-8')).hexdigest()=}.")

        except AssertionError:
            print(f"User {self.id} was not able to compute Lagrangian Interpolation.")
            return


def main():
    g = get_G1(b"Broadcast Encryption")
    user = User(id=USER_ID, g=g, ip=HOSTNAME, port=PORT)

    point_ = user.receive_message()
    x_user, y_user = klib.jload({"point": (Fr, Fr)}, point_, True)["point"]
    user.receive_register_response(x=x_user, y=y_user)

    header_ = user.receive_message()
    header = klib.jload({"H": (G1, [(Fr, G1)], Fr)}, header_, True)["H"]
    user.receive_header(header=header)
    user.generate_fresh_K()


if __name__ == "__main__":
    main()
