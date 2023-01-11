import hashlib

from mcl_utils import G2
from Crypto.Cipher import AES

GROUP = G2
HASH_CLS = hashlib.sha256
BC_MODE = AES.MODE_GCM


def NAND(x1: bool, x2: bool):
    if x1 is False and x2 is False:
        y = True
    if x1 is False and x2 is True:
        y = True
    if x1 is True and x2 is False:
        y = True
    if x1 is True and x2 is True:
        y = False
    return y


BOOLEAN_CIRCUIT = NAND
