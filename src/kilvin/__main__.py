import argparse
import pathlib
import sys

from livereload import Server

from kilvin import configs, utils
from kilvin.cmds import build, init, new


def start_server():
    server = Server()
    try:
        print("Serving.")
        server.serve(root="./public")
    except KeyboardInterrupt:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="kilvin", description="A simple static site generator."
    )
    subparsers = parser.add_subparsers(dest="cmd", help="Help:")

    parser_init = subparsers.add_parser(
        "init", help="create directory structure for the project"
    )
    parser_new = subparsers.add_parser("new", help="create a new markdow post")

    parser_init.add_argument(
        "PATH", type=pathlib.Path, help="path for the project directory "
    )
    parser_new.add_argument(
        "PATH", type=pathlib.Path, help="path for the markdown post "
    )

    subparsers.add_parser("build", help="build the current project")

    subparsers.add_parser("server", help="serve the current project")

    args = parser.parse_args()

    if args.cmd == "init":
        init.init(args.PATH)
    elif args.cmd == "new":
        new.create_new_file(args.PATH)
    elif args.cmd == "build":
        utils.clean_public()
        build.build_proj(configs.load_config())
    elif args.cmd == "server":
        start_server()


if __name__ == "__main__":
    main()
