from random import random
from typing import Tuple

from mcl_utils import Fr, get_Fr
from sigma_ake.sigma_ake_utils import GROUP, std_concat_method, hash_values_to_group_element


class SIGMAParty:
    eph_priv_key = None
    eph_pub_key = None
    K = None
    K0 = None
    K1 = None
    session_identifier = None

    def get_pub_key(self):
        ...

    @staticmethod
    def produce_session_identifier():
        session_identifier = random.randint(0, 10 ** 6)
        return session_identifier

    def produce_ephemeral(self, g: GROUP):
        self.eph_priv_key = get_Fr()
        self.eph_pub_key = g * self.eph_priv_key

    def derive_keys(self, eph_pub: GROUP, eph_priv_key: Fr):
        self.K = eph_pub * eph_priv_key
        self.K0 = self.PRF(self.K, "0")
        self.K1 = self.PRF(self.K, "1")

    def get_eph_pub_key(self):
        return self.eph_pub_key

    @staticmethod
    def schnorr_sign(g: GROUP, priv_key: Fr, message: Tuple[str, str, GROUP]):
        x = get_Fr()
        X = g * x
        h = Fr.setHashOf(str(message).encode())
        s = x + priv_key * h
        return X, s, message

    @staticmethod
    def schnorr_verify(g: GROUP, pub_key: GROUP, sigma: Tuple[GROUP, Fr], message: Tuple[str, GROUP, GROUP]):
        X, s = sigma
        h = Fr.setHashOf(str(message).encode())
        if g * s == X + (pub_key * h):
            return True
        else:
            return False

    @staticmethod
    def PRF(*values):
        return hash_values_to_group_element(values)

    @staticmethod
    def MAC(*values):
        return hash_values_to_group_element(values)

    def MAC_verify(self, mac: GROUP, key: GROUP, cert: GROUP):
        if self.MAC(key, cert) == mac:
            return True
        else:
            return False

    def sign_and_mac(self, g: GROUP, priv_key: Fr, message: Tuple[str, GROUP, GROUP], cert: str):
        sigma = self.schnorr_sign(g=g, priv_key=priv_key, message=message)
        mac = self.MAC(self.K0, cert)
        return sigma, mac
