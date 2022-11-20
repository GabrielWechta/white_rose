import json
from typing import Union

class MCLJsonEncoder(json.JSONEncoder):
    """JSON encoder capable of properly encoding mcl structures."""
    def default(self, o):
        if hasattr(o, "getStr"):
            return o.getStr().decode() if type(o) != bytes else o.hex()
        else:
            return json.JSONEncoder.default(self, o)
                
def jload(expected_values: dict, json_str: str, return_dict: bool = False) -> Union[dict, list]:
    """
    Decode JSON string.
    
    By default it returns a list for backwards compatibility. 
    return_dict=True is suggested for convenience.
    """
    preprocessed_dict = json.loads(json_str)
    result = {} if return_dict else []
    
    for key, val in expected_values.items():
        type = val
        decoded = __parse_single(type, preprocessed_dict[key])
        
        if return_dict:
            result[key] = decoded
        else:    
            result.append(decoded)

    return result

def __parse_single(cls, str_or_list):
    try:
        iter(cls)
        iterable = True
    except TypeError as te:
        iterable = False

    if iterable:
        decoded = []
        # assume homogenous
        if len(cls) == 1:
            list = [cls[0] for i in range(len(str_or_list))]
        elif len(cls) == len(str_or_list):
            list = cls
        else:
            raise Exception("Expected list has different length than list in JSON.")
        for i, single in enumerate(str_or_list):
            # yes its recurrent, sue me
            decoded.append(__parse_single(list[i], single))
        decoded = type(cls)(decoded)
    else:
        object = str_or_list
        if not isinstance(object, cls) if cls != None else cls != None:
            if cls != bytes:
                decoded = cls()
                decoded.setStr(object.encode())
            else:
                decoded = cls.fromhex(object)
        else:
            decoded = object
    return decoded



def jstore(dictionary: dict) -> str:
    """Encode dictionary as a JSON string."""
    return json.dumps(dictionary, cls=MCLJsonEncoder)

def __jstore(d: dict) -> str:
    return json.dumps({ k: v.getStr().decode() if type(v) != bytes else v.hex() for k, v in d.items() })

def __jload_single(d: dict, j: str) -> dict:
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


if __name__ == "__main__":
    # some tests
    from mcl import Fr, G1, G2, GT

    num1: Fr = Fr.rnd()
    num2: Fr = Fr.rnd()
    point1: G1 = G1.hashAndMapTo(b"Test1")
    point2: G2 = G2.hashAndMapTo(b"Test2")

    plain_dict = {"X": num1, "Y": num2}
    homogenous_list = {"X": [num1, num2, num1]}
    two_lists = {"X": [num1, num2], "Y": [point1, point1, point1]}
    tuple_dict = {"X": (num1, num2)}
    not_homogenous_list = {"X": [num1, point1, point2]}
    non_mcl_types = {"X": [num1, 13, "test", None]}

    print(plain_dict)
    json_str = jstore(plain_dict)
    print(json_str)
    res = jload({"X": Fr, "Y": Fr}, json_str, True)
    print(res)
    assert plain_dict == res
    print("Plain dict OK")

    print(homogenous_list)
    json_str = jstore(homogenous_list)
    print(json_str)
    res = jload({"X": [Fr]}, json_str, True)
    print(res)
    assert homogenous_list == res
    print("Homogenous list OK")

    print(two_lists)
    json_str = jstore(two_lists)
    print(json_str)
    res = jload({"X": [Fr], "Y": [G1]}, json_str, True)
    print(res)
    assert two_lists == res
    print("two lists OK")

    print(tuple_dict)
    json_str = jstore(tuple_dict)
    print(json_str)
    res = jload({"X": (Fr, Fr)}, json_str, True)
    print(res)
    assert tuple_dict == res
    print("tuple OK")

    print(not_homogenous_list)
    json_str = jstore(not_homogenous_list)
    print(json_str)
    res = jload({"X": [Fr, G1, G2]}, json_str, True)
    print(res)
    assert not_homogenous_list == res
    print("Not homogenous list OK")

    print(non_mcl_types)
    json_str = jstore(non_mcl_types)
    print(json_str)
    res = jload({"X": [Fr, int, str, None]}, json_str, True)
    print(res)
    assert non_mcl_types == res
    print("non MCL types OK")

    print(two_lists)
    json_str = jstore(two_lists)
    print(json_str)
    res = jload({"X": [Fr], "Y": [G1]}, json_str, False)
    print(res)
    print("two lists return type list OK")

    print("All 'tests' passed")
    