---
title: digna Julkaisu 2025.09 | Modulaarinen arkkitehtuuri, viisi uutta moduulia, MFA OIDC:n kautta
description: Tutustu, mitä uutta digna Julkaisu 2025.09 tuo. Tämä versio esittelee modulaarisen arkkitehtuurin, viisi uutta moduulia, MFA OIDC:n kautta ja moduulikohtaiset ilmoitukset.
keywords: digna Julkaisu 2025.09, digna muutosloki, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modulaarinen suunnittelu, digna OIDC MFA
image: /assets/logo_square.png
---

# Muutosloki – Julkaisu 2025.09  

Julkaisussa 2025.09 digna esittelee uuden **modulaarisen arkkitehtuurin** ja lanseeraa **viisi erikoistunutta moduulia** datan laadun ja observoitavuuden tarpeisiin.  
Tämä julkaisu myös vahvistaa todennusta ja parantaa ilmoitusten käsittelyä koko alustalla.  

---

## Uudet ominaisuudet  

### Modulaarinen arkkitehtuuri  
- digna noudattaa nyt **modulaarista arkkitehtuuria**.  
- Asiakkaat voivat ottaa käyttöön vain tarvitsemansa moduulit ja lisätä niitä tarpeen kasvaessa.  
- Aiempi toiminnallisuus on nyt osa **digna Data Anomalies**.  

### Uudet moduulit  
- **digna Data Anomalies** – Tekoälypohjainen poikkeavuuksien tunnistus datamäärissä, jakaumissa ja puuttuvissa arvoissa.  
- **digna Data Analytics** – Aikasarja-analyysi observoitavuusmittareille pitkän aikavälin trendien ja vaihtelun havaitsemiseksi.  
- **digna Data Timeliness** – Odotettujen datan saapumisaikojen seuranta, sekä tekoäly- että sääntöpohjaisin menetelmin.  
- **digna Data Validation** – Sääntöpohjaiset rivikohtaiset tarkistukset liiketoimintasääntöjen noudattamisen varmistamiseksi.  
- **digna Data Schema Tracker** – Skeeman muutosten (DDL-muutokset) havaitseminen valvotuissa tietokannoissa.  

### MFA OIDC:n kautta  
- Tuki **monivaiheiselle todennukselle (MFA)** OIDC Single Sign-On -integraation kautta.  
- Tarjoaa yritystason turvallisuuden kaikille käyttäjäkirjautumisille.  

### Moduulikohtaiset sähköposti-ilmoitukset  
- Ilmoitukset lähetetään nyt **moduulikohtaisesti**, mikä helpottaa Data Anomalies-, Data Analytics- ja muiden moduulien hälytysten eriyttämistä.  

---

## CLI-päivitykset  

- **Uusi komento: `inspect-cancel`** – Peruuta tarkastuksia pyynnön ID:llä tai lopeta kaikki aktiiviset pyynnöt.  
- **Uusi komento: `check-config`** – Tarkista määritystiedostot ennen käynnistystä.  
- **Uusi komento: `remove-orphans`** – Siivoa orpoja repositorion merkintöjä.  
- **Parannettu `inspect`-komento** – Uusi optio `--bypass-backend` (`-bb`) ja standardoidut paluuarvot (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Dokumentaatio  
- Uudet oppaat:  
  - Single Sign-On -integraatio-opas