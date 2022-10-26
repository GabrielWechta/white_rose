from common_protocol import Responder
from mcl_utils import get_Fr, get_G1, jstore, jload, G1, Fr, monitor_func
from proof_of_possession.proof_of_possession_utils import \
    lagrangian_interpolation

HOSTNAME = "localhost"
PORT = 15000


class Cloud(Responder):
    def __init__(self, ip: str, port: int):
        # super().__init__(ip, port)
        self.H = None
        self.tag_block_dict = None
        self.proof_block_dict = {}
        self.g_r = None
        self.x_c = None
        self.ordinate_0 = None
        self.P = None

    @monitor_func
    def receive_tagged_block(self, T):
        self.tag_block_dict = T

    @monitor_func
    def receive_challenge(self, H):
        self.H = H
        self.g_r, self.x_c, self.ordinate_0 = H

    @monitor_func
    def gen_proof(self):
        for key, m_t_dict in self.tag_block_dict.items():
            ordinate = self.g_r * m_t_dict["t"]
            self.proof_block_dict[key] = {"abscissa": m_t_dict["m"], "ordinate":ordinate}
        self.proof_block_dict[len(self.proof_block_dict)] = {"abscissa": get_Fr(0), "ordinate":self.ordinate_0}
        self.P = lagrangian_interpolation(x=self.x_c, abscissa_ordinate_dict=self.proof_block_dict)
        return self.P



def main():
    ...


if __name__ == "__main__":
    main()
