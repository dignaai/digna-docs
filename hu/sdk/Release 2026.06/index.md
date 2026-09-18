# digna Python SDK referencia 2026.06

Ez a szakasz a ***digna*** Python SDK-ját mutatja be. Több oldalból álló referenciaként épül fel: ez az áttekintés a kliens megismerését szolgálja, majd a gyors bevezetőnek, az erőforrásoknak, a modelleknek, a hibáknak és a generált API-dokumentációnak külön oldalai vannak.

Az SDK a `digna-sdk` csomagként jelenik meg, és stabil, verziózott klienst nyújt a ***digna*** REST API-jához.

---

## Az SDK alapjai

---

### Áttekintés

Az SDK erőforrás-központú klienstervezést követ. Minden API-terület önálló kliensként jelenik meg a legfelső szintű `DignaClient` objektumon, tipizált kérés- és válaszmodellekkel, egységes hibakezeléssel.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Fő jellemzők

- **Tipizált modellek** — minden kérést és választ a pydantic ellenőriz, így a szerkesztő és a típusellenőrző még a hálózati hívás előtt kiszűri a hibákat.
- **Erőforrás-központú felépítés** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` és `client.inspection_statuses` egyaránt egyszerű `list` / `get` / `create` / `update` / `delete` metódusokat kínál.
- **Egyértelmű hibák** — az API-hibák `DignaAPIError` kivételt váltanak ki (vagy egy pontosabb alosztályt, például `DignaAuthenticationError`, `DignaAuthorizationError` vagy `DignaNotFoundError`) ahelyett, hogy csendben `None` értéket adnának vissza.

### Telepítés

```bash
pip install digna-sdk
```

---

## Referenciaoldalak

Ez a kiadás a következő oldalakra tagolódik:

- [Gyors bevezető](quickstart.md) — csatlakozás és az első hívások.
- [Erőforrások](resources.md) — az elérhető erőforrás-kliensek teljes listája.
- [Modellek](models.md) — a bemenethez és kimenethez használt pydantic modellek.
- [Hibák](errors.md) — a kivételek hierarchiája.
- [API-referencia](reference.md) — automatikusan generált referenciadokumentáció.