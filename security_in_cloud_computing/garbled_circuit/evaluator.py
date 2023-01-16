from typing import List

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from common_protocol import Responder
from garbled_circuit.garbled_circuit_utils import byte_concat
from klib import jload, jstore
from mcl_utils import get_Fr, get_G
from oblivious_polynomial_evaluation.oblivious_polynomial_evaluation_utils import HASH_CLS, BYTES_XOR, GROUP
from parser import parse_args


class Evaluator(Responder):
    def __init__(self, g: GROUP, x2: bool, ot_type: str, ip: str = None, port: int = None):
        if ip is not None and port is not None:
            Responder.__init__(self, ip, port)
        self.g = g
        self.x2 = x2
        self.hash_obj = HASH_CLS()
        self.C = None
        self.La = None
        self.Lb = None
        self.k = None

        # OT attributes
        self.ot_type = ot_type
        self.alpha = None
        self.Rs = None
        self.Cs = None
        self.W = None

    # OT methods
    def set_Rs(self, Rs: List[GROUP]):
        self.Rs = Rs

    def produce_W(self, j: int):
        self.alpha = get_Fr()
        R = self.Rs[j]
        if self.ot_type == "krzywiecki":
            self.W = R * self.alpha
        elif self.ot_type == "rev_gr_el":
            self.W = R + (self.g * self.alpha)

        return self.W

    def set_Cs(self, Cs: List[str]):
        self.Cs = Cs

    def calculate_Lb(self, j):
        C = self.Cs[j]
        hash_obj = HASH_CLS()
        if self.ot_type == "krzywiecki":
            g_a_bytes = str(self.g * self.alpha).encode("utf-8")
            hash_obj.update(g_a_bytes)
        elif self.ot_type == "rev_gr_el":
            R = self.Rs[j]
            R_a_bytes = str(R * self.alpha).encode("utf-8")
            hash_obj.update(R_a_bytes)

        h_g_bytes = hash_obj.digest()
        C_bytes = bytes.fromhex(C)
        m_bytes = BYTES_XOR(C_bytes, h_g_bytes)
        self.Lb = m_bytes

    def set_La(self, La):
        self.La = La

    def set_C(self, C):
        self.C = C

    def prepare_key(self):
        self.hash_obj.update(byte_concat(bytes.fromhex(self.La), self.Lb))
        self.k = self.hash_obj.digest()
        print(f"{self.k=}")

    @staticmethod
    def decrypt(key, ciphertext):
        # iv_str, payload_str = ciphertext
        print(f"{ciphertext=}")
        payload = bytes.fromhex(ciphertext)
        cipher = AES.new(key=key, mode=AES.MODE_ECB)
        plaintext = unpad(cipher.decrypt(payload), AES.block_size)
        return plaintext

    def produce_garbled_circuit_output(self):
        output = self.decrypt(key=self.k, ciphertext=self.C)
        return int.from_bytes(output, "little")


def main():
    args = parse_args()
    g = get_G(value=b"genQ", group=GROUP)
    evaluator = Evaluator(g=g, x2=bool(args.x2), ot_type=args.ot_type, ip=args.ip, port=args.port)

    L_c_ = evaluator.receive_message()
    L, c = jload({"L": str, "c": [str]}, L_c_)

    j = 0 if evaluator.x2 is False else 1
    evaluator.set_La(La=L)
    evaluator.set_C(C=c[j])

    Rs_ = evaluator.receive_message()
    Rs = jload({"R": [GROUP]}, Rs_, True)["R"]
    evaluator.set_Rs(Rs=Rs)

    W = evaluator.produce_W(j=j)
    evaluator.send_message(jstore({"W": W}))

    Cs_ = evaluator.receive_message()
    Cs = jload({"c": [str]}, Cs_, True)["c"]
    evaluator.set_Cs(Cs=Cs)

    evaluator.calculate_Lb(j=j)
    evaluator.prepare_key()
    gc_output = evaluator.produce_garbled_circuit_output()

    # evaluator.send_message(message=str(gc_output))

    print(f"Evaluator calculated: {gc_output}")


if __name__ == "__main__":
    main()
