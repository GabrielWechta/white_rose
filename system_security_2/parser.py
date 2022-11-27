import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--port",
        dest="port",
        type=int,
    )

    parser.add_argument(
        "--ip",
        dest="ip",
        type=str,
    )
    return parser.parse_args()
