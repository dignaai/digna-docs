---
title: digna Python SDK-referanse 2026.06 | digna-dokumentasjon
description: Komplett referanse for digna Python SDK-utgivelse 2026.06
image: /assets/logo_square.png
---

# digna Python SDK-referanse 2026.06

Denne delen dokumenterer Python-SDK-et for ***digna***. Den er lagt opp som en referanse over flere sider: bruk denne oversikten til å forstå klienten, og fortsett deretter på de egne sidene om hurtigstart, ressurser, modeller, feil og den genererte API-dokumentasjonen.

SDK-et publiseres som pakken `digna-sdk` og tilbyr en stabil, versjonert klient for ***digna***s REST-API.

---

## SDK-grunnlag

---

### Oversikt

SDK-et bygger på et ressursorientert klientdesign. Hvert API-område eksponeres som en egen klient på den overordnede `DignaClient`, med typede forespørsels- og svarmodeller og enhetlig feilhåndtering.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Hovedfunksjoner

- **Typede modeller** — hver forespørsel og hvert svar valideres med pydantic, slik at editoren og typekontrollen fanger opp feil før kallet når nettverket.
- **Ressursorientert** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` og `client.inspection_statuses` tilbyr hver for seg enkle metoder for `list` / `get` / `create` / `update` / `delete`.
- **Tydelige feil** — API-feil gir `DignaAPIError` (eller en mer spesifikk underklasse som `DignaAuthenticationError`, `DignaAuthorizationError` eller `DignaNotFoundError`) i stedet for stille å returnere `None`.

### Installasjon

```bash
pip install digna-sdk
```

---

## Referansesider

Denne utgivelsen er fordelt på følgende sider:

- [Hurtigstart](quickstart.md) — koble til og gjøre de første kallene.
- [Ressurser](resources.md) — den fullstendige listen over tilgjengelige ressursklienter.
- [Modeller](models.md) — pydantic-modellene som brukes til inn- og utdata.
- [Feil](errors.md) — hierarkiet av unntak.
- [API-referanse](reference.md) — automatisk generert referansedokumentasjon.
