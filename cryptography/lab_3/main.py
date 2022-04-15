from initiator import Initiator
from responder import Responder


def main():
    n = 15
    initiator = Initiator(n)
    responder = Responder(n)
    challenges = responder.get_challenges()
    initiator.put_challenges(challenges)
    initiator.solve_merkel_puzzle()
    responder.put_challenge_id(initiator.get_challenge_id())

    print(initiator.key_bytes == responder.key_bytes)

if __name__ == "__main__":
    main()
