from common_protocol import Responder
from klib import jload, jstore
from mcl_utils import get_G, get_Fr
from parser import parse_args
from private_set_intersection_cardinality_utils import GROUP, set_exponentiation, shuffle_ret


class Client(Responder):
    def __init__(self, private_set: list, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Responder.__init__(self, ip, port)
        self.d = get_Fr()
        self.perm_private_set = shuffle_ret(private_set)
        print(f"I have {self.perm_private_set=}")

    def produce_perm_hash_exp_set(self):
        hash_set = [get_G(value=c.encode(), group=GROUP) for c in self.perm_private_set]
        return set_exponentiation(se=hash_set, exp=self.d)

    def produce_perm_exp_exp_set(self, his_hash_exp_set):
        his_perm_hash_exp_set = shuffle_ret(his_hash_exp_set)
        return set_exponentiation(se=his_perm_hash_exp_set, exp=self.d)


def main():
    args = parse_args()
    client = Client(private_set=["a", "d", "c", "f", "g", "h"], ip=args.ip, port=args.port)

    mine_perm_hash_exp_set = client.produce_perm_hash_exp_set()

    A_ = client.receive_message()
    A = jload({"A": [GROUP]}, A_, True)
    his_hash_exp_set = A["A"]
    his_perm_hash_exp_exp_set = client.produce_perm_exp_exp_set(his_hash_exp_set=his_hash_exp_set)

    client.send_message(message=jstore({"B": his_perm_hash_exp_exp_set, "C": mine_perm_hash_exp_set}))
    print("I have finished.")

    l = client.receive_message()
    print(f"We share {l} files.")


if __name__ == "__main__":
    main()
