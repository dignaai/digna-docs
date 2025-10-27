## Käsurealiidese (CLI) eesmärk

***digna*** käsurealiides (CLI) on võimas tööriist, mis on loodud lihtsustama suhtlust ***digna*** platvormiga. See pakub tekstipõhist liidest, mis võimaldab kasutajatel tõhusalt täita erinevaid ülesandeid ilma graafilise kasutajaliidese vajaduseta.

### Põhifunktsioonid:

- **Tõhusus ja paindlikkus:** CLI võimaldab käskude kiiret täitmist, parandades tootlikkust.
- **Automatiseerimine:** Toetab skriptimist korduvate ülesannete automatiseerimiseks.
- **Kaugjuurdepääs:** Halda ***digna*** ressursse igast asukohast.
- **Ühtlus ja usaldusväärsus:** Tagab usaldusväärse toimimise dokumenteeritud, versioonihalduses olevate käskude abil.
- **Skaalautuvus:** Haldab laiaulatuslikke operatsioone ettevõtte ülesannete jaoks.
- **Õppimine ja valdamine:** Pakub sügavamat arusaamist ***digna*** funktsionaalsusest.
- **Integreerimine teiste tööriistadega:** Sujuv integratsioon automatiseerimistööriistadega nagu Control-M, UC4, AutomateNOW!

---

## Installi juhised Windowsi jaoks

Alustamiseks järgige alltoodud samme, et lahti pakkida vajalikud failid, paigaldada *dignacli* kaust ja konfigureerida oma ühendus ***digna*** repositooriumiga. Enne alustamist veenduge, et teil on repositooriumi kasutajatunnused ja kõik vajalikud konfiguratsioonandmed käepärast.

1. *****digna*** CLI lahti pakkimine:**
   - Hankige `.zip` fail, mis sisaldab ***digna*** CLI-d.
   - Pakkige fail välja soovitud kataloogi.

2. **`dignacli` kausta paigaldamine:**
   - Kopeerige `dignacli` kaust eelistatud paigalduskohta (nt `C:\Program Files\***digna***`).

3. **`config.toml` seadistamine:**
   - Kontrollige, kas `dignacli` kaustas on `config.toml`.
   - Nimeta vajadusel `config_template.toml` ümber `config.toml`-iks ja konfigureerige see vastavalt kaasasolevale dokumentatsioonile.