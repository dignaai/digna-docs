# Changelog – Izdaja 2026.06  

Z Izdajo 2026.06 digna naredi velik korak naprej na področju avtomatizacije, razširljivosti in uporabnosti platforme.  
Ta različica uvaja nov **digna Python SDK**, uradno **Docker podporo za namestitev**, prenovljeno izkušnjo nadzorne plošče in izboljšano prenosljivost pri upravljanju pravil validacije.

---

## Nove funkcije  

### digna Python SDK – avtomatizirajte vse s Pythonom  
- Namestitev:
  ```bash
  pip install digna-sdk
  ```
- Programsko upravljanje in avtomatizacija digna z uporabo Pythona  
- Ustvarjanje in konfiguracija projektov preko kode  
- Sprožanje inšpekcij ter izvajanja nadzorov  
- Programsko upravljanje datasetov, pravil in konfiguracij  
- Profiliranje tabel in pridobivanje vpogledov v metapodatke  
- Izvoz rezultatov profiliranja in kakovosti podatkov v zunanje repozitorije in sisteme  
- Integracija z notebooki, orkestracijskimi orodji in CI/CD cevovodi

**Vpliv:** Omogoča polno infrastrukturo kot kodo in globoko avtomatizacijo potekov dela za kakovost in opazovanje podatkov z uporabo Pythona.

---

### Docker podpora – poenostavljena namestitev in obratovanje  
- Uradna Docker slika za digna  
- Hitro in dosledno nastavitev v različnih okoljih  
- Poenostavljeno uvajanje za razvoj, testiranje in produkcijo  
- Enostavna integracija s Kubernetes in drugimi platformami za kontejnerje  
- Izboljšana prenosljivost in reproducibilnost namestitev

**Vpliv:** Olajša nameščanje in obratovanje digne v sodobnih cloud-native arhitekturah.

---

### QueryMode – prilagodljiva strategija izvajanja SQL poizvedb

Konfigurirajte strategijo izvajanja poizvedb: **Single** ali **Combined** način

**Single Mode**: Vsaka statistika se izračuna z eno namensko SQL poizvedbo

  - Idealno za velike podatkovne vire, kjer so omejitve pomnilnika ključne
  - Preprečuje izčrpanje virov pri združenih poizvedbah (out of memory, omejitve spoola)
  - Večje število poizvedb, a nižja poraba pomnilnika na poizvedbo

**Combined Mode**: Vse statistike se izračunajo znotraj ene SQL poizvedbe

  - Zmanjša skupno število poizvedb in omrežni overhead
  - Optimizira zmogljivost, kadar so podatkovni viri obvladljivi v pomnilniku
  - Bolj učinkovito pri pogostih, vzporednih izvedbah

**Vpliv:** Uporabnikom daje fino nastavitev nad izvajanjem poizvedb za uravnoteženje zmogljivosti, porabe virov in varnosti pomnilnika glede na značilnosti njihovega podatkovnega vira.


---

### Prenovljena izkušnja nadzorne plošče  
- Moderniziran in izboljšan UI/UX dizajn  
- Jasnejša navigacija in struktura  
- Boljša vidljivost rezultatov nadzora in vpogledov o kakovosti podatkov  
- Izboljšana berljivost opozoril, statistik in nadzornih plošč  
- Hitrejši dostop do ključnih operativnih informacij  

**Vpliv:** Izboljšuje uporabnost in dnevno produktivnost za vse uporabnike.

---

### Razširjen uvoz in izvoz pravil validacije  
- Izboljšana funkcionalnost uvoza/izvoza pravil validacije  
- Lažja migracija med okolji in projekti  
- Boljša ponovna uporaba standardiziranih nizov pravil  
- Izboljšano upravljanje urejanja pravil in življenjskega cikla  
- Poenostavljeno sodelovanje med ekipami  

**Vpliv:** Omogoča skalabilno in dosledno upravljanje kakovosti podatkov po organizaciji.

---

## Izboljšave platforme  

- Popolna integracija Python SDK za avtomatizacijo  
- Kontejnerizirana namestitev prek Dockerja  
- Izboljšana UX skozi prenovljeno nadzorno ploščo  
- Razširjena prenosljivost validacijske logike  

---

## Kdo ima koristi od te izdaje  

- Data Inženirji: avtomatizacija, uporaba SDK, integracija v cevovode  
- Platformne ekipe: poenostavljena namestitev prek Dockerja  
- Ekipe za upravljanje podatkov: ponovno uporabno upravljanje pravil validacije  
- Analitične ekipe: izboljšana uporabnost in vidnost vpogledov  

---

## Posodobitve CLI  
- Dodana podpora za integracijo SDK  
- Izboljšani poteki uvoza/izvoza  
- Splošne izboljšave stabilnosti in zmogljivosti