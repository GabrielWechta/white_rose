import hashlib
from mcl_utils import G1, G2

GROUP = G1
HASH_CLS = hashlib.sha256


def bytes_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


BYTES_XOR = bytes_xor
