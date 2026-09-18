# digna Python SDK Referenz 2026.06

Dieser Abschnitt dokumentiert das Python SDK für ***digna***. Er ist als mehrseitige Referenz aufgebaut: Nutzen Sie diese Übersicht, um den Client zu verstehen, und lesen Sie dann auf den eigenen Seiten zu Quickstart, Ressourcen, Modellen, Fehlern und der generierten API-Dokumentation weiter.

Das SDK wird als Paket `digna-sdk` veröffentlicht und stellt einen stabilen, versionierten Client für die ***digna*** REST-API bereit.

---

## SDK-Grundlagen

---

### Überblick

Das SDK folgt einem ressourcenorientierten Client-Design. Jeder API-Bereich wird als eigenständiger Client auf dem obersten `DignaClient` bereitgestellt – mit typisierten Request- und Response-Modellen und einheitlicher Fehlerbehandlung.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Kernfunktionen

- **Typisierte Modelle** — jeder Request und jede Response wird mit pydantic validiert, sodass Ihr Editor und Ihr Type-Checker Fehler erkennen, bevor der Aufruf das Netzwerk erreicht.
- **Ressourcenorientiert** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` und `client.inspection_statuses` stellen jeweils einfache `list` / `get` / `create` / `update` / `delete`-Methoden bereit.
- **Klare Fehler** — API-Fehler lösen `DignaAPIError` aus (oder eine spezifischere Unterklasse wie `DignaAuthenticationError`, `DignaAuthorizationError` oder `DignaNotFoundError`), statt stillschweigend `None` zurückzugeben.

### Installation

```bash
pip install digna-sdk
```

---

## Referenzseiten

Dieses Release ist auf die folgenden Seiten aufgeteilt:

- [Quickstart](quickstart.md) — verbinden und die ersten Aufrufe absetzen.
- [Ressourcen](resources.md) — die vollständige Liste der verfügbaren Ressourcen-Clients.
- [Modelle](models.md) — die für Ein- und Ausgabe verwendeten pydantic-Modelle.
- [Fehler](errors.md) — die Ausnahmehierarchie.
- [API-Referenz](reference.md) — automatisch generierte Referenzdokumentation.