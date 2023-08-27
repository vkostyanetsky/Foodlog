#!/usr/bin/env python3

"""
Router class for the application.
"""

import io
import os
import sys

from foodlog import constants
from foodlog.commands import command_show

import click


def __get_path(path: str | None) -> str:
    """
    Determines the path to a working directory. It is supposed to be the "Foodlog" folder
    in user's home directory in case it's not specified via app's options.
    """

    if path is None:
        path = os.path.expanduser("~")
        path = os.path.join(path, "Foodlog")

    return path


def __path_help() -> str:
    return "Set path to working directory."


def __path_type() -> click.Path:
    return click.Path(exists=True)


@click.group(help="CLI tool that helps to keep a food diary.", invoke_without_command=True)
@click.pass_context
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def cli(context: click.core.Context | None, path: str | None) -> None:
    """
    Main CLI entry point.
    """

    if isinstance(sys.stdout, io.TextIOWrapper) and sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding=constants.ENCODING)

    if context is None or not context.invoked_subcommand:
        __show(path)


@cli.command(help="Show details of fasting.")
@click.argument("what", default="last", type=click.Choice(["last", "prev", "on"]))
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def show(path: str | None, what: str) -> None:
    """
    Outputs detailed information about a fast.
    """

    __show(path, what)


def __show(path: str | None, what: str | None = "last") -> None:
    """
    Executes SHOW command (outputs detailed information about a fast).
    """

    path = __get_path(path)
    command_show.main(path, what)


if __name__ == "__main__":
    cli(context=None, path=None)
