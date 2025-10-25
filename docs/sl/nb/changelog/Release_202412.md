---
title: digna Release 2024.12 | Dnevnik sprememb in nove funkcije
description: Odkrijte, kaj je novega v digna Release 2024.12. Ta različica uvaja vgrajeni scheduler, PDF-poročanje, prilagodljive lastne stolpce, dinamične nadomestne znake v snapshot-povpraševanjih in pametnejšo optimizacijo pragov za izboljšanje odkrivanja anomalij in nadzora kakovosti podatkov.
keywords: digna Release 2024.12, digna dnevnik sprememb, opombe k izdaji, vgrajeni scheduler, PDF-poročila, lastni tip stolpca, snapshot-poizvedbeni nadomestni znaki, optimizacija pragov, data observability, nadzor kakovosti podatkov, odkrivanje anomalij
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Dnevnik sprememb – Release 2024.12

Release 2024.12 vsebuje novo serijo funkcij in izboljšav, ki naredijo digna bolj avtomatizirano, prilagodljivo in pripravljeno za poslovanje.  
Ta različica izboljšuje načrtovanje, poročanje, upravljanje poizvedb in natančnost pri odkrivanju anomalij.  

---

## Nove funkcije

### Vgrajeni Scheduler
Inšpekcije niso več odvisne samo od ukazne vrstice ali API-klicev.  
Z **novim digna Schedulerjem** se inšpekcije samodejno izvajajo ob določenih časih.  

- Podpira **Cron-izraze** za ponavljajoče se razporejanje (dnevno, tedensko ali po meri).  
- Omogoča natančen nadzor preko **offsets**, **datumov začetka** in **datumov konca**.  
- Omogoča ekipam, da zagotovijo, da so vse kritične podatkovne vire dosledno pregledane brez ročnega dela.  

---

### Poročila v PDF-formatu
Ekipe lahko zdaj enostavno delijo rezultate z deležniki preko **PDF-izvozov**.  

- Grafi, meritve in rezultati anomalij so lahko izvoženi v profesionalni PDF-obliki.  
- Poročila združujejo **vizualizacije** in **osnovne podatke** za tehnične in poslovne uporabnike.  
- Odpravlja potrebo po zunanjih orodjih za generiranje poročil.  

---

### Nov tip stolpca: `CUSTOM`
Za večjo prilagodljivost digna uvaja nov tip stolpca: **`CUSTOM`**.  

- Uporabniki lahko natančno določijo, katere **statistike in metrike** se uporabljajo za določene atribute.  
- Idealno za posebne primere, ki ne ustrezajo standardnim kategorijam, kot sta NUMERICAL ali CATEGORICAL.  
- Pomaga ohranjati analize osredotočene in rezultate relevantne za poslovni kontekst.  

---

### Novi nadomestni znaki v snapshot-poizvedbah
Snapshot-poizvedbe so zdaj preprostejše in manj nagnjene k napakam z uporabo **dinamičnih nadomestnih znakov**.  

- Tokeni, kot sta `#date+n#` ali `#date-n#`, samodejno prilagodijo datume v poizvedbah.  
- Primer:  
  - `#date+1#` → jutri  
  - `#date-2#` → pred dvema dnevoma  
- Odpravlja ročne izračune datumov in zagotavlja doslednost med ekipami.  

---

### Optimizacija pragov
Pragi za anomalije so zdaj bolj inteligentni in kontekstno zavedni.  

- Za metrike, kot je **NULL COUNT**, so spodnji pragovi samodejno omejeni na **0**.  
- Preprečuje neveljavne ali nesmiselne prage.  
- Zagotavlja manj lažnih pozitivnih zaznav in bolj zanesljivo odkrivanje anomalij.  

---

## Splošne izboljšave
- Izboljšane **UI-komponente** v pogledih za konfiguracijo projektov in atributov.  
- Izboljšana **zmogljivost nadzorne plošče** za velike količine podatkov.  
- Boljša **beleženje in sporočila o napakah** za odpravljanje težav.  

---

## Povzetek
Release 2024.12 krepi digna kot platformo za **kakovost podatkov, odkrivanje anomalij in data observability**.  
Z avtomatizacijo prek razporejanja, deljivimi PDF-poročili, prilagodljivimi stolpci, poenostavljenimi snapshot-poizvedbami in pametnejšimi pragi postaja digna še bolj dragocena za tehnične uporabnike in poslovne deležnike.