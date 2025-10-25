---
title: digna različica 2024.12 | Spremembe in nove funkcije
description: Odkrijte, kaj je novega v digna različici 2024.12. Ta različica uvaja vgrajen razporejevalnik, poročanje v PDF, prilagodljive prilagojene stolpce, dinamične označevalce poizvedb snapshot in izboljšano optimizacijo pragov za boljšo zaznavo anomalij.
keywords: digna različica 2024.12, digna dnevnik sprememb, zapis sprememb, vgrajen scheduler, PDF poročila, custom column type, snapshot query placeholders, threshold optimization, opazljivost podatkov, spremljanje kakovosti podatkov, zaznavanje anomalij
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---

# Spremembe – Različica 2024.12

Različica 2024.12 prinaša nove funkcije in izboljšave, zaradi katerih je digna bolj avtomatizirana, prilagodljiva in pripravljena za poslovno rabo.  
Ta izdaja izboljšuje razporejanje, poročanje, obdelavo poizvedb in natančnost zaznavanja anomalij.  

---

## Nove funkcije

### Vgrajeni razporejevalnik
Pregledi niso več odvisni samo od ukazne vrstice ali API klicev.  
Z novim **digna Scheduler** lahko pregledi tečejo samodejno ob določenih časih.  

- Podpira **Cron izraze** za ponavljajoče se urnike (dnevno, tedensko ali po meri).  
- Omogoča natančen nadzor z **offseti**, **začelnimi datumi** in **končnimi datumi**.  
- Pomaga ekipam zagotoviti, da se vsi kritični podatkovni viri dosledno pregledajo brez ročnega dela.  

---

### Poročila v formatu PDF
Ekipe lahko rezultate zdaj preprosto delijo s deležniki z uporabo **izvozov v PDF**.  

- Grafikoni, meritve in rezultati zaznavanja anomalij so izvozljivi v profesionalni PDF obliki.  
- Poročila združujejo **vizualizacije** in **infrastrukturne podatke**, primerno tako za tehnične kot poslovne uporabnike.  
- Odpravlja potrebo po zunanjih orodjih za ustvarjanje poročil.  

---

### Nov tip stolpca: `CUSTOM`
Za večjo prilagodljivost digna uvaja nov tip stolpca **`CUSTOM`**.  

- Uporabniki lahko natančno določijo, katere **statistike in metrike** se uporabljajo za določene atribute.  
- Idealno za posebne primere, ki ne sodijo v standardne kategorije, kot so NUMERICAL ali CATEGORICAL.  
- Pomaga, da analize ostanejo osredotočene in da rezultati ustrezajo poslovnemu kontekstu.  

---

### Novi označevalci v snapshot poizvedbah
Snapshot poizvedbe so zdaj enostavnejše in manj dovzetne za napake z uporabo **dinamičnih označevalcev**.  

- Tokeni, kot so `#date+n#` ali `#date-n#`, samodejno prilagodijo datume v poizvedbah.  
- Primer:  
  - `#date+1#` → jutri  
  - `#date-2#` → pred dvema dnevoma  
- Odpravlja ročne izračune datumov in zagotavlja doslednost med ekipami.  

---

### Optimizacija pragov
Pragi za anomalije so zdaj pametnejši in občutljivi na kontekst.  

- Za metrike, kot je **NULL COUNT**, so spodnji pragovi samodejno omejeni na **0**.  
- Preprečuje nastanek neveljavnih ali nesmiselnih pragov.  
- Zmanjšuje število lažno pozitivnih zaznav in povečuje zanesljivost odkrivanja anomalij.  

---

## Splošne izboljšave
- Izboljšane **UI komponente** v pogledih za konfiguracijo projektov in atributov.  
- Izboljšana **zmogljivost nadzorne plošče** pri velikih količinah podatkov.  
- Izboljšano **beleženje in sporočila o napakah** za lažje odpravljanje težav.  

---

## Povzetek
Različica 2024.12 naredi digno močnejšo platformo za **kakovost podatkov, zaznavanje anomalij in opazljivost**.  
Z avtomatizacijo razporejanja, deljivimi PDF poročili, prilagodljivimi stolpci, poenostavljenimi snapshot poizvedbami in pametnejšimi pragi je digna še bolj vredna tako za tehnične uporabnike kot poslovne deležnike.