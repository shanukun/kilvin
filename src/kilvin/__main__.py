import pathlib
import sys

import click
from livereload import Server

from kilvin import configs, utils
from kilvin.cmds import build as _build
from kilvin.cmds import init as _init
from kilvin.cmds import new as _new


def start_server():
    server = Server()
    try:
        log.info("Serving.")
        server.serve(root="./public")
    except KeyboardInterrupt:
        sys.exit(1)


def main():
    @click.group()
    @click.version_option()
    def cli():
        """
        Kilvin is a simple static site generator.
        It takes markdown text and turns it into a static webpage using layouts.
        """
        pass

    @cli.command()
    @click.argument("path", type=pathlib.Path, nargs=1)
    def init(path):
        """Create directory structure for the project"""
        _init.create_project(path)

    @cli.command()
    @click.argument("path", type=pathlib.Path, nargs=1)
    def new(path):
        """Create a new markdow post in ./content dir"""
        _new.create_new_file(path)

    @cli.command()
    def build():
        """Build the current project"""
        utils.clean_public()
        _build.build_proj(configs.load_config())

    @cli.command()
    def server():
        """Serve the current project"""
        start_server()

    cli()
