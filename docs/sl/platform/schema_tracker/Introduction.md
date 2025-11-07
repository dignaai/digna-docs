---
title: Data Schema Tracker – Spremljanje razvoja shem | digna Dokumentacija
description: Spoznajte, kako digna Data Schema Tracker spremlja spremembe stolpcev, posodobitve podatkovnih tipov in drift shem. Odkrijte in opozorite na namerne in nenamerne spremembe sheme, da preprečite napake ETL, pokvarjene nadzorne plošče in izgubo opazljivosti podatkov.
canonical_url: https://docs.digna.ai/platform/data_schema_tracker/
image: /assets/logo_square.png
keywords:
  - sledenje shem podatkov
  - zaznavanje drift sheme
  - spremljanje razvoja shem
  - opazljivost metapodatkov
  - opazljivost podatkov
  - kakovost podatkov
  - spremljanje strukture podatkov
  - metapodatki baze podatkov
  - stabilnost ETL cevovodov
  - digna Data Schema Tracker
lang: sl
robots: index, follow
og_title: Data Schema Tracker – Spremljanje razvoja shem | digna Dokumentacija
og_description: digna Data Schema Tracker spremlja drift sheme, spremembe podatkovnih tipov in posodobitve stolpcev. Prejmite opozorila pred tem, ko ETL cevovodi ali nadzorne plošče odpovejo zaradi nepričakovanih sprememb strukture.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Spremljanje razvoja shem
<h1 style="display:none;">Modul, poganjan z AI, za opazljivost metapodatkov in kakovost podatkov – digna Data Schema Tracker</h1>

---

## Namen

The **Data Schema Tracker** vas obvešča o tem, kako se razvijajo strukture vaše baze podatkov.  
Neprestano spremlja **sheme tabel, stolpce in podatkovne tipe**, da zazna **drift sheme** — namenske ali nenamerne strukturne spremembe, ki lahko povzročijo motnje v cevovodih, ETL opravilih ali BI nadzornih ploščah.

Z zagotavljanjem preglednosti pri razvoju shem digna organizacijam pomaga ohranjati **zaupanje v kakovost podatkov**, vzdrževati **opazljivost podatkovnih sistemov** in se izogniti dragim incidentom v produkciji, ki nastanejo zaradi nezaznanih sprememb sheme.

---

## Tehnični pregled

### Kaj spremlja

- **Dodani ali odstranjeni stolpci** – zazna novo uvedene, preimenovane ali izbrisane stolpce.  
- **Spremembe podatkovnih tipov** – prepozna spremembe, kot so `INT → VARCHAR` ali `DATE → TIMESTAMP`.  
- **Spremembe tabel in pogledov** – sledi ustvarjanju, preimenovanju ali odstranitvi tabel in pogledov.  
- **Razlike med okolji** – primerja različice shem med Dev, Test in Production okolji.  

### Zaznavanje in obveščanje

- Pregleduje **metapodatke baze podatkov** ali **sistemske kataloge** neposredno znotraj vaše podatkovne platforme.  
- Primerja vsak posnetek sheme z prej znano različico, shranjeno v digna observability schema.  
- Generira **realnočasovna opozorila** v nadzorni plošči, preko API ali zunanjih kanalov za obveščanje (e-pošta, Slack, webhook).  
- Beleži vsako različico sheme za **zgodovinsko sledenje in pripravo na revizije**.

---

## Arhitektura in izvedba

- **Izvajanje znotraj baze:** digna deluje v celoti znotraj vašega okolja in poizveduje po pogledih z metapodatki, ne da bi izvažal dejanske podatke.  
- **Lahko skeniranje:** dostopa le do strukturnih informacij — nikoli do uporabniških podatkov.  
- **Centralizirano shranjevanje:** metapodatki sheme in zapisi o driftu so shranjeni v digna observability schema za vizualizacijo in analitiko.  
- **Avtomatizacija:** podpira načrtovane ali dogodkovno sprožene preglede preko digna Core ali zunanjih orodij za orkestracijo.  

---

## Primeri uporabe

| Use Case | Description |
|-----------|--------------|
| **ETL Stability Monitoring** | Zaznajte spremembe zgornjega toka strukture, preden cevovodi odpovejo zaradi neusklajenosti sheme. |
| **Business Intelligence Reliability** | Preprečite pokvarjene nadzorne plošče, ki jih povzročijo preimenovani ali manjkajoči stolpci. |
| **Data Warehouse Governance** | Ohranjajte revizijsko sled razvoja shem za skladnost in analizo vplivov. |
| **Integration Oversight** | Zagotovite, da so sheme data lake in skladišča po strukturnih posodobitvah še vedno sinhronizirane. |

---

## Prednosti

| Area | Benefit |
|------|----------|
| **Data Quality** | Preprečuje nezaznan drift sheme, ki lahko pokvari ali razveljavi podatkovne cevovode. |
| **Observability** | Dodaja strukturno spremljanje k splošni opazljivosti podatkovnih ekosistemov. |
| **Compliance** | Ohranja verzionirano zgodovino shem za revizijo, sledljivost in nadzor sprememb. |
| **Prevention** | Zaznava strukturne težave preden se razširijo v poročanje ali produkcijske napake. |

---

## Kako deluje

1. **Zajem posnetka** – digna zajame trenutne metapodatke sheme.  
2. **Primerjava** – nov posnetek se primerja