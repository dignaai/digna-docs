import typer

from translator import constants


def languages() -> None:

    for key, value in constants.LANGUAGES.items():
        typer.secho(f"{key}: ", fg=typer.colors.CYAN, nl=False)
        typer.echo(f"{value}")
