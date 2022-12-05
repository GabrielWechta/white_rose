"""by Adrian Cinal ver 2"""
import socket
from typing import Callable

RECV_BUF_SIZE = 4 * 1024     # Receive a page
STRING_ENCODING = "utf-8"
IP_VERSION = socket.AF_INET  # Use IPv4
SYNC_CHARACTER = "_"

UPDATED_VERSION = True

class Party:
    """Protocol party."""

    def send_message(self, message: str) -> None:
        """Send a message to the other party."""
        if UPDATED_VERSION:
            # Append a page of sync data to the payload
            payload = message + SYNC_CHARACTER * RECV_BUF_SIZE
        else:
            payload = message
        self.sock.send(bytes(payload, STRING_ENCODING))

    def receive_message(self) -> str:
        """Receive a message from the other party."""

        if UPDATED_VERSION:
            message = ""
            while message[-RECV_BUF_SIZE:] != SYNC_CHARACTER * RECV_BUF_SIZE:
                frame = str(self.sock.recv(RECV_BUF_SIZE), STRING_ENCODING)
                if not frame:
                    raise Exception("Failed to receive the message from the other party")
                message += frame
            # Skip the last page of sync
            return message[:-RECV_BUF_SIZE]
        else:
            return str(self.sock.recv(RECV_BUF_SIZE), STRING_ENCODING)

class Initiator(Party):
    """Initiator party (prover, signer, client)."""

    def __init__(self, ip: str, port: int) -> None:
        """Start the initiator."""
        # Open a clientside TCP socket
        self.sock = socket.socket(IP_VERSION, socket.SOCK_STREAM, 0)
        # Connect to the responder (verifier, server)
        self.sock.connect((ip, port))

class Responder(Party):
    """Responder party (verifier, server)."""

    def __init__(self, ip: str, port: int, callback: Callable = None) -> None:
        """Start the responder."""
        # Open a serverside TCP socket
        self.listen_sock = socket.socket(IP_VERSION, socket.SOCK_STREAM, 0)
        # Assign a name to the socket
        self.listen_sock.bind((ip, port))
        # Mark the socket as passive with no backlog
        self.listen_sock.listen(0)
        # Run a custom callback, if any provided, e.g. to synchronize
        # the initiator and the responder on a single host
        if callback:
            callback()
        # Block until a client connects
        self.sock, _ = self.listen_sock.accept()
