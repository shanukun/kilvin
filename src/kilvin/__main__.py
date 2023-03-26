import pathlib

import click

from kilvin import configs, utils
from kilvin.cmds import build as _build
from kilvin.cmds import init as _init
from kilvin.cmds import new as _new
from kilvin.cmds import server as _server


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
        _server.start_server()

    cli()
