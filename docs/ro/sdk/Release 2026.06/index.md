---
title: Referință SDK Python digna 2026.06 | Documentație digna
description: Referință completă pentru versiunea 2026.06 a SDK-ului Python digna
image: /assets/logo_square.png
---

# Referință SDK Python digna 2026.06

Această secțiune documentează SDK-ul Python pentru ***digna***. Este organizată ca o referință pe mai multe pagini: folosiți această prezentare generală pentru a înțelege clientul, apoi continuați cu paginile dedicate pentru pornire rapidă, resurse, modele, erori și documentația API generată.

SDK-ul este publicat ca pachetul `digna-sdk` și pune la dispoziție un client stabil și versionat pentru API-ul REST ***digna***.

---

## Noțiuni de bază despre SDK

---

### Prezentare generală

SDK-ul urmează un design de client orientat pe resurse. Fiecare zonă a API-ului este expusă ca un client de sine stătător pe obiectul `DignaClient` de nivel superior, cu modele tipizate de cerere și răspuns și tratare consecventă a erorilor.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Funcționalități principale

- **Modele tipizate** — fiecare cerere și fiecare răspuns sunt validate cu pydantic, astfel încât editorul și verificatorul de tipuri să depisteze greșelile înainte de apelul în rețea.
- **Orientat pe resurse** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` și `client.inspection_statuses` expun fiecare metode simple `list` / `get` / `create` / `update` / `delete`.
- **Erori clare** — erorile API ridică `DignaAPIError` (sau o subclasă mai specifică, precum `DignaAuthenticationError`, `DignaAuthorizationError` sau `DignaNotFoundError`) în loc să returneze în tăcere `None`.

### Instalare

```bash
pip install digna-sdk
```

---

## Pagini de referință

Această versiune este împărțită în următoarele pagini:

- [Pornire rapidă](quickstart.md) — conectarea și primele apeluri.
- [Resurse](resources.md) — lista completă a clienților de resurse disponibili.
- [Modele](models.md) — modelele pydantic folosite pentru intrare și ieșire.
- [Erori](errors.md) — ierarhia excepțiilor.
- [Referință API](reference.md) — documentație de referință generată automat.
