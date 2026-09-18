# digna Python SDK-referens 2026.06

Det här avsnittet dokumenterar Python-SDK:t för ***digna***. Det är upplagt som en referens över flera sidor: använd översikten för att förstå klienten och fortsätt sedan till de egna sidorna om snabbstart, resurser, modeller, fel och den genererade API-dokumentationen.

SDK:t publiceras som paketet `digna-sdk` och tillhandahåller en stabil, versionshanterad klient för ***digna***s REST-API.

---

## SDK-grunder

---

### Översikt

SDK:t bygger på en resursorienterad klientdesign. Varje API-område exponeras som en egen klient på den överordnade `DignaClient`, med typade request- och response-modeller och enhetlig felhantering.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Huvudfunktioner

- **Typade modeller** — varje request och response valideras med pydantic, så att din editor och din typkontroll fångar misstag innan anropet når nätverket.
- **Resursorienterat** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` och `client.inspection_statuses` exponerar var för sig enkla metoder för `list` / `get` / `create` / `update` / `delete`.
- **Tydliga fel** — API-fel ger `DignaAPIError` (eller en mer specifik subklass som `DignaAuthenticationError`, `DignaAuthorizationError` eller `DignaNotFoundError`) i stället för att tyst returnera `None`.

### Installation

```bash
pip install digna-sdk
```

---

## Referenssidor

Den här releasen är uppdelad på följande sidor:

- [Snabbstart](quickstart.md) — anslut och gör dina första anrop.
- [Resurser](resources.md) — hela listan över tillgängliga resursklienter.
- [Modeller](models.md) — de pydantic-modeller som används för in- och utdata.
- [Fel](errors.md) — hierarkin av undantag.
- [API-referens](reference.md) — automatiskt genererad referensdokumentation.