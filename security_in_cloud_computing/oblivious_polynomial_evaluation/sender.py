from common_protocol import Initiator
from mcl_utils import get_G, G1, get_Fr
from parser import parse_args


class Sender(Initiator):
    def __init__(self, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Initiator.__init__(self, ip, port)
        alpha = get_Fr(value=2)



def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=G1)
    sender = Sender(ip=args.ip, port=args.port)




if __name__ == "__main__":
    main()
