# standard library
import argparse


# this package
from health import health
from health.exit_codes import EXIT_SUCCESS


def run():
    args = _parse_args()

    exit_code = health.health(args)
    if exit_code == EXIT_SUCCESS:
        print("exiting sucessfully")

    return EXIT_SUCCESS


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pull",
        required=False,
        nargs="?",
        default=False,
        const=True,
        choices=["body-comp", "heart-rate", "activites"],
        help="pull and health information",
    )
    parser.add_argument(
        "--plot",
        required=False,
        nargs="?",
        const="weight",
        default=False,
        choices=[
            "weight",
            "muscle-mass",
            "body-fat",
            "body-comp",
            "heart-rate",
            "activites",
        ],
        help="pull and health information",
    )
    args = parser.parse_args()
    return args
