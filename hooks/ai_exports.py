"""Machine-readable companions to the rendered HTML, for LLMs and AI agents.

Three artefacts are emitted, all derived from what MkDocs already knows, so
nothing here needs hand-maintaining as pages come and go:

* ``<page>.md`` and ``<page>/index.md`` — the raw Markdown source of every
  page, so an agent can fetch prose instead of scraping rendered HTML.
  Both spellings are written because MkDocs runs with directory URLs: a
  reader who appends ``.md`` to ``/databases/snowflake_connector_guide/``
  and one who trims the slash first both land on a real file.

* ``llms.txt`` — the llmstxt.org index: the site's nav, flattened to a
  linked list with each page's own ``description`` frontmatter.

* ``llms-full.txt`` — every page's Markdown concatenated, for ingestion in
  a single request.

All three are written **per locale**. mkdocs-static-i18n runs one build pass
per language, and each pass re-enters these events with only that language's
pages, so /de/llms.txt describes the German site using German descriptions.
That is the point of doing this by hook rather than by hand: 27 indexes stay
correct for free.
"""

from __future__ import annotations

import os
import posixpath

# Pages accumulated during the current build pass. mkdocs-static-i18n
# triggers on_post_build once per language, and the list is reset each time
# (see on_post_build) so locales never bleed into one another.
_pages: list = []

# The resolved navigation for the current pass. on_post_build is not handed
# the nav, so it is captured here while it is available.
_nav: list = []


def _dest_dir(config) -> str:
    return config["site_dir"]


def on_pre_build(config, **kwargs) -> None:
    _pages.clear()
    _nav.clear()


def on_nav(nav, config, files, **kwargs):
    _nav.clear()
    _nav.extend(nav.items)
    return nav


def on_post_page(output: str, page, config, **kwargs) -> str:
    """Write the page's Markdown next to its HTML and record it for the index."""
    if not page.markdown:
        return output

    dest = page.file.dest_path.replace(os.sep, "/")
    if not dest.endswith(".html"):
        return output

    body = page.markdown
    site_dir = _dest_dir(config)

    # …/page/index.html -> …/page/index.md and …/page.md
    targets = [dest[: -len(".html")] + ".md"]
    if dest.endswith("/index.html"):
        targets.append(dest[: -len("/index.html")] + ".md")

    for target in targets:
        path = os.path.join(site_dir, target.replace("/", os.sep))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(body)

    _pages.append(page)
    return output


def _locale_prefix(pages) -> str:
    """The build pass's URL prefix: "" for the default language, else "de/"…

    Derived from the homepage's destination rather than from config, because
    the i18n plugin rewrites destinations but leaves the base config alone.
    """
    for page in pages:
        dest = page.file.dest_path.replace(os.sep, "/")
        if dest == "index.html":
            return ""
        if dest.endswith("/index.html") and dest.count("/") == 1:
            return dest.split("/")[0] + "/"
    return ""


def _summary(pages, config) -> str:
    for page in pages:
        dest = page.file.dest_path.replace(os.sep, "/")
        if dest == "index.html" or (dest.endswith("/index.html") and dest.count("/") == 1):
            meta = page.meta or {}
            if meta.get("description"):
                return str(meta["description"])
    return config.get("site_description") or ""


def _walk(items, depth: int = 0):
    """Yield (depth, item) for the nav tree, sections included."""
    for item in items or []:
        yield depth, item
        if getattr(item, "children", None):
            yield from _walk(item.children, depth + 1)


def on_post_build(config, **kwargs) -> None:
    if not _pages:
        return

    # Page URLs already carry the locale prefix during a localised pass, so
    # the base is the bare site root; the prefix is only used to choose the
    # directory these files are written into.
    site_url = (config.get("site_url") or "").rstrip("/")
    prefix = _locale_prefix(_pages)
    base = f"{site_url}/" if site_url else "/"
    out_dir = os.path.join(config["site_dir"], prefix.rstrip("/").replace("/", os.sep))
    os.makedirs(out_dir, exist_ok=True)

    by_url = {p.url: p for p in _pages}

    lines = [f"# {config['site_name']}", ""]
    summary = _summary(_pages, config)
    if summary:
        lines += [f"> {summary}", ""]

    body: list[str] = []
    for depth, item in _walk(_nav):
        title = (item.title or "").strip()
        if not title:
            continue
        if getattr(item, "is_section", False):
            if depth == 0:
                body += ["", f"## {title}", ""]
            else:
                body += ["", f"### {title}", ""]
            continue
        if not getattr(item, "is_page", False):
            continue
        page = by_url.get(item.url)
        if page is None:
            continue
        desc = (page.meta or {}).get("description", "")
        url = f"{base}{item.url}"
        # Angle brackets keep URLs containing spaces valid in Markdown.
        link = f"<{url}>" if " " in url else url
        body.append(f"- [{title}]({link})" + (f": {desc}" if desc else ""))

    lines += body + [""]

    # Notes: generated rather than written by hand so the language list can
    # never drift from the set actually being built.
    alternates = [a for a in (config.get("extra", {}).get("alternate") or []) if a.get("lang")]
    notes = ["", "## Notes", ""]
    notes.append(
        "- Every page is also available as raw Markdown: append `.md` to its URL, "
        "e.g. `" + base + "platform/overview.md`."
    )
    notes.append("- `llms-full.txt` beside this file carries the full text of every page in one request.")
    if len(alternates) > 1:
        langs = ", ".join(f"`/{a['lang']}/`" for a in alternates if a["lang"] != "en")
        notes.append(
            f"- This documentation is published in {len(alternates)} languages under a locale "
            f"prefix ({langs}). Each locale has its own `llms.txt`. "
            f"The sitemap at {base}sitemap.xml lists every URL."
        )
    notes.append(
        "- The marketing site at https://www.digna.ai covers use cases, industry "
        "applications and company information not duplicated here."
    )
    lines += notes + [""]

    with open(os.path.join(out_dir, "llms.txt"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines).replace("\n\n\n", "\n\n"))

    full = [f"# {config['site_name']}", ""]
    if summary:
        full += [f"> {summary}", ""]
    for page in _pages:
        full += ["", "---", "", f"# {page.title}", f"Source: {base}{page.url}", "", page.markdown]
    with open(os.path.join(out_dir, "llms-full.txt"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(full))

    _pages.clear()
