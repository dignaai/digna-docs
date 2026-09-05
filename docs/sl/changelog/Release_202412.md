---
title: digna izdaja 2024.12 | Dnevnik sprememb in nove funkcije
description: Odkrijte, kaj je novega v digna izdaji 2024.12. Ta različica uvaja vgrajen Scheduler, poročila v PDF, prilagodljive CUSTOM stolpce, dinamične nadomestne tokene v snapshot poizvedbah in pametnejšo optimizacijo pragov za izboljšanje zaznavanja anomalij in nadzora kakovosti podatkov.
keywords: digna izdaja 2024.12, digna dnevnik sprememb, opombe ob izdaji, vgrajeni Scheduler, PDF poročila, CUSTOM tip stolpca, nadomestni tokeni v snapshot poizvedbah, optimizacija pragov, opazovanje podatkov, nadzor kakovosti podatkov, zaznavanje anomalij
image: /assets/logo_square.png
---



# Dnevnik sprememb – Izdaja 2024.12

Izdaja 2024.12 prinaša nov nabor funkcij in izboljšav, ki naredijo digna bolj avtomatizirano, prilagodljivo in pripravljeno za poslovno rabo.  
Ta različica izboljšuje razporejanje, poročanje, obdelavo poizvedb in natančnost zaznavanja anomalij.  

---

## Nove funkcije

### Vgrajeni Scheduler
Inšpekcije se ne zanašajo več izključno na ukazno vrstico ali API klice.  
Z **novim digna Schedulerjem** se lahko inšpekcije izvajajo samodejno ob določenih časih.  

- Podpira **Cron expressions** za ponavljajoče se urnike (dnevno, tedensko ali po meri).  
- Omogoča natančen nadzor z **offseti**, **datumi začetka** in **datumi konca**.  
- Ekipa lahko zagotovi, da so vsi ključni viri podatkov dosledno pregledani brez ročnega dela.  

---

### Poročila v formatu PDF
Ekipe lahko zdaj enostavno delijo rezultate z deležniki prek **izvozov v PDF**.  

- Grafi, metrike in rezultati anomalij se lahko izvozijo v profesionalni PDF obliki.  
- Poročila združujejo **vizualizacije** in **osnovne podatke**, da zadovoljijo tako tehnične kot poslovne uporabnike.  
- Odpravlja potrebo po zunanjih orodjih za ustvarjanje poročil.  

---

### Nov tip stolpca: `CUSTOM`
Za večjo prilagodljivost digna uvaja nov **`CUSTOM` tip stolpca**.  

- Uporabniki lahko natančno določijo, katere **statistike in metrike** se uporabljajo za določene atribute.  
- Idealno za posebne primere, ki se ne prilegajo standardnim kategorijam, kot so NUMERICAL ali CATEGORICAL.  
- Pomaga ohranjati analize osredotočene in rezultate relevantne za poslovni kontekst.  

---

### Novi nadomestni tokeni v snapshot poizvedbah
Snapshot poizvedbe so zdaj preprostejše in manj dovzetne za napake z uporabo **dinamičnih nadomestnih tokenov**.  

- Tokeni, kot so `#date+n#` ali `#date-n#`, samodejno prilagodijo datume v poizvedbah.  
- Primer:  
  - `#date+1#` → jutri  
  - `#date-2#` → pred dvema dnevoma  
- Odpravlja ročne izračune datumov in zagotavlja doslednost med ekipami.  

---

### Optimizacija pragov
Pragi za anomalije so zdaj bolj inteligentni in ozaveščeni o kontekstu.  

- Za metrike, kot je **NULL COUNT**, so spodnji pragovi samodejno omejeni na **0**.  
- Preprečuje veljavne ali nepomembne prage.  
- Posledica so manj lažnih pozitivnih zaznav in bolj zanesljivo odkrivanje anomalij.  

---

## Splošne izboljšave
- Izboljšane **UI komponente** v pogledih za konfiguracijo projektov in atributov.  
- Izboljšana **zmogljivost nadzorne plošče** pri velikih količinah podatkov.  
- Izboljšano **beleženje in sporočila o napakah** za lažje odpravljanje težav.  

---

## Povzetek
Izdaja 2024.12 krepi digna kot platformo za **kakovost podatkov, zaznavanje anomalij in opazovanje podatkov**.  
Z avtomatizacijo prek razporejanja, deljivimi PDF poročili, prilagodljivimi stolpci, poenostavljenimi snapshot poizvedbami in pametnejšimi stroški pragov postaja digna še bolj dragocena tako za tehnične uporabnike kot poslovne deležnike.