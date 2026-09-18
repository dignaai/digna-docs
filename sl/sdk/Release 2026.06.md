# Referenca SDK Python digna 2026.06

Ta razdelek dokumentira SDK Python za ***digna***. Urejen je kot večstranska referenca: ta pregled pomaga razumeti odjemalca, nato pa nadaljujte na posebnih straneh o hitrem začetku, virih, modelih, napakah in samodejno ustvarjeni dokumentaciji API.

SDK je objavljen kot paket `digna-sdk` in ponuja stabilnega, verzioniranega odjemalca za REST API ***digna***.

---

## Osnove SDK

---

### Pregled

SDK temelji na zasnovi odjemalca, usmerjeni v vire. Vsako področje API je na vrhnjem objektu `DignaClient` na voljo kot samostojen odjemalec, s tipiziranimi modeli zahtev in odzivov ter enotnim obravnavanjem napak.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Ključne zmogljivosti

- **Tipizirani modeli** — vsaka zahteva in vsak odziv sta preverjena s pydantic, zato urejevalnik in preverjevalnik tipov napake odkrijeta še pred omrežnim klicem.
- **Usmerjenost v vire** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` in `client.inspection_statuses` ponujajo preproste metode `list` / `get` / `create` / `update` / `delete`.
- **Jasne napake** — napake API sprožijo `DignaAPIError` (ali natančnejši podrazred, na primer `DignaAuthenticationError`, `DignaAuthorizationError` ali `DignaNotFoundError`), namesto da bi tiho vrnile `None`.

### Namestitev

```bash
pip install digna-sdk
```

---

## Referenčne strani

Ta izdaja je razdeljena na naslednje strani:

- [Hitri začetek](quickstart.md) — povezava in prvi klici.
- [Viri](resources.md) — celoten seznam razpoložljivih odjemalcev virov.
- [Modeli](models.md) — modeli pydantic, uporabljeni za vhod in izhod.
- [Napake](errors.md) — hierarhija izjem.
- [Referenca API](reference.md) — samodejno ustvarjena referenčna dokumentacija.