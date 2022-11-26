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

    parser.add_argument(
        "--ot_type",
        dest="ot_type",
        choices=["krzywiecki", "rev_gr_el"],
        type=str,
    )

    parser.add_argument(
        "--n",
        dest="n",
        type=int
    )

    return parser.parse_args()
