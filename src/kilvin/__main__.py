import argparse
import pathlib

from kilvin.cmds import build, create, new

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Kilvin", description="A simple static site generator."
    )
    subparsers = parser.add_subparsers(dest="cmd", help="Help:")

    parser_init = subparsers.add_parser(
        "create", help="Create directory structure for the project."
    )
    parser_init.add_argument(
        "path", type=pathlib.Path, help="Path for the project directory. "
    )

    parser_build = subparsers.add_parser("build", help="Build the current project.")

    parser_new = subparsers.add_parser("new", help="Create a new markdow post.")
    parser_new.add_argument(
        "path", type=pathlib.Path, help="Path for the markdown post. "
    )

    args = parser.parse_args()

    if args.cmd == "create":
        create.create(args.path)
    elif args.cmd == "new":
        new.create_new_file(args.path)
    elif args.cmd == "build":
        build.build_proj()
