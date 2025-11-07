import os
import pathlib
import shutil
import tomllib

from openai import OpenAI

from translator import constants, types
from translator.config import Config


__all__ = [
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


def translate_file(
        client: OpenAI,
        path: pathlib.Path,
        language: types.LanguageType,
) -> str:

    content = get_file_content(path)
    language_name = get_language_name(language)

    instructions = f"""
        You are an English-to-{language_name} translator specializing in technical software documentation.
        Your task is to translate the provided English text into clear and natural {language_name}.
        When translating, retain English technical terms if they are commonly used or sound more natural than their {language_name} equivalents.
        Do not translate the module names: Data Anomalies, Data Analytics, Data Validation, Data Timeliness, Data Schema Tracker.
        Preserve all Markdown formatting from the original text.
        Do not change any file paths in the text.
        Provide only the translated content in your response.
        Do not include any comments, explanations, or questions.
    """

    response = client.responses.create(
        model='gpt-5-mini',
        instructions=instructions,
        input=content,
    )

    return response.output_text


def write_file(
        path: pathlib.Path,
        content: str,
) -> None:

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
