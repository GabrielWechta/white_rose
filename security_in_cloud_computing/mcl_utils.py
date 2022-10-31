import sys
import os
import json
import functools

sys.path.insert(1, '/home/gabriel/opt/mcl-python')

from mcl import Fr, G1

Fr = Fr
G1 = G1


def get_Fr(value=None):
    fr = Fr()
    if value is None:
        fr.setByCSPRNG()
    else:
        fr.setInt(value)
    return fr


def pow_Fr(fr, exp):
    result = get_Fr(1)
    for _ in range(exp):
        result *= fr
    return fr


def get_G1(value=None):
    if value is None:
        rnd_bytes = os.urandom(16)
        g = G1.hashAndMapTo(rnd_bytes)
    else:
        g = G1.hashAndMapTo(value)
    return g


def jstore(d):
    return json.dumps(
        {k: v.getStr().decode() if type(v) != bytes else v.hex() for k, v in
         d.items()})


def jload(d, j):
    j = json.loads(j)
    r = []
    for k, t in d.items():
        if t != bytes:
            v = t()
            v.setStr(j[k].encode())
        else:
            v = t.fromhex(j[k])
        r.append(v)
    return r


def monitor_func(func):
    @functools.wraps(func)
    def wrapper(*func_args, **func_kwargs):
        print('function call ' + func.__name__ + '()')
        retval = func(*func_args, **func_kwargs)
        print('function ' + func.__name__ + '() returns ' + repr(retval))
        return retval

    return wrapper