# A simple abstraction over TCP sockets (good enough for System Security II, if anyone has problems with it during Cloud, let me know ;)
from common_protocol import Initiator, Responder, STRING_ENCODING
# MCL Python wrapper
from mcl import G1, G2, Fr
# Serialization/deserialization library compatible with MCL (again good enough for System Security II, for Cloud it is highly advised to use Oliwer's klib)
from jlib import jload, jstore

# Choose the group of computation (good practice to declare it at the top for ease of matching with other students)
GROUP = G2
# Seed used for creating the group generator
HASHSEED = b"genQ"

# Model the pseudorandom function (PRF) and message authentication codes (MACs) via a simple hash
# - use a hash to the group element
def hash_values_to_group_element(*values) -> GROUP:
    """Hash a tuple of values to a group element to model PRF and MAC."""
    seed = ""
    for value in values:
        seed += str(value)
    # Hash to the group element (we could have used e.g. SHA, but some people may not be familiar with hashlib's API
    # so let's stick with MCL APIs) - also the jlib library will give you hell if you try sending strings or worse yet: bytearrays
    return GROUP.hashAndMapTo(bytes(seed, STRING_ENCODING))

def initiator_entry_point(responder_ip: str, responder_port: int) -> None:
    """Run the initiator party."""
    group_generator = GROUP.hashAndMapTo(HASHSEED)

    initiator = Initiator(responder_ip, responder_port)

    # Send the public key and commitment to the responder (use the common notation from the lecture and/or Schnorr schemes)
    first_message = jstore({ "X": commitment, "A": public_key })

    # NOTE: Anyone using the common_protocol library, please do not make several send_message calls in succession, always intertwine sending and receiving
    # - in practice this usually means sending public keys along with commitments in the same message (for technical reason behind this, ask me, I'll be happy
    # to discuss it :)
    initiator.send_message(first_message)

    # Note that the scheme uses a signature, let's use Schnorr signatures as they are the easiest to implement (just reuse code from the first exercise)

    second_message = initiator.receive_message()
    responder_commitment, responder_signature_commitment, \
        responder_signature_response, responder_mac, \
        responder_public_key = jload({
        # Bob's commitment
        "Y": GROUP,
        # Bob's signature over (X,Y,1)
        "sig_commit": GROUP,  # Schnorr commitment (X in Schnorr protocol description)
        "sig_response": Fr,   # Schnorr response (s in Schnorr protocol description)
        # Bob's MAC over B with K0 (hash h(K0, B))
        "MB": GROUP,
        # Bob's public key
        "B": GROUP
    }, second_message)

    # TODO: Verify Bob's MAC and signature

    ...

    # Produce our own signature
    my_signature_commitment, my_signature_response = schnorr_sign( (responder_commitment, my_commitment, 0), my_secret_key )  # Sign((X,Y,0), a)
    # Produce our own MAC (mocked by a hash function)
    hash_values_to_group_element(K0, public_key)  # MAC(K0, A)

    third_message = jstore({
        "sig_commit": my_signature_commitment,
        "sig_response": my_signature_response,
        "MA": my_mac
    })

    # The result of the protocol is a shared secret (K1 in the protocol description)
    print(f"I derived the common key: {hash_values_to_hex_string(K1)})

def responder_entry_point(ip: str, port: int) -> None
    """Run the responder party."""
    # Open the socket (block internally until a connection is established with an initiator)
    responder = Responder(ip, port)

    ...

    # TODO: Wait for the initiator's message

def hash_values_to_hex_string(*values) -> str:
    """Hash values using SHA-256 to a human-readable string for inspection."""
    h = hashlib.sha256()
    for value in values:
        h.update(bytes(str(value), STRING_ENCODING))
    ret = h.hexdigest()
    return ret
