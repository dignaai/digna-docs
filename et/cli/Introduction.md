## Käsurealiidese (CLI) eesmärk

***digna*** Command Line Interface (CLI) on võimas tööriist, mis on loodud sujuvdama suhtlust ***digna*** platvormiga. See pakub tekstipõhist liidest, mis võimaldab kasutajatel tõhusalt sooritada mitmesuguseid ülesandeid ilma graafilise kasutajaliideseta.

### Põhifunktsioonid:

- **Tõhusus ja paindlikkus:** CLI võimaldab käskude kiiret täitmist, suurendades tootlikkust.
- **Automatiseerimine:** Toetab skriptimist korduvate ülesannete automatiseerimiseks.
- **Kaugjuurdepääs:** Halda ***digna*** ressursse ükskõik kust.
- **Järjepidevus ja usaldusväärsus:** Tagab usaldusväärseid toiminguid dokumenteeritud ja versioonihalduse all olevate käskudega.
- **Skaleeritavus:** Suudab käsitleda laiaulatuslikke ettevõtteülesandeid.
- **Õppimine ja valdamine:** Pakub põhjalikumat arusaama ***digna*** funktsionaalsusest.
- **Integratsioon teiste tööriistadega:** Sujuv integreerimine automatiseerimisvahenditega nagu Control-M, UC4, AutomateNOW!

---

## Paigaldusjuhised Windowsile

Alustamiseks järgige alltoodud samme, et lahti pakkida vajalikud failid, juurutada *dignacli* kaust ja konfigureerida ühendus ***digna*** hoidlaga. Enne alustamist veenduge, et teil on olemas hoidla kasutajatunnused ja kõik nõutavad konfiguratsiooniandmed.

1. *****digna*** CLI lahtipakkimine:**
   - Hankige `.zip`-fail, mis sisaldab ***digna*** CLI-d.
   - Pakkige fail lahti soovitud kataloogi.

2. **`dignacli` kausta juurutamine:**
   - Kopeerige `dignacli` kaust eelistatud paigalduskohta (nt `C:\Program Files\***digna***`).

3. **`config.toml` konfigureerimine:**
   - Kontrollige, kas `dignacli` sees on `config.toml`.
   - Kui vaja, nimetage `config_template.toml` ümber `config.toml` ja seadistage see vastavalt antud dokumentatsioonile.