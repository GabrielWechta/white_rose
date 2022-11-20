from broadcast_encryption.broadcaster import Broadcaster
from broadcast_encryption.broadcast_encryption_utils import Polynomial
from broadcast_encryption.user import User
from common_protocol import Responder
from mcl_utils import get_Fr, get_G1, monitor_func, std_concat_method


def main():
    z = 3
    broadcaster = Broadcaster(z=z)
    g = get_G1()
    broadcaster.setup(g=g)

    users = []
    for user_id in range(z):
        user = User(g=g)
        x_user, y_user = broadcaster.register_user(user_id)
        user.receive_register_response(x=x_user, y=y_user)
        users.append(user)

    broadcaster.make_header()


if __name__ == "__main__":
    main()
