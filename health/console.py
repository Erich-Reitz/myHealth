# standard library
import argparse

# this package
from . import health


def run():
    args = _parse_args()
    health.health(args)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--action",
        required=True,
        choices=["pull"],
        help="pull and format health information",
    )
    args = parser.parse_args()
    return args
