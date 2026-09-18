# digna Python SDK -referenssi 2026.06

Tämä osio dokumentoi ***digna***-palvelun Python SDK:n. Se on jäsennetty monisivuiseksi referenssiksi: tästä yleiskatsauksesta saa käsityksen asiakasohjelmasta, minkä jälkeen kannattaa jatkaa omille sivuille pikaoppaasta, resursseista, malleista, virheistä ja generoidusta API-dokumentaatiosta.

SDK julkaistaan pakettina `digna-sdk`, ja se tarjoaa vakaan, versioidun asiakasohjelman ***digna***-palvelun REST-rajapintaan.

---

## SDK:n perusteet

---

### Yleiskatsaus

SDK noudattaa resurssikeskeistä asiakasohjelman rakennetta. Jokainen rajapinta-alue on tarjolla omana asiakasohjelmanaan ylimmän tason `DignaClient`-oliossa, ja käytössä ovat tyypitetyt pyyntö- ja vastausmallit sekä yhtenäinen virheenkäsittely.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Keskeiset ominaisuudet

- **Tyypitetyt mallit** — jokainen pyyntö ja vastaus validoidaan pydanticilla, joten editori ja tyyppitarkistin huomaavat virheet ennen verkkokutsua.
- **Resurssikeskeisyys** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` ja `client.inspection_statuses` tarjoavat kukin yksinkertaiset `list` / `get` / `create` / `update` / `delete` -metodit.
- **Selkeät virheet** — rajapintavirheet nostavat poikkeuksen `DignaAPIError` (tai tarkemman aliluokan, kuten `DignaAuthenticationError`, `DignaAuthorizationError` tai `DignaNotFoundError`) sen sijaan, että palauttaisivat hiljaisesti arvon `None`.

### Asennus

```bash
pip install digna-sdk
```

---

## Referenssisivut

Tämä julkaisu on jaettu seuraaville sivuille:

- [Pikaopas](quickstart.md) — yhdistäminen ja ensimmäiset kutsut.
- [Resurssit](resources.md) — täydellinen luettelo käytettävissä olevista resurssiasiakkaista.
- [Mallit](models.md) — syötteissä ja vastauksissa käytettävät pydantic-mallit.
- [Virheet](errors.md) — poikkeusten hierarkia.
- [API-referenssi](reference.md) — automaattisesti generoitu referenssidokumentaatio.