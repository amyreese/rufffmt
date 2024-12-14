# Copyright Amethyst Reese
# Licensed under the MIT license

import logging
import sys
from pathlib import Path

import click
import trailrunner
from click_fuzzy import FuzzyCommandGroup

from .core import rufffmt_file, rufffmt_text


@click.group(cls=FuzzyCommandGroup)
@click.option("--debug", is_flag=True, default=False, help="Enable debug logging")
def main(debug: bool) -> None:
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.DEBUG if debug else logging.WARNING,
    )
    pass


@main.command("format")
@main.alias("f")
@click.option(
    "--stdin-filename",
    required=False,
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path),
)
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(resolve_path=True, allow_dash=True, path_type=Path),
)
def format(paths: list[Path], stdin_filename: Path | None) -> None:
    """
    Format a file or stdin
    """
    if paths and paths[0] == Path("-"):
        # stdin
        content = sys.stdin.read()
        content = rufffmt_text(stdin_filename or Path("-"), content)
        print(content)

    else:
        trailrunner.walk_and_run(paths, rufffmt_file)
        print("done", file=sys.stderr)


@main.command("lsp")
def lsp() -> None:
    """
    Start a formatting language server
    """
    from .lsp import rufffmt_lsp

    rufffmt_lsp().start_io()
