import argparse
import pathlib

from kilvin.cmds import create

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Kilvin", description="A simple static site generator."
    )
    subparsers = parser.add_subparsers(dest="cmd", help="Help:")

    parser_init = subparsers.add_parser(
        "create", help="Create directory structure for the project."
    )
    parser_init.add_argument(
        "name", type=pathlib.Path, help="Name for the project directory. "
    )

    parser_build = subparsers.add_parser("build", help="Build the current project.")

    args = parser.parse_args()

    if args.cmd == "create":
        create.create(args.name)
