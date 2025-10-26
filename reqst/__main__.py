import argparse
from .main import read_file, send_request, output_formatted


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
    request = read_file(args.file)
    response = send_request(request)
    output_formatted(response)