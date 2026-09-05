import os
import pathlib
import shutil
import tomllib

from openai import OpenAI

from translator import constants, types, validation
from translator.config import Config


__all__ = [
    'build_instructions',
    'delete_folder',
    'list_md_files',
    'get_config',
    'get_openai_client',
    'get_file_content',
    'get_language_name',
    'translate_file',
    'write_file',
]


def cleanup_folder(
        language: types.LanguageType
) -> None:

    file_paths = list_md_files(language)

    for file_path in file_paths:
        main_file_path = pathlib.Path(file_path.parts[0], *file_path.parts[2:])
        if not os.path.exists(main_file_path):
            os.remove(file_path)


def delete_folder(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)


def list_md_files(
        language: types.LanguageType | None = None,
        match: str | None = None,
) -> list[pathlib.Path]:

    path = 'docs'

    if language:
        path = os.path.join(path, language)

    folder = pathlib.Path(path)
    file_paths = list(folder.rglob('*.md'))

    file_paths_final = []

    for file_path in file_paths:
        if not language:
            part = str(file_path.parts[1])
            if part not in constants.MAIN_FOLDERS and not part.endswith('.md'):
                continue

        if match and match not in str(file_path):
            continue

        file_paths_final.append(file_path)

    return file_paths_final


def get_config() -> Config:

    with open('config.toml', 'rb') as f:
        config_dict = tomllib.load(f)

    return Config(**config_dict)


def get_openai_client() -> OpenAI:

    config = get_config()

    return OpenAI(api_key=config.api_key)


def get_file_content(path: pathlib.Path) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def get_language_name(
        language: types.LanguageType,
) -> str:
    return constants.LANGUAGES[language]


def build_instructions(language_name: str) -> str:
    return f"""
        You are an English-to-{language_name} translator specializing in technical software documentation.
        Your task is to translate the provided English text into clear and natural {language_name}.
        When translating, retain English technical terms if they are commonly used or sound more natural than their {language_name} equivalents.
        Do not translate the module names: Data Anomalies, Data Analytics, Data Validation, Data Timeliness, Data Schema Tracker.
        Preserve all Markdown formatting from the original text.
        Do not change any file paths in the text.
        Headings may end with an explicit id attribute like "{{: #some-id }}" (curly braces containing a hash and a slug). Keep these attributes character-for-character identical, including the slug — they are anchor targets that in-page links depend on and must not be translated or altered.

        Structural rules — breaking any of these breaks the published page:
        - If the document starts with a YAML frontmatter block between --- lines, reproduce that block with every key intact. Translate only the human-readable values (title, description, keywords); never drop the block and never rename a key.
        - In frontmatter, wrap any value that starts with *, &, [, {{, >, |, # or @ in double quotes. Unquoted, YAML reads it as something other than text and the whole block is silently discarded.
        - Translate every heading, including section headings. Do not leave headings in English.
        - Reproduce every fenced code block. The ``` markers must stay balanced and equal in number to the source. Translate comments inside code only where that is safe; never translate commands, identifiers or paths.
        - Translate link text but never link targets: `[text](target)` keeps its target byte for byte, including #anchors.

        Provide only the translated content in your response.
        Do not include any comments, explanations, or questions.
    """


def translate_file(
        client: OpenAI,
        path: pathlib.Path,
        language: types.LanguageType,
        attempts: int = 3,
) -> tuple[str, list[str]]:
    """Translate a page, retrying while it fails the structural checks.

    Returns the content and any problems that survived the final attempt, so
    the caller can report pages that need a human look rather than silently
    publishing a broken one.
    """

    content = get_file_content(path)
    instructions = build_instructions(get_language_name(language))

    best: str = ''
    problems: list[str] = []

    for attempt in range(attempts):
        prompt = content
        if problems:
            prompt = (
                'Your previous translation of this document had these problems:\n'
                + '\n'.join(f'- {p}' for p in problems)
                + '\n\nTranslate the document again, fixing them.\n\n'
                + content
            )

        response = client.responses.create(
            model='gpt-5-mini',
            instructions=instructions,
            input=prompt,
        )

        # Applied every time: the model cannot be trusted to remember the
        # quoting rule, and an unquoted alias fails silently at build time.
        best = validation.repair_yaml_scalars(response.output_text)

        problems = validation.check(content, best)
        if not problems:
            return best, []

    return best, problems


def write_file(
        path: pathlib.Path,
        content: str,
) -> None:

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
