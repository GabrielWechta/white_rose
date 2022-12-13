from hashlib import sha256

from common_protocol import Initiator
from mcl_utils import Fr, get_G
from parser import parse_args
from proof_of_possession_2.proof_of_possession_2_utils import GROUP


class Client(Initiator):
    def __init__(self, g: GROUP, n: int, m: int, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Initiator.__init__(self, ip, port)
        self.g = g
        self.n = n
        self.m = m
        

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

    def check_proof(self):
        if self.K == self.P:
            return "Proof of possession accepted."
        else:
            return "Proof of possession rejected."


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    client = Client(g=g, ip=args.ip, port=args.port)


if __name__ == "__main__":
    main()
