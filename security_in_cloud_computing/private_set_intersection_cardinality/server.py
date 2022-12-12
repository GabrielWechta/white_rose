from common_protocol import Initiator
from klib import jstore, jload
from mcl_utils import std_concat_method, get_G, get_Fr
from parser import parse_args
from private_set_intersection.private_set_intersection_utils import GROUP
from private_set_intersection_cardinality.private_set_intersection_cardinality_utils import set_exponentiation

CONCAT_METHOD = std_concat_method


class Server(Initiator):
    def __init__(self, private_set: list, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Initiator.__init__(self, ip, port)
        self.private_set = private_set
        self.r = get_Fr()
        print(f"I have {self.private_set=}")

    def produce_hash_exp_set(self):
        hash_set = [get_G(value=s.encode(), group=GROUP) for s in self.private_set]
        return set_exponentiation(se=hash_set, exp=self.r)

    def find_intersection_size(self, mine_hash_exp_exp_list, his_hash_exp_list):
        mine_hash_exp_exp_rev_exp_list = set_exponentiation(mine_hash_exp_exp_list, get_Fr(1) / self.r)
        mine_hash_exp_exp_set = set(str(e) for e in mine_hash_exp_exp_rev_exp_list)
        his_hash_exp_set = set(str(e) for e in his_hash_exp_list)
        l = len(mine_hash_exp_exp_set & his_hash_exp_set)
        print("Intersection size is: ", l)
        return l


def main():
    args = parse_args()
    server = Server(private_set=["a", "b", "c", "d"], ip=args.ip, port=args.port)

    hash_exp_set = server.produce_hash_exp_set()
    server.send_message(message=jstore({"A": hash_exp_set}))

    A_hat_B_hat_ = server.receive_message()
    A_hat_B_hat = jload({"B": [GROUP], "C": [GROUP]}, A_hat_B_hat_, True)

    mine_hash_exp_exp_list = A_hat_B_hat["B"]
    his_hash_exp_list = A_hat_B_hat["C"]
    l = server.find_intersection_size(mine_hash_exp_exp_list=mine_hash_exp_exp_list,
                                      his_hash_exp_list=his_hash_exp_list)

    server.send_message(message=str(l))


if __name__ == "__main__":
    main()
