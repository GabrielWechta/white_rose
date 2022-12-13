from common_protocol import Responder
from mcl_utils import get_G
from parser import parse_args
from proof_of_possession_2.proof_of_possession_2_utils import GROUP


class Cloud(Responder):
    def __init__(self, g: GROUP, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Responder.__init__(self, ip, port)


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    cloud = Cloud(g=g, ip=args.ip, port=args.port)


if __name__ == "__main__":
    main()
