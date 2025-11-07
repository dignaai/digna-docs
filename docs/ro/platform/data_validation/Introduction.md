---
title: Data Validation – Verificări bazate pe reguli pentru conformitate & auditabilitate | Documentație digna
description: Descoperiți cum digna Data Validation impune verificări deterministe, bazate pe reguli, cu praguri, intervale și liste de referință. Asigurați conformitatea, auditabilitatea și raportarea pentru reglementări în finanțe, sănătate și alte industrii sensibile la date.
image: /assets/logo_square.png
keywords:
  - validare date
  - verificări bazate pe reguli pentru date
  - calitatea datelor
  - observabilitatea datelor
  - praguri și intervale
  - validarea listelor de referință
  - auditabilitate
  - monitorizarea conformității
  - digna Data Validation
lang: ro
robots: index, follow
og_title: Data Validation – Verificări bazate pe reguli pentru conformitate & auditabilitate | Documentație digna
og_description: digna Data Validation impune verificări deterministe, bazate pe reguli, cu praguri, intervale și liste de referință. Proiectat pentru industrii reglementate, asigură conformitate, transparență și auditabilitate.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Rule-Based Checks
<h1 style="display:none;">Modul Data Validation bazat pe AI pentru calitatea datelor și observabilitate – digna</h1>

---

## Scop

Modulul **Data Validation** asigură **calitatea datelor** prin verificări precise, bazate pe reguli.  
Permite organizațiilor să definească logica deterministă de validare, atât de business, cât și tehnică, garantând că datele respectă standardele de conformitate, SLA-urile contractuale și cerințele de reglementare.

Combinând *executarea regulilor direct în baza de date*, *trasee complete de audit* și *integrarea cu alte module digna*, **Data Validation** garantează **calitatea datelor și observabilitatea** consecventă și trasabilă în medii enterprise complexe.

---

## Prezentare tehnică

### Tipuri de validare acceptate

- **Verificări de egalitate**  
  Confirmă că valorile corespund rezultatelor așteptate (de ex., coduri de referință, flaguri booleene, mapări categorice).

- **Praguri & Intervale**  
  Validează măsuri numerice sau KPI-uri față de limite definite — statice sau derivate dinamic.

- **Liste de referință & Lookups**  
  Verifică dacă valorile din câmp există în seturi master aprobate (de ex., coduri TVA, liste ISO de țări, cataloage de produse).

- **Consistență între coloane**  
  Asigură corectitudinea relațională (de ex., moneda se aliniază cu regiunea, categoria de risc corespunde tipului de activ).

- **Reguli pentru gestionarea valorilor NULL**  
  Detectează valori NULL sau goale neașteptate în coloane critice.

### Execuție și înregistrare

- **Procesare în baza de date** – Toate regulile de validare se execută direct în baza dvs. de date (Teradata, Snowflake, Databricks, PostgreSQL, etc.).  
- **Fără extragere a datelor** – digna nu transferă niciodată date brute în afara mediului dvs.  
- **Trasabilitate completă** – Rezultatul fiecărei reguli este înregistrat cu marcă temporală, setul de date responsabil, numărul de înregistrări și rezultatul trecere/eșec.  
- **Audit**
