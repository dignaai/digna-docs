---
title: digna Release 2024.12 | Zapis sprememb in nove funkcije
description: Izvedite, kaj je novega v digna Release 2024.12. V tej izdaji je dodan vgrajen razporejevalnik, PDF-poročila, prilagodljivi CUSTOM stolpci, dinamični placeholderji v snapshot-poizvedbah in pametnejša optimizacija pragov za izboljšano odkrivanje anomalij in spremljanje kakovosti podatkov.
keywords: digna Release 2024.12, digna zapis sprememb, opombe ob izdaji, vgrajen razporejevalnik, PDF-poročila, tip CUSTOM stolpca, placeholderji v snapshot-poizvedbah, optimizacija pragov, opazljivost podatkov, spremljanje kakovosti podatkov, odkrivanje anomalij
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Zapis sprememb – Release 2024.12

Izdaja 2024.12 prinaša vrsto novih funkcij in izboljšav, zaradi katerih je digna bolj avtomatizirana, prilagodljiva in pripravljena za uporabo v podjetjih.  
Ta različica izboljšuje razporejanje, poročanje, obdelavo poizvedb in natančnost odkrivanja anomalij.  

---

## Nove funkcije

### Vgrajen razporejevalnik
Preverjanja niso več odvisna izključno od ukazne vrstice ali klicev API.  
Z novim razporejevalnikom digna se lahko preverjanja izvajajo samodejno ob določenem času.  

- Podpira **Cron-izraze** za ponavljajoče se urnike (dnevno, tedensko ali z lastnim intervalom).  
- Omogoča natančen nadzor preko **offsetov (offsets)**, **datumov začetka** in **datumov konca**.  
- Omogoča ekipam zagotoviti dosledno in brezskrbno preverjanje vseh ključnih virov podatkov.  

---

### Poročila v formatu PDF
Ekipe zdaj lahko preprosto delijo rezultate s ključnimi deležniki preko **izvoza v PDF**.  

- Grafi, metrike in rezultati anomalij se lahko izvozijo v profesionalno PDF-datoteko.  
- Poročila združujejo **vizualizacije** in **ključne podatke**, zadovoljijo pa tako tehnične kot poslovne uporabnike.  
- Odpravlja potrebo po zunanjih orodjih za ustvarjanje poročil.  

---

### Nov tip stolpca: `CUSTOM`
Da bi zagotovili več prilagodljivosti, digna uvaja nov tip stolpca **`CUSTOM`**.  

- Uporabniki lahko natančno določijo, katere **statistike in metrike** se uporabljajo za določene atribute.  
- Idealno za posebne primere, ki se ne ujemajo s standardnimi kategorijami, kot so NUMERICAL ali CATEGORICAL.  
- Pomaga ohraniti analizo osredotočeno in naredi rezultate relevantne za poslovni kontekst.  

---

### Novi placeholderji v snapshot-poizvedbah
Snapshot-poizvedbe so postale preprostejše in manj nagnjene k napakam zahvaljujoč **dinamičnim placeholderjem**.  

- Tokeni, kot so `#date+n#` ali `#date-n#`, samodejno prilagodijo datume v poizvedbah.  
- Primer:  
  - `#date+1#` → jutri  
  - `#date-2#` → pred dvema dnevoma  
- Odpravlja ročne izračune datumov in zagotavlja doslednost v ekipah.  

---

### Optimizacija pragov
Pragi za anomalije so postali pametnejši in kontekstno občutljivi.  

- Za metrike, kot je **NULL COUNT**, so spodnji pragi samodejno omejeni na vrednost **0**.  
- Preprečuje nepravilne ali nesmiselne prage.  
- Zmanjšuje število lažnih sprožitev in povečuje zanesljivost odkrivanja anomalij.  

---

## Splošne izboljšave
- Izboljšani **UI komponenti** v prikazih konfiguracije projektov in atributov.  
- Izboljšana zmogljivost **dashboarda** pri velikih količinah podatkov.  
- Razširjeno beleženje in sporočanje o napakah za lažjo razlago in odpravljanje težav.  

---

## Povzetek
Izdaja 2024.12 krepi položaj digne kot platforme za **kakovost podatkov, odkrivanje anomalij in opazljivost podatkov**.  
Z avtomatizacijo prek razporejanja, skupnimi PDF-poročili, prilagodljivimi stolpci, poenostavljenimi snapshot-poizvedbami in pametnejšimi pragi postaja digna še bolj dragoceno orodje tako za tehnične uporabnike kot poslovne deležnike.