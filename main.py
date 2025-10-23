import typer

from translator import commands


app = typer.Typer()


app.command(name='languages')(commands.languages)
app.command(name='translate')(commands.translate)


if __name__ == '__main__':
    try:
        app()
    except Exception as error:
        typer.echo(str(error))
        typer.Exit(1)
