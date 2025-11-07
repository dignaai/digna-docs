---
title: Data Schema Tracker – Seuraa skeeman kehitystä | digna Documentation
description: Tutustu siihen, miten digna Data Schema Tracker seuraa sarakkeiden muutoksia, tietotyyppipäivityksiä ja skeeman liukumista. Tunnista ja hälytä sekä tarkoituksellisista että tahattomista skeemamuutoksista estääksesi ETL-virheet, rikkinäiset raportit ja observabiliteetin heikentymisen.
canonical_url: https://docs.digna.ai/platform/data_schema_tracker/
image: /assets/logo_square.png
keywords:
  - skeeman seuranta
  - skeeman liukuman havaitseminen
  - skeeman kehityksen seuranta
  - metadatan observabiliteetti
  - datan observabiliteetti
  - datan laatu
  - datarakenteen seuranta
  - tietokannan metatiedot
  - etl-putken vakaus
  - digna data schema tracker
lang: fi
robots: index, follow
og_title: Data Schema Tracker – Seuraa skeeman kehitystä | digna Documentation
og_description: digna Data Schema Tracker seuraa skeeman liukumista, tietotyyppimuutoksia ja sarakemuutoksia. Saat hälytykset ennen kuin ETL-putket tai raportit epäonnistuvat odottamattomien rakennemuutosten vuoksi.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Seuraa skeeman kehitystä
<h1 style="display:none;">AI-pohjainen moduuli metadatan observabiliteettiin ja datan laatuun – digna Data Schema Tracker</h1>

---

## Tarkoitus

The **Data Schema Tracker** pitää sinut ajan tasalla tietokantarakenteiden kehityksestä.  
Se valvoo jatkuvasti **taulujen skeemoja, sarakkeita ja tietotyyppejä** havaitakseen **skeeman liukumista** — tarkoituksellisia tai tahattomia rakenneuudistuksia, jotka voivat häiritä putkia, ETL-tehtäviä tai BI-raportteja.

Varmistamalla läpinäkyvyyden skeeman muutoksissa digna auttaa organisaatioita ylläpitämään **luottamusta datan laatuun**, turvaamaan **datajärjestelmien observabiliteetin** ja välttämään kalliita tuotantohäiriöitä, joita havaitsemattomat skeemamuutokset voivat aiheuttaa.

---

## Tekninen yleiskatsaus

### Mitä se valvoo

- **Lisätyt tai poistetut sarakkeet** – Havaitsee äskettäin lisätyt, uudelleennimetyt tai poistetut sarakkeet.  
- **Tietotyyppimuutokset** – Tunnistaa muutoksia, kuten `INT → VARCHAR` tai `DATE → TIMESTAMP`.  
- **Taulujen ja näkymien muutokset** – Seuraa taulujen ja näkymien luomista, uudelleennimeämistä tai poistamista.  
- **Ympäristöjen väliset erot** – Vertaa skeemaversioita kehitys-, testi- ja tuotantoympäristöjen välillä.  

### Havaitseminen ja hälytys

- Skannaa **tietokannan metatietoja** tai **järjestelmäkatalogeja** suoraan dataplatformissasi.  
- Vertailee kutakin skeeman tilannekuvaa aiemmin tallennettuun versioon dignan observability-skeemassa.  
- Luo **reaaliaikaisia hälytyksiä** dashboardilla, API:n kautta tai ulkoisiin ilmoituskanaviin (sähköposti, Slack, webhook).  
- Kirjaa jokaisen skeemaversion **historiallista seurantaa ja auditointivalmiutta** varten.

---

## Arkkitehtuuri ja toteutus

- **Tietokannan sisäinen suoritus:** digna suoritetaan kokonaisuudessaan ympäristössäsi, kyselyt kohdistuvat metatietonäkymiin ilman käyttäjädatan poistamista.  
- **Kevyt skannaus:** pääsy vain rakenteelliseen informaatioon — ei koskaan käyttäjädataa.  
- **Keskitetty tallennus:** skeeman metatiedot ja liukumatiedot tallennetaan dignan observability-skeemaan visualisointia ja analytiikkaa varten.  
- **Automaatio:** tukee ajastettuja tai tapahtumapohjaisia skannauksia digna Coren tai ulkoisten orkestrointityökalujen kautta.  

---

## Esimerkkitapaukset

| Käyttötapaus | Kuvaus |
|-----------|--------------|
| **ETL-putkien vakauden seuranta** | Havaitse ylätason rakenteelliset muutokset ennen kuin putket epäonnistuvat skeemayhteensopimattomuuksien vuoksi. |
| **Business Intelligence -luotettavuus** | Estä rikkinäiset dashboardit, joita aiheuttaa uudelleennimetyt tai puuttuvat sarakkeet. |
| **Tietovaraston hallinta** | Säilytä auditoitava historia skeeman kehityksestä vaatimustenmukaisuutta ja muutosten vaikutusanalyysiä varten. |
| **Integraation valvonta** | Varmista, että datalake- ja varastoskema pysyvät synkronoituna rakenteellisten päivitysten jälkeen. |

---

## Hyödyt

| Alue | Hyöty |
|------|----------|
| **Datan laatu** | Estää havaitsematonta skeeman liukumista, joka voi korruptoida tai mitätöidä dataputkia. |
| **Observabiliteetti** | Lisää rakenteellista seurantaa osaksi dataympäristöjen kokonaisobservabiliteettia. |
| **Vaatimustenmukaisuus** | Säilyttää versionoidun skeemahistorian auditointia, jäljitettävyyttä ja muutoksenhallintaa varten. |
| **Ennaltaehkäisy** | Havaitsee rakenteelliset ongelmat ennen kuin ne leviävät raportointi- tai tuotantovirheiksi. |

---

## Kuinka se toimii

1. **Otoskeruu** – digna ottaa talteen nykyisen skeeman metatiedot.  
2. **Vertaaminen** – uusi otos verrataan