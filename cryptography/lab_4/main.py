import argparse
import pathlib
from pprint import pprint
from typing import List

from jks import jks

from attacker import Attacker
from cpa_experiment import CPAExperiment
from encryptor import Encryptor


class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Program for encrypting message and playing CPA game, "
                    "using AES-CBC and AES-GCM."
    )

    parser.add_argument(
        "--mode",
        dest="mode",
        type=str,
        choices=["enc_oracle", "challenge"],
        help="encryption oracle - on input consisting q messages: m_1, m_2, "
             "..., m_q it returns it ciphertexts. \n "
             "challenge - on input m_0, m_1 program picks independently, "
             "uniformly random bit b from {0, 1} and returns a ciphertext c_b "
             "of a message m_b."
    )

    parser.add_argument(
        "--bc_mode",
        dest="bc_mode",
        type=str,
        choices=["CBC", "GCM"],
        help="Block cipher mode of operation, from {CBC, GCM}",
    )

    parser.add_argument(
        "--keystore_path",
        dest="keystore_path",
        type=str,
        help="Path to the keystore file location.",
    )

    parser.add_argument(
        "--key_identifier",
        dest="key_identifier",
        type=str,
        help="Identifier for key in keystore file.",
    )

    parser.add_argument(
        "--keystore_password",
        dest="keystore_password",
        type=str,
        help="Password for keystore.",
    )

    parser.add_argument(
        "--messages_file_path",
        dest="messages_file_path",
        type=str,
        help="Path to file with messages. Messages should be seperated with \\n",
    )

    return parser.parse_args()


def get_privkey_from_keystore(keystore_path: str, key_identifier: str,
                              keystore_password: str):
    keystore = jks.KeyStore.load(keystore_path, keystore_password)
    privkey_entry = keystore.private_keys[key_identifier]

    # if the key could not be decrypted using the store password,
    # decrypt with a custom password now
    if not privkey_entry.is_decrypted():
        privkey_entry.decrypt(keystore_password)

    privkey = privkey_entry.pkey
    privkey += bytes(1)
    # print(f"{privkey=}")
    return privkey


def read_file_to_list(file_path: pathlib.Path) -> List[bytes]:
    messages = []
    with open(file_path) as file:
        while line := file.readline().rstrip():
            messages.append(line.encode())

    return messages


def enc_oracle(encryptor: Encryptor, messages: List[bytes]):
    for message in messages:
        print(f"{message} -> {encryptor.encrypt(message)}")


def chosen_plaintext_attack(cpa_exp: CPAExperiment, attacker: Attacker):
    stage_one_messages = attacker.produce_stage_one_messages(3)
    print(c.HEADER + "Attacker sends x_0, x_1, ..., x_i:" + c.ENDC)
    pprint(stage_one_messages)

    stage_one_ciphertext = cpa_exp.conduct_stage_one(stage_one_messages)
    print(c.OKBLUE + "Attacker receives y_0, y_1, ..., y_i:" + c.ENDC)
    pprint(stage_one_ciphertext)
    attacker.set_stage_one_ciphertexts(
        stage_one_ciphertexts=stage_one_ciphertext)

    challenge_mes_1, challenge_mes_2 = attacker.produce_challenge_messages()
    print(c.HEADER + "Attacker sends m_1, m_2:" + c.ENDC)
    pprint({challenge_mes_1, challenge_mes_2})

    challenge_cipher = cpa_exp.get_challenge(challenge_mes_1, challenge_mes_2)
    print(c.OKBLUE + "Attacker receives c_b:" + c.ENDC)
    pprint(challenge_cipher)
    attacker.set_challenge_ciphertext(challenge_ciphertext=challenge_cipher)

    stage_two_messages = attacker.produce_stage_two_messages()
    print(c.HEADER + "Attacker sends m_1 XOR IV_{i+1} XOR IV_{i+2}...")
    print("and sends m_2 XOR IV_{i+1} XOR IV_{i+3}..." + c.ENDC)
    pprint(stage_two_messages)

    stage_two_ciphertext = cpa_exp.conduct_stage_two(stage_two_messages)
    print(c.OKBLUE + "Attacker receives c_1, c_2:" + c.ENDC)
    pprint(stage_two_ciphertext)
    attacker.set_stage_two_ciphertexts(
        stage_two_ciphertexts=stage_two_ciphertext)

    attacker_b = attacker.decide_b()
    print(c.OKCYAN + f"Attacker decides that b={attacker_b}." + c.ENDC)
    print(c.OKGREEN + "Attacker won." + c.ENDC) if cpa_exp.check_b(
        attacker_b) else print(
        c.FAIL + "Attacker failed." + c.ENDC)


def main():
    args = _parse_args()
    mode, bc_mode = args.mode, args.bc_mode
    keystore_path, key_identifier = args.keystore_path, args.key_identifier
    keystore_password = args.keystore_password
    messages_file_path = pathlib.Path(args.messages_file_path)

    privkey = get_privkey_from_keystore(keystore_path=keystore_path,
                                        key_identifier=key_identifier,
                                        keystore_password=keystore_password)

    if mode == "enc_oracle":
        encryptor = Encryptor(private_key=privkey, bc_mode=bc_mode)
        messages_to_encrypt = read_file_to_list(file_path=messages_file_path)
        enc_oracle(encryptor=encryptor, messages=messages_to_encrypt)

    if mode == "challenge":
        attacker = Attacker()
        cpa_exp = CPAExperiment(privkey=privkey, bc_mode=bc_mode)
        chosen_plaintext_attack(cpa_exp=cpa_exp, attacker=attacker)


if __name__ == "__main__":
    main()
