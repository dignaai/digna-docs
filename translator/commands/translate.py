import concurrent.futures
import threading
import typing
from pathlib import Path

import typer

from translator import constants, types, utils


__all__ = ['translate']


def _translate_one(client, file_path: Path, language: str) -> tuple[Path, str, list[str]]:
    content, problems = utils.translate_file(client, file_path, language)
    return file_path, content, problems


def translate(
        language: typing.Annotated[str, typer.Argument(help='The language to translate into, or "all" for every configured language.')],
        match: typing.Annotated[str | None, typer.Argument(help='Translates only matching files.')] = None,
        workers: typing.Annotated[int, typer.Option(help='Pages translated in parallel. Lower this if the API rate-limits.')] = 6,
) -> None:

    if language == 'all':
        languages = [code for code in constants.LANGUAGES if code != 'en']
    else:
        if language not in constants.LANGUAGES:
            raise typer.BadParameter(f'Unknown language {language!r}.')
        languages = [language]

    client = utils.get_openai_client()
    file_paths = utils.list_md_files(match=match)

    total = len(file_paths) * len(languages)
    typer.echo(f'Translating {len(file_paths)} pages into {len(languages)} language(s) — {total} calls.')

    # Pages that still fail the structural checks after every retry. These are
    # written anyway (a flawed translation beats a missing page) but reported
    # at the end so they can be looked at rather than silently published.
    failures: list[tuple[str, Path, list[str]]] = []
    lock = threading.Lock()
    done = 0

    for lang in languages:
        utils.cleanup_folder(lang)
        typer.echo(f'\n=== {lang} ({utils.get_language_name(lang)}) ===')

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(_translate_one, client, path, lang): path
                for path in file_paths
            }
            for future in concurrent.futures.as_completed(futures):
                path = futures[future]
                try:
                    file_path, content, problems = future.result()
                except Exception as error:  # noqa: BLE001 - one page must not stop the run
                    with lock:
                        failures.append((lang, path, [f'{type(error).__name__}: {error}']))
                        done += 1
                        typer.echo(f'  [{done}/{total}] ERROR {path} — {error}')
                    continue

                utils.write_file(Path('docs', lang, *file_path.parts[1:]), content)

                with lock:
                    done += 1
                    if problems:
                        failures.append((lang, file_path, problems))
                        typer.echo(f'  [{done}/{total}] {file_path}  ⚠ {len(problems)} unresolved')
                    else:
                        typer.echo(f'  [{done}/{total}] {file_path}')

    typer.echo(f'\nDone: {total - len(failures)}/{total} pages passed all structural checks.')
    if failures:
        typer.echo(f'\n{len(failures)} page(s) need review:')
        for lang, path, problems in failures:
            typer.echo(f'  {lang}/{path}')
            for problem in problems:
                typer.echo(f'      - {problem}')
