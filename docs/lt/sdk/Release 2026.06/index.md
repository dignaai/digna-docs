---
title: digna Python SDK žinynas 2026.06 | digna dokumentacija
description: Išsamus digna Python SDK 2026.06 laidos žinynas
image: /assets/logo_square.png
---

# digna Python SDK žinynas 2026.06

Šiame skyriuje aprašomas ***digna*** Python SDK. Jis sudarytas kaip kelių puslapių žinynas: iš šios apžvalgos susipažinsite su klientu, o paskui galėsite tęsti atskiruose puslapiuose apie greitąją pradžią, išteklius, modelius, klaidas ir sugeneruotą API dokumentaciją.

SDK platinamas kaip paketas `digna-sdk` ir suteikia stabilų, versijuojamą ***digna*** REST API klientą.

---

## SDK pagrindai

---

### Apžvalga

SDK remiasi į išteklius orientuota kliento sandara. Kiekviena API sritis pateikiama kaip atskiras klientas aukščiausio lygio objekte `DignaClient`, su tipizuotais užklausų ir atsakymų modeliais bei nuosekliu klaidų apdorojimu.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Pagrindinės savybės

- **Tipizuoti modeliai** — kiekviena užklausa ir kiekvienas atsakymas tikrinami su pydantic, todėl redaktorius ir tipų tikrintuvas pastebi klaidas dar prieš kreipiantis į tinklą.
- **Orientacija į išteklius** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` ir `client.inspection_statuses` pateikia paprastus metodus `list` / `get` / `create` / `update` / `delete`.
- **Aiškios klaidos** — API klaidos kelia išimtį `DignaAPIError` (arba konkretesnę poklasę, pvz., `DignaAuthenticationError`, `DignaAuthorizationError` ar `DignaNotFoundError`), užuot tyliai grąžinusios `None`.

### Diegimas

```bash
pip install digna-sdk
```

---

## Žinyno puslapiai

Ši laida suskirstyta į šiuos puslapius:

- [Greitoji pradžia](quickstart.md) — prisijungimas ir pirmosios užklausos.
- [Ištekliai](resources.md) — visas galimų išteklių klientų sąrašas.
- [Modeliai](models.md) — įvesčiai ir išvesčiai naudojami pydantic modeliai.
- [Klaidos](errors.md) — išimčių hierarchija.
- [API žinynas](reference.md) — automatiškai sugeneruota žinyno dokumentacija.
