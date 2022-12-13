import hashlib

from mcl_utils import G1

GROUP = G1
HASH_CLS = hashlib.sha256

def split_gen(l, z):
    k, m = divmod(len(l), z)
    return (l[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(z))