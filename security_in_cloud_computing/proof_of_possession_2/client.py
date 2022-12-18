from common_protocol import Initiator
from klib import jstore, jload
from mcl_utils import get_G, G2, G1, get_Fr, std_concat_method, mcl_sum, GT, Fr
from parser import parse_args
from proof_of_possession_2.proof_of_possession_2_utils import generate_file, psi_Fr


class Client(Initiator):
    def __init__(self, u: G1, g: G2, m: int, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Initiator.__init__(self, ip, port)
        self.u = u
        self.g = g
        self.m = m
        self.x = get_Fr()
        self.y = self.g * self.x

        self.file = None
        self.file_id = None
        self.sigmas = []
        self.k = None
        self.rs = None

    def store_sigmas(self):
        for j, b in enumerate(self.file):
            h = get_G(value=std_concat_method(self.file_id, j), group=G1)
            sigma = (h + (self.u * b)) * self.x
            self.sigmas.append(sigma)

    def produce_k_and_rs(self):
        self.k = get_Fr()
        self.rs = [psi_Fr(k=self.k, j=j) for j in range(len(self.file))]

    def verify(self, sigma, mu):
        W_elements = [get_G(value=std_concat_method(self.file_id, j), group=G1) * r for j, r in enumerate(self.rs)]
        W = mcl_sum(li=W_elements)
        if GT.pairing(sigma, self.g) == GT.pairing(W + self.u * mu, self.y):
            return "Proof of possession accepted."
        else:
            return "Proof of possession rejected."

    def set_file(self, file, file_id):
        self.file = file
        self.file_id = file_id

    def get_file(self):
        return self.file

    def get_sigmas(self):
        return self.sigmas

    def get_k(self):
        return self.k


def main():
    args = parse_args()
    u = get_G(value=b"genQ", group=G1)
    g = get_G(value=b"genQ", group=G2)
    client = Client(u=u, g=g, m=args.m, ip=args.ip, port=args.port)
    client.set_file(file=generate_file(part_num=args.m), file_id="Zdjecia_z_Chorwacji_2012")
    client.store_sigmas()
    client.produce_k_and_rs()

    file = client.get_file()
    sigmas = client.get_sigmas()
    k = client.get_k()
    client.send_message(message=jstore({"F": file, "sigma": sigmas, "k": k}))

    sigma_mu_ = client.receive_message()
    sigma_mu = jload({"sigma": G1, "mu": Fr}, sigma_mu_, True)
    sigma, mu = sigma_mu["sigma"], sigma_mu["mu"]

    verification_status = client.verify(sigma=sigma, mu=mu)
    client.send_message(verification_status)

    print(verification_status)


if __name__ == "__main__":
    main()
