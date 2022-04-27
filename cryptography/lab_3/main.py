from initiator import Initiator
from responder import Responder


def main():
    n = 15
    initiator = Initiator(n=n)
    print(f"Initiator is created, {n=}.")
    responder = Responder(n=n,
                          num_of_challenges=10)  # num_of_challenges should be 2^n
    print(f"Responder is created, {n=}.")
    challenges = responder.get_challenges()
    print("Initiator asks for challenges.")
    print(f"Responder returns {challenges=}.")
    initiator.set_challenges(challenges)
    initiator.solve_merkel_puzzle()
    print("Initiator solves merkel_puzzle...")
    key_id = initiator.get_key_id()
    responder.set_challenge_id(key_id)
    print(f"Initiator sends {key_id=} to Responder.")

    print(
        f"Does Initiator and Responder have the same key? "
        f"{initiator.key_bytes == responder.key_bytes}")


if __name__ == "__main__":
    main()
