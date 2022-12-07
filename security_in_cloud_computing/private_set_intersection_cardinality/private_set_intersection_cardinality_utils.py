import hashlib
from random import shuffle

from mcl_utils import G1, G2

GROUP = G1
HASH_CLS = hashlib.sha256


def set_exponentiation(se, exp):
    return [e * exp for e in se]


def shuffle_ret(li):
    shuffle(li)
    return li
