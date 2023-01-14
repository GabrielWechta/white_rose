from random import shuffle

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

from common_protocol import Initiator
from garbled_circuit.garbled_circuit_utils import byte_concat, BOOLEAN_CIRCUIT
from klib import jload, jstore
from mcl_utils import get_G, get_Fr
from oblivious_polynomial_evaluation.oblivious_polynomial_evaluation_utils import GROUP, HASH_CLS, \
    BYTES_XOR
from parser import parse_args


def prepare_for_sending(d):
    d.pop('b')
    d["La"] = d["La"].hex()
    d["o"][0] = d["o"][0].hex()
    d["o"][1] = d["o"][1].hex()


class Garbler(Initiator):
    def __init__(self, g: GROUP, x1: bool, ot_type: str, ip: str = None, port: int = None):

        if ip is not None and port is not None:
            Initiator.__init__(self, ip, port)
        self.g = g
        self.x1 = x1

        self.garb_0 = None
        self.garb_1 = None
        self.eval_0 = None
        self.eval_1 = None
        self.k_00 = None
        self.k_01 = None
        self.k_10 = None
        self.k_11 = None

        self.circuit = None
        self.garbled_circuit = None

        # OT attributes
        self.n = 2
        self.ot_type = ot_type
        self.rs = []
        self.Rs = []
        self.Cs = []
        self.W = None

    def prepare_labels(self):
        self.garb_0 = get_random_bytes(16)
        self.garb_1 = get_random_bytes(16)
        self.eval_0 = get_random_bytes(16)
        self.eval_1 = get_random_bytes(16)

    @staticmethod
    def hash(data):
        hash_obj = HASH_CLS()
        hash_obj.update(data)
        return hash_obj.digest()

    def generate_keys(self):
        self.k_00 = self.hash(byte_concat(self.garb_0, self.eval_0))
        self.k_01 = self.hash(byte_concat(self.garb_0, self.eval_1))
        self.k_10 = self.hash(byte_concat(self.garb_1, self.eval_0))
        self.k_11 = self.hash(byte_concat(self.garb_1, self.eval_1))
        # print(f"{self.k_00=}")
        # print(f"{self.k_01=}")
        # print(f"{self.k_10=}")
        # print(f"{self.k_11=}")

    @staticmethod
    def encrypt(key, data):
        # print(data)
        cipher = AES.new(key=key, mode=AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return [cipher.iv, ciphertext]

    def prepare_garbled_circuit(self):
        # garbling
        self.garbled_circuit = [
            {'a': False, 'b': False, 'La': self.garb_0, 'Lb': self.eval_0,
             'o': self.encrypt(key=self.k_00, data=BOOLEAN_CIRCUIT(x1=False, x2=False))},
            {'a': False, 'b': True, 'La': self.garb_0, 'Lb': self.eval_1,
             'o': self.encrypt(key=self.k_01, data=BOOLEAN_CIRCUIT(x1=False, x2=True))},
            {'a': True, 'b': False, 'La': self.garb_1, 'Lb': self.eval_0,
             'o': self.encrypt(key=self.k_10, data=BOOLEAN_CIRCUIT(x1=True, x2=False))},
            {'a': True, 'b': True, 'La': self.garb_1, 'Lb': self.eval_1,
             'o': self.encrypt(key=self.k_11, data=BOOLEAN_CIRCUIT(x1=True, x2=True))},
        ]
        # pprint(self.garbled_circuit)
        # shuffling
        shuffle(self.garbled_circuit)

    def produce_garbled_circuit_share(self):
        tmp_share = []
        share = []
        for row in self.garbled_circuit:
            if row['a'] is self.x1:
                for key in ['a', 'Lb']:
                    row.pop(key)
                tmp_share.append(row)

        if tmp_share[0]['b'] is False:
            prepare_for_sending(tmp_share[0])
            prepare_for_sending(tmp_share[1])
            share.extend([tmp_share[0], tmp_share[1]])
        else:
            prepare_for_sending(tmp_share[0])
            prepare_for_sending(tmp_share[1])
            share.extend([tmp_share[1], tmp_share[0]])
        return share

    # OT methods
    def produce_Rs(self):
        for _ in range(self.n):
            r = get_Fr()
            self.rs.append(r)
            self.Rs.append(self.g * r)
        return self.Rs

    def set_W(self, W: GROUP):
        self.W = W

    def produce_Cs(self):
        for r, R, m_bytes in zip(self.rs, self.Rs, [self.eval_0, self.eval_1]):
            if self.ot_type == "krzywiecki":
                K = self.W * (get_Fr(1) / r)
            elif self.ot_type == "rev_gr_el":
                K = (self.W - R) * r
            else:
                raise ValueError
            hash_obj = HASH_CLS()
            K_bytes = str(K).encode()
            hash_obj.update(K_bytes)
            h_K_bytes = hash_obj.digest()
            C_bytes = BYTES_XOR(m_bytes, h_K_bytes)
            C = C_bytes.hex()
            self.Cs.append(C)
        return self.Cs


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    garbler = Garbler(g=g, x1=bool(args.x1), ip=args.ip, ot_type="krzywiecki", port=args.port)
    garbler.prepare_labels()
    garbler.generate_keys()
    garbler.prepare_garbled_circuit()
    share = garbler.produce_garbled_circuit_share()

    garbler.send_message(jstore({"Las": [share[0]["La"], share[1]["La"]], "Cs": [share[0]["o"], share[1]["o"]]}))

    Rs = garbler.produce_Rs()
    garbler.send_message(jstore({"R": Rs}))

    W_ = garbler.receive_message()
    W = jload({"W": GROUP}, W_, True)["W"]
    garbler.set_W(W=W)

    Cs = garbler.produce_Cs()
    garbler.send_message(jstore({"c": Cs}))

    gc_output = garbler.receive_message()
    print(f"Garbler calculated: {gc_output}")


if __name__ == "__main__":
    main()
