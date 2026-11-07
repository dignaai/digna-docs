"""Generate the REST API Reference resource pages from a snapshot of the stable v1 OpenAPI document.

The digna backend serves the document at /api-docs/stable/v1/openapi.json. For a new release, save
it as docs/rest_api/Release <YYYY.MM>/openapi.json and run:

    python scripts/gen_rest_api_reference.py "docs/rest_api/Release <YYYY.MM>"

One page is written per OpenAPI tag. The Overview (index.md) is written by hand and left alone.
The generated pages are English only, like the SDK API pages that mkdocstrings renders.
"""
import json
import re
import sys
from pathlib import Path

# Page per tag, in nav order: (tag, file name, page title, introduction).
PAGES = [
    ("projects", "projects.md", "Projects",
     "Projects group database connections and data sources. The API reads projects; create and "
     "change them in the dashboard."),
    ("db-connections", "db_connections.md", "DB Connections",
     "Database connections of a project. The API reads them, without connection properties or "
     "secrets; create and change them in the dashboard."),
    ("data-sources", "data_sources.md", "Data Sources",
     "Data sources are the tables, views and queries *digna* inspects. Create, read, update and "
     "delete them."),
    ("data-sets", "data_sets.md", "Data Sets",
     "Datasets split a data source into segments that *digna* monitors separately."),
    ("attributes", "attributes.md", "Attributes",
     "Attributes are the columns, and the query attributes, that *digna* profiles in a data "
     "source."),
    ("check-definitions", "check_definitions.md", "Check Definitions",
     "Check definitions are the statistics *digna* calculates and checks for a data source."),
    ("inspection-requests", "inspection_requests.md", "Inspection Requests",
     "Inspection requests run inspections for a range of dates, like an inspection started from "
     "the Inspection Hub."),
    ("inspection-statuses", "inspection_statuses.md", "Inspection Statuses",
     "Inspection statuses report the result of each inspected day per project, data source and "
     "dataset."),
]

# Integer enums whose values the document doesn't name.
ENUM_MEANINGS = {
    "InspectionStatus": {-1: "no status", 0: "OK", 1: "warning", 2: "critical"},
    "TestStatus": {-1: "not tested", 0: "passed", 1: "uncertain", 2: "failed"},
}

SUCCESS = ("200", "201", "204")


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def ref_name(ref):
    return ref.rsplit("/", 1)[-1]


