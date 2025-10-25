## Namen ukazne vrstice (CLI)

The ***digna*** Command Line Interface (CLI) je zmogljivo orodje, zasnovano za poenostavitev interakcij s platformo ***digna***. Ponuja besedilni vmesnik, ki uporabnikom omogoča učinkovito izvajanje širokega nabora opravil, brez potrebe po grafičnem uporabniškem vmesniku.

### Ključne lastnosti:

- **Učinkovitost in prilagodljivost:** CLI omogoča hitro izvrševanje ukazov ter povečuje produktivnost.
- **Avtomatizacija:** Podpira skriptiranje za avtomatizacijo ponavljajočih se opravil.
- **Oddaljen dostop:** Upravljajte vire ***digna*** od kjer koli.
- **Doslednost in zanesljivost:** Zagotavlja zanesljive operacije z dokumentiranimi ukazi, ki so pod nadzorom različic.
- **Razširljivost:** Obvladuje obsežne operacije za podjetja.
- **Učenje in obvladovanje:** Omogoča globlje razumevanje funkcionalnosti ***digna***.
- **Integracija z drugimi orodji:** Brezhibno se integrira z orodji za avtomatizacijo, kot so Control-M, UC4, AutomateNOW!

---

## Navodila za namestitev v sistemu Windows

Za začetek sledite spodnjim korakom za razpakiranje potrebnih datotek, namestitev
*dignacli* mape in konfiguracijo svoje povezave do repozitorija ***digna***. Pred začetkom poskrbite, da imate pripravljene poverilnice za repozitorij in morebitne zahtevane podatke za konfiguracijo.

1. **Extracting the ***digna*** CLI:**
   - Pridobite `.zip` datoteko, ki vsebuje CLI ***digna***.
   - Razpakirajte datoteko v želeno mapo.

2. **Deploying the `dignacli` Folder:**
   - Kopirajte mapo `dignacli` v želeno lokacijo namestitve (npr. `C:\Program Files\***digna***`).

3. **Configuring `config.toml`:**
   - Preverite, ali v mapi `dignacli` obstaja `config.toml`.
   - Če ni, preimenujte `config_template.toml` v `config.toml` in ga konfigurirajte po priloženi dokumentaciji.