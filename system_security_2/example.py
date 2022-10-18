from common_protocol import Initiator, Responder
import sys

HOSTNAME = "localhost"
PORT = 15000

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} [ prover | verifier ]")
elif sys.argv[1] == "prover":
    prover = Initiator(HOSTNAME, PORT)
    prover.send_message("Hello there")
    message = prover.receive_message()
    print(f"Prover received: {message}")
elif sys.argv[1] == "verifier":
    verifier = Responder(HOSTNAME, PORT)
    message = verifier.receive_message()
    print(f"Verifier received: {message}")
    verifier.send_message(f"{message}, yourself")
