from broadcast_encryption.broadcaster import Broadcaster
from broadcast_encryption.user import User
from mcl_utils import get_G1


def main():
    z = 3
    broadcaster = Broadcaster(z=z)
    g = get_G1()
    broadcaster.setup()

    users = []
    for user_id in range(z):
        user = User(id=user_id, g=g)
        x_user, y_user = broadcaster.register_user(user_id)
        user.receive_register_response(x=x_user, y=y_user)
        users.append(user)

    header = broadcaster.make_header(excluded_users_ids=[1,2])

    for user in users:
        user.receive_header(header=header)
        user.generate_fresh_K()


if __name__ == "__main__":
    main()
