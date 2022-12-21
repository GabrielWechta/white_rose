import hashlib

from mcl_utils import G1

STRING_ENCODING = 'utf-8'
GROUP = G1
HASH_CLS = hashlib.sha256
LAM = 256


def hash_values_to_group_element(*values) -> GROUP:
    """Hash a tuple of values to a group element to model PRF and MAC."""
    seed = ""
    for value in values:
        seed += str(value)
    return GROUP.hashAndMapTo(bytes(seed, STRING_ENCODING))


def std_concat_method(*args):
    con = ""
    for arg in args:
        con += str(arg)

    return con.encode()
