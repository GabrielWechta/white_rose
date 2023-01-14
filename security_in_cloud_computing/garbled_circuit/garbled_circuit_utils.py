import hashlib

from mcl_utils import G2
# from Crypto.Cipher import AES

GROUP = G2
HASH_CLS = hashlib.sha256
# BC_MODE = AES.MODE_GCM


def NAND(x1: bool, x2: bool):
    if x1 is False and x2 is False:
        y = 1
    if x1 is False and x2 is True:
        y = 1
    if x1 is True and x2 is False:
        y = 1
    if x1 is True and x2 is True:
        y = 0
    return str(y).encode()


BOOLEAN_CIRCUIT = NAND

def byte_concat(*args):
    concat = b''
    for arg in args:
        concat += arg
    return concat
