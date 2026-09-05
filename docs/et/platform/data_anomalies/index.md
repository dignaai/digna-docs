---
title: digna Data Anomalies | AI-põhine andmete jälgitavus
description: digna Data Anomalies on osa digna Data Observability Platformist. See õpib automaatselt teie andmete mustreid ja tuvastab anomaaliaid, et parandada andmete kvaliteeti ning jälgitavust andmebaasides, andmejärvedes ja andmelaos.
tags:
  - andmete kvaliteet
  - andmete jälgitavus
  - andmete kvaliteet
  - andmete jälgitavus
  - AI-põhine jälgimine
  - anomaaliate tuvastamine
  - digna
  - digna platvorm
hide:
  - toc                # optional: hide the small top-level TOC if you use inline nav
  - navigation         # optional: hide side navigation for standalone pages
image: /assets/logo_square.png
---


# digna Data Anomalies – AI-põhine andmekvaliteedi probleemide avastamine

**AI-toega jälgitavus pideva andmete usaldusväärsuse jaoks**

digna Data Anomalies on osa **digna Data Observability Platform**ist — moodulipõhine lahendus, mis parandab **andmete kvaliteeti**, analüüsides pidevalt, kuidas andmekogumid aja jooksul käituvad.

See õpib automaatselt, milline on teie andmete „tavaline” käitumine, ja teavitab teid käitumise muutustest — ilma staatiliste lävendite määramise või ühe reegli kirjutamiseta.  
Moodul töötab otse teie andmebaasis, nii et andmed ei lahku kunagi teie keskkonnast.

---

## digna Data Anomalies eesmärk

**digna Data Anomalies** moodul tagab pideva **andmete jälgitavuse**, arvutades ja jälgides eelmääratletud statistilisi mõõdikuid, nagu:

- Andmemaht ja kirjete arv  
- Puuduvate väärtuste osakaal  
- Väärtuste jaotused ja histogrammid  
- Numbrilised vahemikud ja keskmised  
- Veergude unikaalsus ja teksti pikkus  

Need mõõdikud kogutakse automaatselt iga andmekogu kohta.  
Nende abil ehitab digna mudeleid, mis esindavad iga mõõdiku tüüpilist käitumist — õppides päevaseid, nädalalisi või hooajalisi mustreid.  
Kui mudel on treenitud, ennustab moodul oodatavaid väärtusi uute andmete jaoks ja tuvastab kõrvalekalded, mis võivad viidata kvaliteediprobleemidele, protsessiriketest või ülesvoolu muutustest.

---

## Põhifunktsioonid

- Õpib oodatavat andmekäitumist automaatselt AI abil — ei vaja lävendite seadistamist.  
- Tuvastab järsud langused, hüpped või nihked andmemahtudes ja jaotustes.  
- Tuletab välja vahetatud veerud või valed atribuudi-kaardistused.  
- Tõstab esile ootamatud kategoriseeritud väärtused (nt uued piirkonnad või koodid).  
- Toetab kõiki veerutüüpe: numbrilised, kategoriseeritud või määramata.  
- Tegutseb täielikult kliendi keskkonnas — andmete liigutamist ei toimu.  
- Integreerub **digna Data Analytics**iga pikaajaliste trendide analüüsiks.

---

## Kuidas see töötab

### 1. samm – mõõdikute arvutamine
digna arvutab iga tabeli ja veeru kohta hulga profiilimõõdikuid.  
Need mõõdikud kirjeldavad teie andmete struktuuri ja statistilist käitumist ning salvestatakse edasiseks analüüsiks.

### 2. samm – mudeli treenimine
Ajalooliste mõõdikuväärtuste põhjal treenib digna kompaktseid masinõppemudeleid (signatuuri mudeleid), mis jäädvustavad iga mõõdiku normaalvahemikku.

### 3. samm – automaatne lävendi määramine
Kasutades *conformal inference* meetodit, arvutab digna adaptiivsed usaldusintervallid (auto-lävedid), mis kohanevad koos teie andmetega.  
Kui uued mõõdikuväärtused jäävad ennustatud vahemikust välja, märgistatakse need anomaaliatena.

See pidev tagasiside-silmus tagab, et monitooring jääb asjakohaseks isegi siis, kui andmemaht või mustrid loomulikult suurenevad.

---

## Näidistsenaariumid

### Ootamatu langus kirjete mahus
Andmekogu sisaldab tavaliselt umbes 500 000 kirjet päevas.  
Kui uus sissekanne sisaldab vaid 50 000 kirjet, märgib digna anomaalia ja näitab, kui palju väärtus oma õpitud vahemikust kõrvalekaldub.

### Tuvastatud vahetatud veerud
Veeru `last_name` keskmine stringi pikkus sobib järsku `first_name` keskmisega.  
digna tuvastab mõõdikumustrite kõrvalekalde ja annab märku võimalikust veerutevahetusest.

### Ootamatu kategooria tuvastamine
Austria linnu loetlev veerg sisaldab järsku väärtust „Zurich”.  
Põhinedes ajaloolistele jaotustele märgib digna uue väärtuse ootamatuna ja hoiatab kasutajat.

---

## Integratsioon teiste moodulitega

- **digna Data Analytics** — koondab anomaaliaajaloo ja volatiilsuse mõõdikud, et paljastada pikaajalisi trende.  
- **digna Data Validation** — rakendab selgeid ärireegleid deterministlikeks kvaliteedikontrollideks.  
- **digna Data Timeliness** — jälgib andmete saabumisaegu ja korreleerib hilinemisi anomaaliajuhtumitega.  
- **digna Data Schema Tracker** — tuvastab struktuurimuutusi, mis võivad seletada uusi anomaaliaid.

---

## Tüüpilised kasutusjuhtumid

- Puuduva või topeltlaadimise tuvastamine.  
- Vahetatud või lühendatud veergude identifitseerimine.  
- Jaotuse nihke tuvastamine numbrilistes või kategoorilistes tunnustes.  
- Ootamatute viiteväärtuste või koodide leidmine.  
- Pidevate ingestioonitorude monitoorimine ebaühtluste suhtes.  
- Üldise **andmete kvaliteedi** ja andmete **jälgitavuse** jälgimine erinevates domeenides.

---

## Kasud

- Ebanormaalse andmekäitumise viivitamatu tuvastamine.  
- Manuaalse lävendi häälestamise vajaduse likvideerimine.  
- Operatiivse koormuse vähendamine suurtes andmekeskkondades.  
- Analüütika ja aruandluse süsteemide usaldusväärsuse tõstmine.  
- Tugevdab **andmete kvaliteeti** ja lõpp-to-end **andmete jälgitavust**.

---

## Seotud digna moodulid

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — trendi- ja volatiilsusmõõdikud.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — reeglitel põhinev andmete verifitseerimine.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — andmete kohaletoimetamise ajakava jälgimine.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — skeemi muutuste tuvastamine.

---

## Kokkuvõte

**digna Data Anomalies** moodul on digna AI-toega **Data Observability Platform**i tuum.  
Pidevalt jälgides võtmemõõdikuid, õppides mustreid ja tuvastades kõrvalekaldeid aitab see organisatsioonidel tagada, et **andmete kvaliteet** jääb usaldusväärseks, stabiilseks ja seletatavaks — ilma manuaalse seadistamiseta.