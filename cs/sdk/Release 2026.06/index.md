# Referenční příručka digna Python SDK 2026.06

Tato sekce dokumentuje Python SDK pro ***digna***. Je uspořádána jako vícestránková referenční příručka: tento přehled slouží k pochopení klienta, poté pokračujte na samostatných stránkách o rychlém startu, zdrojích, modelech, chybách a vygenerované dokumentaci API.

SDK se publikuje jako balíček `digna-sdk` a poskytuje stabilního, verzovaného klienta pro REST API ***digna***.

---

## Základy SDK

---

### Přehled

SDK vychází z návrhu klienta orientovaného na zdroje. Každá oblast API je dostupná jako samostatný klient na nadřazeném objektu `DignaClient`, s typovanými modely požadavků a odpovědí a jednotným zpracováním chyb.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Hlavní vlastnosti

- **Typované modely** — každý požadavek i každá odpověď se validují pomocí pydantic, takže editor a kontrola typů odhalí chyby dříve, než dojde k síťovému volání.
- **Orientace na zdroje** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` a `client.inspection_statuses` nabízejí jednoduché metody `list` / `get` / `create` / `update` / `delete`.
- **Srozumitelné chyby** — chyby API vyvolají výjimku `DignaAPIError` (nebo konkrétnější podtřídu, například `DignaAuthenticationError`, `DignaAuthorizationError` či `DignaNotFoundError`) místo toho, aby tiše vrátily `None`.

### Instalace

```bash
pip install digna-sdk
```

---

## Referenční stránky

Toto vydání je rozděleno do následujících stránek:

- [Rychlý start](quickstart.md) — připojení a první volání.
- [Zdroje](resources.md) — úplný seznam dostupných klientů zdrojů.
- [Modely](models.md) — modely pydantic používané pro vstup a výstup.
- [Chyby](errors.md) — hierarchie výjimek.
- [Referenční příručka API](reference.md) — automaticky generovaná referenční dokumentace.