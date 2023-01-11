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
        default="krzywiecki",
        type=str,
    )

    parser.add_argument(
        "--n",
        dest="n",
        type=int
    )

    parser.add_argument(
        "--j",
        dest="j",
        type=int
    )

    parser.add_argument(
        "--m",
        dest="m",
        type=int
    )

    parser.add_argument(
        "--k",
        dest="k",
        type=int
    )

    parser.add_argument(
        "--alpha",
        dest="alpha",
        type=int
    )

    parser.add_argument(
        "--x1",
        dest="x1",
        type=bool
    )

    parser.add_argument(
        "--x2",
        dest="x2",
        type=bool
    )

    parser.add_argument(
        "--key",
        dest="key",
        type=str,
    )
    return parser.parse_args()
