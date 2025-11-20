import argparse

from .main import Reqst


def parse_args():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "-f", "--file",
        type=str,
        required=True,
        help="The JSON/YAML/XML file to read the request from.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    reqst = Reqst()
    reqst.send_request(args.file)