---
title: digna Python SDK rokasgrāmata 2026.06 | digna dokumentācija
description: Pilnīga digna Python SDK 2026.06 laidiena rokasgrāmata
image: /assets/logo_square.png
---

# digna Python SDK rokasgrāmata 2026.06

Šajā sadaļā ir dokumentēts ***digna*** Python SDK. Tā ir veidota kā vairāku lappušu rokasgrāmata: izmantojiet šo pārskatu, lai izprastu klientu, un pēc tam turpiniet ar atsevišķām lappusēm par ātro sākumu, resursiem, modeļiem, kļūdām un ģenerēto API dokumentāciju.

SDK tiek publicēts kā pakotne `digna-sdk` un piedāvā stabilu, versionētu klientu ***digna*** REST API.

---

## SDK pamati

---

### Pārskats

SDK pamatā ir uz resursiem orientēts klienta dizains. Katra API joma tiek piedāvāta kā atsevišķs klients augstākā līmeņa objektā `DignaClient`, ar tipizētiem pieprasījumu un atbilžu modeļiem un vienotu kļūdu apstrādi.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Galvenās iespējas

- **Tipizēti modeļi** — katrs pieprasījums un katra atbilde tiek validēta ar pydantic, tāpēc redaktors un tipu pārbaudītājs pamana kļūdas vēl pirms tīkla izsaukuma.
- **Orientācija uz resursiem** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` un `client.inspection_statuses` katrs piedāvā vienkāršas metodes `list` / `get` / `create` / `update` / `delete`.
- **Skaidras kļūdas** — API kļūdas izraisa `DignaAPIError` (vai konkrētāku apakšklasi, piemēram, `DignaAuthenticationError`, `DignaAuthorizationError` vai `DignaNotFoundError`), nevis klusējot atgriež `None`.

### Instalēšana

```bash
pip install digna-sdk
```

---

## Rokasgrāmatas lappuses

Šis laidiens ir sadalīts šādās lappusēs:

- [Ātrais sākums](quickstart.md) — izveidot savienojumu un veikt pirmos izsaukumus.
- [Resursi](resources.md) — pilns pieejamo resursu klientu saraksts.
- [Modeļi](models.md) — ievadei un izvadei izmantotie pydantic modeļi.
- [Kļūdas](errors.md) — izņēmumu hierarhija.
- [API rokasgrāmata](reference.md) — automātiski ģenerēta rokasgrāmatas dokumentācija.
