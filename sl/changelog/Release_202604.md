# Changelog – Release 2026.04  

Z izdajo 2026.04 digna pomembno razširi svoje zmožnosti na področju analitike in validacije podatkov.  
Ta izdaja uvaja napredno analizo časovnih vrst, ponovno uporabne komponente za validacijo in centralizirano standardizacijo vrednosti.

---

## New Features  

### Analytics Chart – Time Series Analysis Without Data Science  
- Novi **Analytics Chart** za interaktivno analizo časovnih vrst  
- Vgrajene analitične metode:
    - Linearna, kvadratna in kubična regresija  
    - Segmentna regresija z nastavljivimi lomnimi točkami  
    - Tehnike glajenja  
    - Analiza kvantilov  
- Samodejna identifikacija trendov, sezonskosti in sprememb vzorcev  
- Analiza rezidualov za globlji vpogled v odstopanja  
- Časovne vrste se samodejno izračunajo za vsak nabor podatkov  

**Vpliv:** Omogoča uporabnikom razumevanje kompleksnega vedenja podatkov skozi čas brez potrebe po znanju podatkovne znanosti ali zunanjih orodjih.

---

### Enumerations – Central Definition of Allowed Values  
- Določite ponovno uporabne nize dovoljenih vrednosti (npr. države, zvezne enote, statusne kode)  
- Preverjajte vrednosti stolpcev glede na vnaprej določene enumeracije v **digna Data Validation**  
- Ponovno uporabite enumeracije v več projektih in virih podatkov  
- Uporabljajte enumeracije povsod preko `#ENUM:MY_ENUM#`  
- Vse kontrole se izvajajo **neposredno v izvorni podatkovni bazi**  

**Vpliv:** Zagotavlja dosledne in standardizirane vrednosti podatkov po celotni organizaciji.

---

### Validation Rule Templates – Reusable Data Quality Logic  
- Določite ponovno uporabna pravila validacije (npr. preverjanje presledkov, NOT NULL, preverjanja formata)  
- Uporabite predloge na več naborih podatkov  
- Zagotovite dosledno logiko pravil med projekti  
- Zmanjšajte podvajanje in ročno konfiguracijo  
- Vse kontrole se izvajajo **neposredno v izvorni podatkovni bazi**  

**Vpliv:** Omogoča skalabilno in zmogljivo validacijo podatkov brez premikanja podatkov.

---

### Pogoji relevantnosti na ravni statistike  
- Določite pogoje relevantnosti na **ravni stolpca za vsako statistiko**  
- Razširja koncept pogojev relevantnosti za anomalije  
- Nadzorujte, kdaj naj se statistika šteje za relevantno  
- Zmanjšajte šum z izključevanjem ne-kritičnih situacij  

**Vpliv:** Izboljša kakovost signalov s fokusiranjem samo na smiselna odstopanja.

---

## Extended Data Analytics & Validation Capabilities  

Z to izdajo digna širi tako **razumevanje podatkov** kot **standardizacijo validacije podatkov**:

- Napredna **interpretacija časovnih vrst** brez znanja podatkovne znanosti  
- Centralizirana definicija **dovoljenih vrednosti z uporabo enumeracij**  
- Ponovno uporabna **logika validacije prek predlog**  
- Fino nastavljen nadzor nad **relevantnostjo statistik in opozoril**  

Skupaj te zmožnosti omogočajo organizacijam, da ne le zaznavajo težave, ampak tudi **razumejo, standardizirajo in nadzorujejo kakovost podatkov**.

---

## Kdo ima koristi od te izdaje  

- **Inženirji podatkov:** Ponovno uporabna logika validacije in izboljšan nadzor nad vedenjem spremljanja  
- **Ekipe za kakovost podatkov in upravljanje:** Standardizirana pravila in dosledna validacija podatkov med sistemi  
- **Ekipe za analitiko in BI:** Boljše razumevanje trendov in odstopanj  
- **Lastniki platforme:** Večje sprejetje zaradi poenostavljene analitike in skalabilne validacije  

---

## CLI Updates  
- Brez sprememb  

---