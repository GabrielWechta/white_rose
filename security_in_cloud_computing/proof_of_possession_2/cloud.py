from common_protocol import Responder
from klib import jload
from mcl_utils import get_G, mcl_sum, Fr, G1
from parser import parse_args
from proof_of_possession_2.proof_of_possession_2_utils import GROUP, psi_Fr


class Cloud(Responder):
    def __init__(self, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Responder.__init__(self, ip, port)
        self.file = None
        self.sigmas = []
        self.k = None
        self.mu = None
        self.sigma = None
        self.rs = None

    def set_file(self, file):
        self.file = file

    def set_sigmas(self, sigmas):
        self.sigmas = sigmas

    def set_k(self, k):
        self.k = k

    def produce_rs(self):
        self.rs = [psi_Fr(k=self.k, j=j) for j in range(len(self.file))]

    def produce_sigma(self):
        sigma_elements = [sig * r for sig, r in zip(self.sigmas, self.rs)]
        sigma = mcl_sum(li=sigma_elements)
        return sigma

    def produce_mu(self):
        mu_elements = [r * b for r, b in zip(self.rs, self.file)]
        mu = mcl_sum(li=mu_elements)
        return mu


def main():
    args = parse_args()
    cloud = Cloud(ip=args.ip, port=args.port)

    F_sigmas_k_ = cloud.receive_message()
    F_sigmas_k = jload({"F": [Fr], "sigma": [G1], "k": Fr}, F_sigmas_k_, True)
    file = F_sigmas_k["F"]
    sigmas = F_sigmas_k["sigma"]
    k = F_sigmas_k["k"]

    client.set_file(file=generate_file(part_num=m), file_id="Zdjecia_z_Chorwacji_2012")
    client.store_sigmas()
    client.produce_k_and_rs()

    file = client.get_file()
    sigmas = client.get_sigmas()
    k = client.get_k()
    client.send_message(message=jstore({"F": file, "sigma": sigmas, "k": k}))


if __name__ == "__main__":
    main()
