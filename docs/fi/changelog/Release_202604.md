---
title: digna Julkaisu 2026.04 | Analytics Chart, Enumerations & Validation Rule Templates
description: Tutustu, mitä uutta digna Julkaisussa 2026.04. Tässä versiossa on edistynyttä aikasarja-analyysiä Analytics Chartin avulla, uudelleenkäytettäviä validointimallipohjia, enumerations-arvostandardisointi ja saraketason relevanssiehdot.
keywords: digna Julkaisu 2026.04, digna changelog, digna Data Analytics, aikasarja-analyysi, regressio, data validation -mallipohjat, enumerations, sallitut arvot validointi, datan laatu säännöt, data observability
image: /assets/logo_square.png
---

# Changelog – Julkaisu 2026.04  

Julkaisussa 2026.04 digna parantaa merkittävästi analytiikka- ja datan validointiominaisuuksia.  
Tämä julkaisu esittelee edistyneitä aikasarja-analyysejä, uudelleenkäytettäviä validointikomponentteja ja keskitettyä arvojen standardisointia.

---

## 🚀 Uudet ominaisuudet  

### Analytics Chart – Aikasarja-analyysi ilman data science -osaamista  
- Uusi **Analytics Chart** interaktiiviseen aikasarja-analyysiin  
- Sisäänrakennetut analyysimenetelmät:
    - Lineaarinen, kvadratiivinen ja kuubinen regressio  
    - Piecewise-regressio konfiguroitavilla murtopisteillä  
    - Smoothing-tekniikat  
    - Kvantiilianalyysi  
- Trendien, kausiluonteisuuden ja mallimuutosten automaattinen tunnistus  
- Jäännösanalyysi syvempään poikkeamien ymmärtämiseen  
- Aikasarjat lasketaan automaattisesti jokaiselle datasetille  

**Vaikutus:** Mahdollistaa käyttäjille monimutkaisen datakäyttäytymisen ymmärtämisen ajassa ilman data science -osaamista tai ulkoisia työkaluja.

---

### Enumerations – Sallitujen arvojen keskitetty määrittely  
- Määrittele uudelleenkäytettäviä sallitun arvon joukkoja (esim. maat, osavaltiot, tilakoodit)  
- Validoi sarakkeen arvot ennalta määriteltyjä enumerations-joukkoja vastaan **digna Data Validation** -moduulissa  
- Käytä enumerations-joukkoja uudelleen projekteissa ja eri tietolähteissä  
- Käytä enumerations-arvoja kaikkialla muodossa `#ENUM:MY_ENUM#`  
- Kaikki tarkistukset suoritetaan **suoraan lähdetietokannassa**  

**Vaikutus:** Varmistaa yhdenmukaiset ja standardoidut datan arvot organisaation laajuisesti.

---

### Validation Rule Templates – Uudelleenkäytettävät datan laatu -logiikat  
- Määrittele uudelleenkäytettäviä validointisääntöjä (esim. välilyöntitarkistukset, NOT NULL, formaattitarkistukset)  
- Käytä mallipohjia useissa datasetissä  
- Varmista yhtenäinen sääntökäytäntö projekteissa  
- Vähennä päällekkäisyyttä ja manuaalista konfigurointia  
- Kaikki tarkistukset suoritetaan **suoraan lähdetietokannassa**  

**Vaikutus:** Mahdollistaa skaalautuvan ja suorituskykyisen datan validoinnin ilman datan siirtoa.

---

### Tilastotason relevanssiehdot  
- Määrittele relevanssiehdot **saraketasoisesti kullekin tilastolle**  
- Laajentaa anomalioiden relevanssiehtojen käsitettä  
- Hallitse, milloin tilastoa tulisi pitää relevanttina  
- Vähennä kohinaa sulkemalla pois ei-kriittiset tilanteet  

**Vaikutus:** Parantaa signaalin laatua keskittymällä vain merkityksellisiin poikkeamiin.

---

## 🧪 Laajennetut Data Analytics- ja Validation-ominaisuudet  

Tässä julkaisussa digna laajentaa sekä **datan ymmärrystä** että **datan validoinnin standardisointia**:

- Edistynyt **aikasarja-tulkinta** ilman data science -osaamista  
- Keskitetty määrittely **sallituille arvoille enumerationsin kautta**  
- Uudelleenkäytettävä **validointilogiikka mallipohjien avulla**  
- Hienojakoinen kontrolli **tilastojen ja hälytysten relevanssille**  

Näiden ominaisuuksien avulla organisaatiot voivat paitsi havaita ongelmia, myös **ymmärtää, standardoida ja kontrolloida datan laatua**.

---

## 🎯 Kenelle julkaisu hyödyttää  

- **Data Engineers:** Uudelleenkäytettävät validointilogiikat ja parannettu hallinta seurannan käytöksestä  
- **Data Quality & Governance -tiimit:** Standardoidut säännöt ja yhtenäinen datan validointi järjestelmien välillä  
- **Analytics & BI -tiimit:** Parempi ymmärrys trendeistä ja poikkeamista  
- **Alustan omistajat:** Suurempi käyttöönotto yksinkertaistetun analytiikan ja skaalautuvan validoinnin kautta  

---

## 🛠 CLI-päivitykset  
- Ei muutoksia  

---