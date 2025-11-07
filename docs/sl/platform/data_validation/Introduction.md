---
title: Data Validation – Preverjanja na osnovi pravil za skladnost in revizijsko sledljivost | digna dokumentacija
description: Odkrijte, kako digna Data Validation izvaja deterministične preverjave na osnovi pravil z mejami, razponi in referenčnimi seznami. Zagotovite skladnost, revizijsko sledljivost in poročanje za regulirana področja, kot so finance in zdravstvo.
image: /assets/logo_square.png
keywords:
  - data validation
  - preverjanja podatkov na osnovi pravil
  - kakovost podatkov
  - kakovost podatkov
  - data observability
  - meje in razponi
  - preverjanje po referenčnih seznamih
  - revizijska sledljivost
  - spremljanje skladnosti
  - digna data validation
lang: en
robots: index, follow
og_title: Data Validation – Rule-Based Checks for Compliance & Auditability | digna Documentation
og_description: digna Data Validation enforces deterministic, rule-based checks with thresholds, ranges, and reference lists. Designed for regulated industries, it ensures compliance, transparency, and auditability.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Rule-Based Checks
<h1 style="display:none;">AI-Driven Data Validation Module for Data Quality and Observability – digna</h1>

---

## Namen

Modul **Data Validation** zagotavlja **kakovost podatkov** s pomočjo natančnih preverjanj na osnovi pravil.  
Omogoča organizacijam, da definirajo deterministične poslovne in tehnične validacijske logike ter s tem zagotovijo, da podatki izpolnjujejo standarde skladnosti, pogodbene SLA in regulatorne zahteve.

S kombinacijo *in-database rule execution*, *complete audit trails* in *integracije z drugimi digna moduli*, **Data Validation** zagotavlja dosledno in sledljivo **kakovost podatkov in opazljivost** v kompleksnih podjetniških okoljih.

---

## Tehnični pregled

### Podprti tipi validacij

- **Preverjanja enakosti**  
  Potrdite, da se vrednosti ujemajo s pričakovanimi rezultati (npr. referenčne kode, Boolean zastavice, kategorialne preslikave).

- **Meje in razponi**  
  Validirajte numerične meritve ali KPI-je glede na določene omejitve — statične ali dinamično izpeljane.

- **Referenčni seznami in poizvedbe (lookups)**  
  Preverite, ali vrednosti polj obstajajo v odobrenih glavnih podatkovnih nizih (npr. DDV kode, ISO seznami držav, produktni katalogi).

- **Konsistentnost med stolpci**  
  Zagotovite relacijsko pravilnost (npr. valuta ustreza regiji, kategorija tveganja se ujema z vrsto premoženja).

- **Pravila za ravnanje z NULL vrednostmi**  
  Zaznajte nepričakovane NULL ali prazne vrednosti v kritičnih stolpcih.

### Izvedba in beleženje

- **In-database processing** – Vsa pravila se izvajajo neposredno v vaši bazi podatkov (Teradata, Snowflake, Databricks, PostgreSQL itd.).  
- **Brez izvažanja podatkov** – digna nikoli ne prenaša surovih podatkov izven vašega okolja.  
- **Popolna sledljivost** – Vsak rezultat pravila je zabeležen z žigom časa, odgovornim naborom podatkov, številom zapisov in izidom (uspeh/neuspeh).  
- **Revizija**