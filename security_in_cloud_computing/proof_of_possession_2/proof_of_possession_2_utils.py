import hashlib

from mcl_utils import G1, get_Fr, std_concat_method

GROUP = G1
HASH_CLS = hashlib.sha256


def split_gen(l, z):
    k, m = divmod(len(l), z)
    return (l[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(z))


def generate_file(part_num: int):
    file = []
    for _ in range(part_num):
        file.append(get_Fr())
    return file


def psi_Fr(k, j):
    return get_Fr(value=std_concat_method(k, j))
