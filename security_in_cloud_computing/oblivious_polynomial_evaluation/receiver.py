from common_protocol import Responder
from klib import jload, jstore
from mcl_utils import get_G, mcl_sum, Fr, G1
from parser import parse_args
from proof_of_possession_2.proof_of_possession_2_utils import GROUP, psi_Fr


class Receiver(Responder):
    def __init__(self, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Responder.__init__(self, ip, port)

def main():
    args = parse_args()
    receiver = Receiver(ip=args.ip, port=args.port)



if __name__ == "__main__":
    main()
