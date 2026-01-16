---
title: Data Validation – Reeglipõhised kontrollid vastavuse ja auditeeritavuse jaoks | digna Documentation
description: Avastage, kuidas digna Data Validation rakendab deterministlikke reeglipõhiseid kontrolle koos lävendite, vahemike ja viitenimekirjadega. Tagage vastavus, auditeeritavus ja regulatiivne aruandlus finants-, tervishoiu- ja teistes andmetundlikes valdkondades.
image: /assets/logo_square.png
keywords:
  - andmete valideerimine
  - reeglipõhised andmekontrollid
  - andmekvaliteet
  - andmete kvaliteet
  - andmete jälgitavus
  - lävendid ja vahemikud
  - viitenimekirjade valideerimine
  - auditeeritavus
  - vastavuse jälgimine
  - digna data validation
lang: et
robots: index, follow
og_title: Data Validation – Reeglipõhised kontrollid vastavuse ja auditeeritavuse jaoks | digna Documentation
og_description: digna Data Validation rakendab deterministlikke, reeglipõhiseid kontrolle koos lävendite, vahemike ja viitenimekirjadega. Mõeldud reguleeritud tööstusharudele, tagab see vastavuse, läbipaistvuse ja auditeeritavuse.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Rule-Based Checks
<h1 style="display:none;">Tehisintellekti juhitud Data Validation moodul andmekvaliteedi ja jälgitavuse jaoks – digna</h1>

---

## Eesmärk

The **Data Validation** module tagab **andmete kvaliteedi** täpsete, reeglipõhiste kontrollide kaudu.  
See võimaldab organisatsioonidel määratleda deterministliku ärilise ja tehnilise valideerimisloogika, tagades, et andmed vastavad vastavusstandarditele, lepingulistele SLA-dele ja regulatiivsetele nõuetele.

Kombineerides *andmebaasis reeglite täideviimist*, *täielikke auditeerimisjälgi* ja *integreerimist teiste digna-moodulitega*, garanteerib **Data Validation** järjepideva ja jälgitava **andmekvaliteedi ja jälgitavuse** keerukates ettevõttekeskkondades.

---

## Tehniline ülevaade

### Toetatud valideerimistüübid

- **Võrdluskontrollid**  
  Kinnitage, et väärtused vastavad oodatule (nt viitekoodid, Boolean-lipud, kategoorilised seosed).

- **Lävendid & Vahemikud**  
  Valideerige numbrilisi mõõdikuid või KPI-sid määratletud piiride vastu — staatilised või dünaamiliselt tuletatud.

- **Viitenimekirjad & Otsingud**  
  Kontrollige, kas välja väärtused eksisteerivad kinnitatud master-andmekogudes (nt käibemaksukoodid, ISO riikide nimekirjad, tootekataloogid).

- **Veergudevaheline järjepidevus**  
  Tagage seoste õigsus (nt valuuta vastab regioonile, riskikategooria vastab varatüübile).

- **Nullväärtuste käsitlemise reeglid**  
  Tuvastage ootamatud null- või tühiväärtused kriitilistes veergudes.

### Täideviimine ja logimine

- **Andmebaasis töötlemine** – kõik valideerimisreeglid käivitatakse otse teie andmebaasis (Teradata, Snowflake, Databricks, PostgreSQL jne).  
- **Andmete väljavõtmine puudub** – digna ei edasta kunagi toorandmeid teie keskkonnast välja.  
- **Täielik jälgitavus** – iga reegli tulemus logitakse ajatempli, vastutava andmekomplekti, rekordiarvude ning läbinud/ebaõnnestunud tulemuste koosseisus.  
- **Audit**
