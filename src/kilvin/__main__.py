import argparse
import pathlib
import shutil
import os
from livereload import Server
import sys

from kilvin.cmds import build, create, new


def clean():
    for root, dirs, files in os.walk('./public'):
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

    parser_build = subparsers.add_parser("build", help="Build the current project.")

    parser_build = subparsers.add_parser("server", help="Serve the current project.")

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
        clean()
        build.build_proj()
    elif args.cmd == "server":
        server()
