import socket
from typing import Callable

CHUNK_SIZE = 16 * 1024
STRING_ENCODING = "utf-8"
IP_VERSION = socket.AF_INET  # Use IPv4
SYNC_TRAILER = "@@@@@@@@@@@"

class Party:
    """Protocol party."""
    def __init__(self) -> None:
        """Instantiate a communicating party."""
        self.ring = ""

    def send_message(self, message: str) -> None:
        """Send a message to the other party."""
        # Add a postamble to allow for maintenance of message boundaries
        payload = message + SYNC_TRAILER
        self.sock.send(bytes(payload, STRING_ENCODING))

    def receive_message(self) -> str:
        """Receive a message from the other party."""
        # Loop until we find a sync sequence, i.e. until we have a full message
        while self.ring.find(SYNC_TRAILER) == -1:
            chunk = str(self.sock.recv(CHUNK_SIZE), STRING_ENCODING)
            if not chunk:
                raise Exception("Connection reset by peer")
            self.ring += chunk
        trailer = self.ring.find(SYNC_TRAILER)
        message = self.ring[:trailer]
        # Update the ringbuffer
        self.ring = self.ring[trailer + len(SYNC_TRAILER):]
        return message

class Initiator(Party):
    """Initiator party (prover, signer, client)."""

    def __init__(self, ip: str, port: int) -> None:
        """Start the initiator."""
        super().__init__()
        # Open a clientside TCP socket
        self.sock = socket.socket(IP_VERSION, socket.SOCK_STREAM, 0)
        # Connect to the responder (verifier, server)
        self.sock.connect((ip, port))

class Responder(Party):
    """Responder party (verifier, server)."""

    def __init__(self, ip: str, port: int, callback: Callable = None) -> None:
        super().__init__()
        """Start the responder."""
        # Open a serverside TCP socket
        self.listen_sock = socket.socket(IP_VERSION, socket.SOCK_STREAM, 0)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
