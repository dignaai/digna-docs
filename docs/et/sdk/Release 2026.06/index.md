---
title: digna Python SDK teatmik 2026.06 | digna dokumentatsioon
description: Täielik teatmik digna Python SDK versiooni 2026.06 kohta
image: /assets/logo_square.png
---

# digna Python SDK teatmik 2026.06

See jaotis dokumenteerib ***digna*** Python SDK-d. See on üles ehitatud mitmeleheküljelise teatmikuna: kasuta seda ülevaadet kliendi mõistmiseks ning jätka seejärel eraldi lehtedega kiirjuhendi, ressursside, mudelite, vigade ja genereeritud API dokumentatsiooni kohta.

SDK avaldatakse paketina `digna-sdk` ning see pakub stabiilset versioonitud klienti ***digna*** REST API jaoks.

---

## SDK alused

---

### Ülevaade

SDK järgib ressursipõhist kliendidisaini. Iga API valdkond on kättesaadav eraldi kliendina ülemises objektis `DignaClient`, kusjuures päringu- ja vastusemudelid on tüübitud ning veakäsitlus on ühtne.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Põhifunktsioonid

- **Tüübitud mudelid** — iga päring ja vastus valideeritakse pydanticuga, nii et redaktor ja tüübikontrollija märkavad vead enne võrgupäringu tegemist.
- **Ressursipõhisus** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` ja `client.inspection_statuses` pakuvad igaüks lihtsaid meetodeid `list` / `get` / `create` / `update` / `delete`.
- **Selged vead** — API vead tõstavad erindi `DignaAPIError` (või täpsema alamklassi, näiteks `DignaAuthenticationError`, `DignaAuthorizationError` või `DignaNotFoundError`) selle asemel, et vaikselt tagastada `None`.

### Paigaldamine

```bash
pip install digna-sdk
```

---

## Teatmiku lehed

See väljalase on jaotatud järgmiste lehtede vahel:

- [Kiirjuhend](quickstart.md) — ühenduse loomine ja esimesed päringud.
- [Ressursid](resources.md) — saadaolevate ressursiklientide täielik loend.
- [Mudelid](models.md) — sisendi ja väljundi jaoks kasutatavad pydanticu mudelid.
- [Vead](errors.md) — erindite hierarhia.
- [API teatmik](reference.md) — automaatselt genereeritud teatmikudokumentatsioon.
