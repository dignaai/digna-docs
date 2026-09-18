# digna Python SDK-referentie 2026.06

Dit onderdeel documenteert de Python SDK voor ***digna***. Het is opgezet als een referentie over meerdere pagina's: gebruik dit overzicht om de client te begrijpen en ga daarna verder met de aparte pagina's over de snelstart, resources, modellen, fouten en de gegenereerde API-documentatie.

De SDK wordt gepubliceerd als het pakket `digna-sdk` en biedt een stabiele, geversioneerde client voor de ***digna*** REST API.

---

## SDK-basis

---

### Overzicht

De SDK volgt een resourcegericht clientontwerp. Elk API-gebied wordt als volwaardige client aangeboden op de bovenliggende `DignaClient`, met getypeerde request- en responsmodellen en consistente foutafhandeling.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Belangrijkste functies

- **Getypeerde modellen** — elk request en elke response wordt gevalideerd met pydantic, zodat uw editor en typechecker fouten opmerken voordat er netwerkverkeer plaatsvindt.
- **Resourcegericht** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` en `client.inspection_statuses` bieden elk eenvoudige `list` / `get` / `create` / `update` / `delete`-methoden.
- **Duidelijke fouten** — API-fouten werpen `DignaAPIError` op (of een specifiekere subklasse zoals `DignaAuthenticationError`, `DignaAuthorizationError` of `DignaNotFoundError`) in plaats van stilzwijgend `None` terug te geven.

### Installatie

```bash
pip install digna-sdk
```

---

## Referentiepagina's

Deze release is verdeeld over de volgende pagina's:

- [Snelstart](quickstart.md) — verbinding maken en de eerste aanroepen doen.
- [Resources](resources.md) — de volledige lijst met beschikbare resourceclients.
- [Modellen](models.md) — de pydantic-modellen die voor invoer en uitvoer worden gebruikt.
- [Fouten](errors.md) — de hiërarchie van excepties.
- [API-referentie](reference.md) — automatisch gegenereerde referentiedocumentatie.