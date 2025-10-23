from pathlib import Path
import typing

import typer

from translator import types, utils


__all__ = ['translate']


def translate(
        language: typing.Annotated[types.LanguageType, typer.Argument(help='The language you want to translate into.')],
        match: typing.Annotated[str | None, typer.Argument(help='Translates only matching files.')] = None,
) -> None:

    utils.cleanup_folder(language)
    file_paths = utils.list_md_files(match=match)
    client = utils.get_openai_client()

    for file_path in file_paths:
        typer.echo(f'Translating {file_path}')

        new_file_path = Path('docs', language, *file_path.parts[1:])
        content = utils.translate_file(client, file_path, language)
        utils.write_file(new_file_path, content)
