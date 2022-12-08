import hashlib
from mcl_utils import G1, G2, get_Fr, get_G, std_concat_method
from functools import reduce
import operator

GROUP = G1
HASH_CLS = hashlib.sha256
CONCAT_METHOD = std_concat_method
PUB_KEYS_NUM = 10


def create_pub_key(g: GROUP):
    a_list = []
    a = get_Fr()
    while a in a_list:
        a = get_Fr()
    a_list.append(a)
    yield g * a