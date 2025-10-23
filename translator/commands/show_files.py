from pathlib import Path
import typing

import typer

from translator import constants, utils


__all__ = ['show_files']


def show_files(
    match: typing.Annotated[str | None, typer.Argument(help='Translates only matching files.')] = None,
) -> None:

    for file_path in utils.list_md_files(match=match):
        typer.echo(file_path)
