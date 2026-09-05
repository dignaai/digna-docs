"""Structural checks run on every translated page before it is written.

A translation that reads well but breaks the page is worse than no
translation, and each of the checks below corresponds to a defect this
tool has actually shipped to production:

* ``frontmatter``  — 28 pages were published with no frontmatter block at
  all, so they had no meta description and no og:image and fell back to
  the generic site description.
* ``yaml``         — two pages had a value beginning with ``*`` (``*digna*
  monitorizeaza…``). YAML reads that as an alias, MkDocs swallows the
  parse error and returns *empty* metadata, so the Romanian homepage
  served no title, description or Open Graph tags whatsoever.
* ``fences``       — an unbalanced ``` in a page mis-pairs every fence
  after it, printing code as prose and prose as code.
* ``anchors``      — heading ``{: #id }`` attributes are in-page link
  targets; translating them breaks the table of contents.
* ``links``        — link targets are paths, not prose, and must survive
  translation unchanged.
* ``headings``     — a dropped or added heading means content was lost or
  invented.

Each check returns None when it passes, or a short instruction that is fed
back to the model on the retry.
"""

from __future__ import annotations

import re

import yaml


__all__ = ["check", "repair_yaml_scalars", "FRONTMATTER_RE"]


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)

# A leading character that makes YAML read a bare scalar as something other
# than a string: alias, anchor, flow collection, block scalar, tag, comment.
_UNSAFE_LEAD = ("*", "&", "[", "{", ">", "|", "%", "@", "`", "!", "#")


def repair_yaml_scalars(text: str) -> str:
    """Quote frontmatter values YAML would otherwise misread.

    Applied unconditionally rather than asked for in the prompt: the model
    cannot be relied on to remember, and the failure is silent.
    """
    match = FRONTMATTER_RE.match(text)
    if not match:
        return text

    out = []
    for line in match.group(1).split("\n"):
        pair = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):[ \t]+(\S.*)$", line)
        if pair and pair.group(2).lstrip().startswith(_UNSAFE_LEAD):
            value = pair.group(2).rstrip()
            if '"' not in value:
                value = f'"{value}"'
            elif "'" not in value:
                value = f"'{value}'"
            else:
                value = '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
            line = f"{pair.group(1)}: {value}"
        out.append(line)

    return text[: match.start(1)] + "\n".join(out) + text[match.end(1) :]


def _fence_lines(text: str) -> int:
    return sum(1 for line in text.split("\n") if re.match(r"^\s*```", line))


def _anchor_ids(text: str) -> list[str]:
    return sorted(re.findall(r"\{:\s*#([A-Za-z0-9_-]+)\s*\}", text))


def _link_targets(text: str) -> list[str]:
    # Markdown inline links only; reference definitions are not used here.
    return sorted(re.findall(r"\]\(([^)\s]+)", text))


def _headings(text: str) -> int:
    body = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    return len(re.findall(r"^#{1,6} ", body, re.M))


def _admonitions(text: str) -> list[str]:
    """The admonition *types* in order — titles are translated, types are not."""
    return re.findall(r"^!!! (\w+)", text, re.M)


def check(source: str, translated: str) -> list[str]:
    """Return a list of problems; empty means the translation is structurally sound."""
    problems: list[str] = []

    src_fm = FRONTMATTER_RE.match(source)
    out_fm = FRONTMATTER_RE.match(translated)

    if src_fm and not out_fm:
        problems.append(
            "The source begins with a YAML frontmatter block delimited by ---. "
            "Your output dropped it. Reproduce the block, translating only the "
            "human-readable values."
        )
    elif src_fm and out_fm:
        try:
            src_keys = set(yaml.safe_load(src_fm.group(1)) or {})
        except yaml.YAMLError:
            src_keys = set()
        try:
            out_keys = set(yaml.safe_load(out_fm.group(1)) or {})
        except yaml.YAMLError as error:
            problems.append(
                f"The frontmatter is not valid YAML ({str(error).splitlines()[0]}). "
                "Wrap any value containing special characters in double quotes."
            )
            out_keys = set()
        missing = src_keys - out_keys
        if missing:
            problems.append(
                "The frontmatter is missing these keys: "
                + ", ".join(sorted(missing))
                + ". Keep every key from the source."
            )

    src_fences, out_fences = _fence_lines(source), _fence_lines(translated)
    if out_fences % 2:
        problems.append(
            "A fenced code block was left unclosed — the ``` markers must come "
            "in pairs. Reproduce every fence from the source."
        )
    elif src_fences != out_fences:
        problems.append(
            f"The source has {src_fences} ``` fence markers, your output has "
            f"{out_fences}. Reproduce every code block exactly."
        )

    if _anchor_ids(source) != _anchor_ids(translated):
        problems.append(
            "Heading id attributes of the form {: #some-id } must be copied "
            "character for character. Do not translate or drop them."
        )

    src_links, out_links = _link_targets(source), _link_targets(translated)
    if src_links != out_links:
        changed = sorted(set(src_links) ^ set(out_links))[:6]
        problems.append(
            "Link targets must not be translated — only the link text. "
            "These differ: " + ", ".join(changed)
        )

    src_adm, out_adm = _admonitions(source), _admonitions(translated)
    if src_adm != out_adm:
        problems.append(
            f"Admonition blocks must be preserved: the source opens {len(src_adm)} "
            f"({', '.join(src_adm) or 'none'}), your output {len(out_adm)} "
            f"({', '.join(out_adm) or 'none'}). Keep the `!!! type` marker and its "
            "type in English, translate only the quoted title, and keep the body "
            "indented by four spaces."
        )

    src_h, out_h = _headings(source), _headings(translated)
    if src_h != out_h:
        problems.append(
            f"The source has {src_h} headings, your output has {out_h}. "
            "Translate every heading; do not add, drop or merge any."
        )

    return problems
