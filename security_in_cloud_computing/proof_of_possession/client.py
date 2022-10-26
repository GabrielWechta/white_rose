from hashlib import sha256

from common_protocol import Initiator
from mcl_utils import get_Fr, Fr, monitor_func, get_G1
from proof_of_possession.proof_of_possession_utils import Polynomial

HOSTNAME = "localhost"
PORT = 15002


def split_gen(l, z):
    k, m = divmod(len(l), z)
    return (l[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(z))


class Client(Initiator):
    def __init__(self, z: int, ip: str = None, port: int = None):
        # super().__init__(ip, port)
        self.g = get_G1()
        self.z = z
        self.sk = None
        self.f_id = None
        self.tag_block_dict = {}
        self.polynomial = None
        self.all_m = []
        self.H = None
        self.K = None
        self.P = None

    @monitor_func
    def read_file_store_as_Fr(self, filepath: str):
        self.f_id = sha256(filepath.encode('UTF-8')).digest()

        with open(filepath, "r") as file:
            file_lines = file.readlines()

        split_list = list(split_gen(file_lines, self.z))

        for i, elements_list in enumerate(split_list):
            line = "".join(elements_list)
            m = Fr.setHashOf(line.encode('UTF-8'))
            self.all_m.append(m)
            self.tag_block_dict[i] = {"m": m, "t": None}

    @monitor_func
    def setup(self):
        self.sk = get_Fr()

    @monitor_func
    def poly(self):
        coefficients = []
        for i in range(self.z + 1):
            a = Fr.setHashOf(
                (str(self.sk) + str(self.f_id) + str(i)).encode('UTF-8'))
            coefficients.append(a)
        self.polynomial = Polynomial(coefficients=coefficients)

    @monitor_func
    def tag_block(self):
        for key, m_t_dict in self.tag_block_dict.items():
            m = m_t_dict["m"]
            t = self.polynomial(m)
            m_t_dict["t"] = t
        return self.tag_block_dict

    @monitor_func
    def gen_challenge(self):
        r = get_Fr()
        x_c = get_Fr()

        # make sure that x_c is not already in ms
        while x_c in self.all_m:
            x_c = get_Fr()

        self.K = self.g * (r * self.polynomial(x_c))
        self.H = (self.g * r, x_c, self.g * (r * self.polynomial(get_Fr(0))))
        return self.H

    @monitor_func
    def receive_proof(self, P):
        self.P = P

    @monitor_func
    def check_proof(self):
        if self.K == self.P:
            return "Proof of possession accepted."
        else:
            return "Proof of possession rejected."


def main():
    client = Client(z=6, ip=HOSTNAME, port=PORT)
    client.setup()
    client.read_file_store_as_Fr(filepath="block.txt")
    client.poly()
    T = client.tag_block()
    H = client.gen_challenge()

    return


if __name__ == "__main__":
    main()
