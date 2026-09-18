---
title: digna Python SDK-reference 2026.06 | digna-dokumentation
description: Komplet reference til digna Python SDK-udgivelse 2026.06
image: /assets/logo_square.png
---

# digna Python SDK-reference 2026.06

Dette afsnit dokumenterer Python-SDK'et til ***digna***. Det er bygget op som en reference over flere sider: brug denne oversigt til at forstå klienten, og fortsæt derefter på de særskilte sider om hurtig start, ressourcer, modeller, fejl og den genererede API-dokumentation.

SDK'et udgives som pakken `digna-sdk` og stiller en stabil, versioneret klient til rådighed for ***digna***s REST-API.

---

## SDK-grundbegreber

---

### Oversigt

SDK'et bygger på et ressourceorienteret klientdesign. Hvert API-område eksponeres som en selvstændig klient på den øverste `DignaClient` med typede forespørgsels- og svarmodeller og ensartet fejlhåndtering.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Kernefunktioner

- **Typede modeller** — hver forespørgsel og hvert svar valideres med pydantic, så din editor og din typekontrol fanger fejl, før kaldet rammer netværket.
- **Ressourceorienteret** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` og `client.inspection_statuses` stiller hver især enkle `list` / `get` / `create` / `update` / `delete`-metoder til rådighed.
- **Tydelige fejl** — API-fejl kaster `DignaAPIError` (eller en mere specifik underklasse som `DignaAuthenticationError`, `DignaAuthorizationError` eller `DignaNotFoundError`) i stedet for stiltiende at returnere `None`.

### Installation

```bash
pip install digna-sdk
```

---

## Referencesider

Denne udgivelse er fordelt på følgende sider:

- [Hurtig start](quickstart.md) — opret forbindelse, og foretag de første kald.
- [Ressourcer](resources.md) — den fulde liste over tilgængelige ressourceklienter.
- [Modeller](models.md) — de pydantic-modeller, der bruges til input og output.
- [Fejl](errors.md) — hierarkiet af undtagelser.
- [API-reference](reference.md) — automatisk genereret referencedokumentation.
