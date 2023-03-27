import functools

import click


def pretty_print(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        click.secho("")
        func(*args, **kwargs)

    return wrapper


@pretty_print
def succ(msg):
    click.secho(msg, fg="green")


@pretty_print
def info(msg):
    click.secho(msg, fg="cyan")


@pretty_print
def error(msg):
    click.secho(msg, fg="red")