class Doc:
    def __init__(self, spec):
        self.spec = spec
        self.schemas = spec["components"]["schemas"]

    def type_of(self, s, links=True):
        """A schema's type as Markdown, and whether it allows null."""
        nullable = False
        if "oneOf" in s or "anyOf" in s:
            parts = [p for p in s.get("oneOf", s.get("anyOf")) if p.get("type") != "null"]
            nullable = len(parts) < len(s.get("oneOf", s.get("anyOf")))
            text = " or ".join(self.type_of(p, links)[0] for p in parts)
            return text, nullable
        if "$ref" in s:
            n = ref_name(s["$ref"])
            return (f"[{n}](#{slug(n)})" if links else n), False
        t = s.get("type", "object")
        if isinstance(t, list):
            nullable = "null" in t
            t = next((x for x in t if x != "null"), "null")
        if t == "array":
            inner, _ = self.type_of(s.get("items", {}), links)
            text = f"array of {inner}"
        else:
            text = t
            if "format" in s and s["format"] not in ("int32", "int64"):
                text += f" ({s['format']})"
        return text, nullable

    def description(self, s):
        d = s.get("description", "")
        for p in s.get("oneOf", []) + s.get("anyOf", []):
            d = d or p.get("description", "")
        return " ".join(d.split())

    def reachable(self, start):
        """Schema names reachable from a set of schemas or inline fragments, in first-seen order."""
        seen, order, stack = set(), [], list(start)
        while stack:
            x = stack.pop(0)
            if isinstance(x, dict):
                if "$ref" in x:
                    n = ref_name(x["$ref"])
                    if n not in seen:
                        seen.add(n)
                        order.append(n)
                        stack.append(self.schemas[n])
                for k, v in x.items():
                    if k != "$ref":
                        stack.append(v)
            elif isinstance(x, list):
                stack.extend(x)
        return order

    def example_value(self, s, depth=0, key=None):
        if "oneOf" in s or "anyOf" in s:
            parts = [p for p in s.get("oneOf", s.get("anyOf")) if p.get("type") != "null"]
            return self.example_value(parts[0], depth, key) if parts else None
        if "$ref" in s:
            return self.example_value(self.schemas[ref_name(s["$ref"])], depth, key)
        if "enum" in s:
            return s["enum"][0]
        t = s.get("type", "object")
        if isinstance(t, list):
            t = next((x for x in t if x != "null"), "null")
        if t == "object":
            if depth > 3:
                return {}
            req = s.get("required", [])
            return {k: self.example_value(v, depth + 1, k)
                    for k, v in s.get("properties", {}).items() if k in req}
        if t == "array":
            return [self.example_value(s.get("items", {}), depth + 1, key)]
        if t == "integer":
            return 1
        if t == "number":
            return 1.0
        if t == "boolean":
            return False
        if s.get("format") == "date":
            return "2026-11-01"
        return f"<{key}>" if key else "<value>"

    def operation(self, method, path, op):
        out = []
        ok = next((c for c in SUCCESS if c in op["responses"]), None)
        heading = op["responses"][ok]["description"] if ok else op["operationId"]
        out.append(f"## {heading} {{: #{slug(op['operationId'])} }}\n")
        out.append(f"```http\n{method.upper()} {path}\n```\n")

        params = op.get("parameters", [])
        if params:
            out.append("**Parameters**\n")
            out.append("| Name | In | Type | Required | Description |")
            out.append("|---|---|---|---|---|")
            for p in params:
                t, _ = self.type_of(p.get("schema", {}))
                out.append(f"| `{p['name']}` | {p['in']} | {t} | {'Yes' if p.get('required') else 'No'} "
                           f"| {' '.join(p.get('description', '').split())} |")
            out.append("")

        body = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
        if body:
            t, _ = self.type_of(body)
            out.append(f"**Request body**: {t}\n")

        out.append("**Responses**\n")
        out.append("| Status | Description | Body |")
        out.append("|---|---|---|")
        for code, r in sorted(op["responses"].items()):
            sch = r.get("content", {}).get("application/json", {}).get("schema")
            t = self.type_of(sch)[0] if sch else "—"
            out.append(f"| `{code}` | {' '.join(r.get('description', '').split())} | {t} |")
        out.append("")

        url = "https://digna.example.com" + re.sub(r"\{(\w+)\}", r"<\1>", path)
        req_q = [p for p in params if p["in"] == "query" and p.get("required")]
        if req_q:
            url += "?" + "&".join(f"{p['name']}=<{p['name']}>" for p in req_q)
        lines = [f"curl -X {method.upper()} '{url}'", "  -H \"Authorization: Bearer $DIGNA_API_KEY\""]
        if body:
            ex = json.dumps(self.example_value(body), indent=2)
            lines.append("  -H 'Content-Type: application/json'")
            lines.append("  -d '" + ex.replace("\n", "\n  ") + "'")
        out.append("**Example**\n")
        out.append("```bash\n" + " \\\n".join(lines) + "\n```\n")
        return "\n".join(out)

    def schema_section(self, name):
        s = self.schemas[name]
        out = [f"### {name} {{: #{slug(name)} }}\n"]
        if "enum" in s:
            meanings = ENUM_MEANINGS.get(name, {})
            vals = ", ".join(f"`{v}`" + (f" ({meanings[v]})" if v in meanings else "") for v in s["enum"])
            out.append(f"One of: {vals}.\n")
            return "\n".join(out)
        props = s.get("properties", {})
        if not props:
            t, _ = self.type_of(s)
            out.append(f"{t}.\n")
            return "\n".join(out)
        req = set(s.get("required", []))
        out.append("| Field | Type | Required | Description |")
        out.append("|---|---|---|---|")
        for k, v in props.items():
            t, nullable = self.type_of(v)
            if nullable:
                t += ", nullable"
            out.append(f"| `{k}` | {t} | {'Yes' if k in req else 'No'} | {self.description(v)} |")
        out.append("")
        return "\n".join(out)

    def page(self, tag, title, intro, release):
        ops = [(m, p, o) for p, item in self.spec["paths"].items()
               for m, o in item.items() if tag in o.get("tags", [])]
        order = {"get": 0, "post": 1, "put": 2, "delete": 3}
        ops.sort(key=lambda x: (x[1].count("/"), "{" in x[1], order.get(x[0], 9)))
        out = ["---",
               f"title: {title} – REST API Reference {release} | digna Documentation",
               f"description: digna REST API v1 reference for {title.lower()} — endpoints, parameters, "
               f"request bodies, responses and schemas, generated from the API's OpenAPI document.",
               "image: /assets/logo_square.png",
               "---", "",
               "<!-- Generated by scripts/gen_rest_api_reference.py from openapi.json. Do not edit. -->", "",
               f"# {title}\n",
               intro + " Authentication, pagination and errors are described in the "
               "[Overview](index.md).\n",
               "| Method | Path | Description |", "|---|---|---|"]
        for m, p, o in ops:
            ok = next((c for c in SUCCESS if c in o["responses"]), None)
            desc = o["responses"][ok]["description"] if ok else o["operationId"]
            out.append(f"| `{m.upper()}` | `{p}` | [{desc}](#{slug(o['operationId'])}) |")
        out.append("\n---\n")
        for m, p, o in ops:
            out.append(self.operation(m, p, o))
            out.append("---\n")
        names = self.reachable([o for _, _, o in ops])
        if names:
            out.append("## Schemas {: #schemas }\n")
            for n in names:
                out.append(self.schema_section(n))
        return "\n".join(out).rstrip() + "\n"


def main(folder):
    folder = Path(folder)
    doc = Doc(json.loads((folder / "openapi.json").read_text()))
    release = folder.name.removeprefix("Release ")
    tags = {t for item in doc.spec["paths"].values() for o in item.values() for t in o.get("tags", [])}
    missing = tags - {p[0] for p in PAGES}
    if missing:
        sys.exit(f"Tags without a page in PAGES: {', '.join(sorted(missing))}")
    for tag, fname, title, intro in PAGES:
        (folder / fname).write_text(doc.page(tag, title, intro, release))
        print("wrote", folder / fname)


if __name__ == "__main__":
    main(sys.argv[1])
