"""Written by Adrian Cinal"""
import socket
from typing import Callable, Any, Tuple
import logging

RECV_BUF_SIZE = 128 * 1024  # Receive a sh*tton of pages
STRING_ENCODING = "utf-8"
IP_VERSION = socket.AF_INET  # Use IPv4


class Recipient:
    """Recipient node."""

    def __init__(self, ip: str, port: int) -> None:
        """Start the recipient."""
        # Open a clientside TCP socket
        self.sock = socket.socket(IP_VERSION, socket.SOCK_STREAM, 0)
        # Connect to the broadcaster
        self.sock.connect((ip, port))

    def receive_message(self) -> str:
        """Receive a message from the other party."""
        message = str(self.sock.recv(RECV_BUF_SIZE), STRING_ENCODING)
        if not message:
            raise Exception("Failed to receive the message from the broadcaster")
        return message


class AdrianBroadcaster:
    """Broadcaster party."""

    def __init__(self, ip: str, port: int, backlog: int) -> None:
        """Start the broadcaster."""
        # Open a serverside TCP socket
        self.listen_sock = socket.socket(IP_VERSION, socket.SOCK_STREAM, 0)
        # Assign a name to the socket
        self.listen_sock.bind((ip, port))
        # Mark the socket as passive
        self.listen_sock.listen(backlog)

    def accept_connections(self, n: int, log: logging.Logger) -> None:
        self.connections = []
        # Block until n clients connect
        log.debug(f"Waiting for {n} clients to connect...")
        for i in range(n):
            sock, address = self.listen_sock.accept()
            log.debug(f"Accepted a connection from {address}")
            self.connections.append(sock)

    def broadcast_message(self, message: str) -> None:
        """Broadcast a message to all recipients."""
        for recipient in self.connections:
            recipient.send(bytes(message, STRING_ENCODING))

    def send_message(self, sock, message) -> None:
        """Send a message to a given recipient."""
        sock.send(bytes(message, STRING_ENCODING))

    def receive_message(self, sock) -> str:
        """Receive a message from a given recipient."""
        message = str(sock.recv(RECV_BUF_SIZE), STRING_ENCODING)
        if not message:
            raise Exception("Failed to receive the message a recipient")
        return message

    def for_each_recipient(self, callback: Callable, arg: Any) -> Tuple[Any]:
        """Run a callback for each recipient."""
        retvals = []
        for recipient in self.connections:
            send_callback = lambda message: self.send_message(recipient, message)
            recv_callback = lambda: self.receive_message(recipient)
            retvals.append(callback(send_callback, recv_callback, arg))
        return retvals
