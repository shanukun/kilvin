import argparse
import pathlib
import sys

from livereload import Server

from kilvin import utils
from kilvin.cmds import build, create, new


def clean():
    for root, dirs, files in os.walk("./public"):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def server():
    server = Server()
    try:
        print("Serving.")
        server.serve(root="./public")
    except KeyboardInterrupt:
        print("Stop Server.")
        sys.exit(1)


if __name__ == "__main__":
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
        create.init(args.path)
    elif args.cmd == "new":
        new.create_new_file(args.path)
    elif args.cmd == "build":
        utils.clean_public()
        build.build_proj(config)
    elif args.cmd == "server":
        server()
