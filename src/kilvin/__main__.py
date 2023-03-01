import argparse
import pathlib
import sys

from livereload import Server

from kilvin import utils
from kilvin.cmds import build, init, new

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def server():
    server = Server()
    try:
        print("Serving.")
        server.serve(root="./public")
    except KeyboardInterrupt:
        sys.exit(1)


def load_config():
    if not pathlib.Path("config.toml").exists():
        print("Config file not found.")
    with open("config.toml", "rb") as cf:
        try:
            config = tomllib.load(cf)
            return config
        except tomllib.TOMLDecodeError:
            print("Something's wrong with the config file.")


def main(config):
    parser = argparse.ArgumentParser(
        prog="Kilvin", description="A simple static site generator."
    )
    subparsers = parser.add_subparsers(dest="cmd", help="Help:")

    parser_init = subparsers.add_parser(
        "init", help="Create directory structure for the project."
    )
    parser_init.add_argument(
        "path", type=pathlib.Path, help="Path for the project directory. "
    )

    subparsers.add_parser("build", help="Build the current project.")

    subparsers.add_parser("server", help="Serve the current project.")

    parser_new = subparsers.add_parser("new", help="Create a new markdow post.")
    parser_new.add_argument(
        "path", type=pathlib.Path, help="Path for the markdown post. "
    )

    args = parser.parse_args()

    if args.cmd == "init":
        init.init(args.path)
    elif args.cmd == "new":
        new.create_new_file(args.path)
    elif args.cmd == "build":
        utils.clean_public()
        build.build_proj(config)
    elif args.cmd == "server":
        server()


if __name__ == "__main__":
    config = load_config()
    main(config)
