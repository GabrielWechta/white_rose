from abc import abstractmethod
from random import getrandbits

from mcl_utils import get_Fr, std_concat_method
from naxos_ake.naxos_ake_utils import GROUP, HASH_CLS


class NAXOSParty:
    def __init__(self, g: GROUP, lam: int):
        self.g = g
        self.lam = lam
        self.sk_m = get_Fr()
        self.pk_m = self.g * self.sk_m
        self.esk_m = getrandbits(self.lam)
        self.hash_obj = HASH_CLS()

        self.pk_y = None
        self.commitment_exp_m = None
        self.commitment_m = None
        self.commitment_y = None
        self.K = None

    def set_another_party_pk(self, pk_y):
        self.pk_y = pk_y

    def produce_commitment(self):
        self.commitment_exp_m = get_Fr(value=std_concat_method(self.esk_m, self.sk_m))
        self.commitment_m = self.g * self.commitment_exp_m
        return self.commitment_m

    def set_another_party_commitment(self, commitment_y):
        self.commitment_y = commitment_y

    @abstractmethod
    def produce_session_key(self):
        ...

    def show_K(self):
        print("I have: ")
        print(self.K.hex())
