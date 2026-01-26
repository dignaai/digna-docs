---
title: digna Release 2026.01 | Logiska datasources, globala anslutningar & Avancerad Data Validation
description: Ta reda på vad som är nytt i digna Release 2026.01. Denna version introducerar globala databasanslutningar, logiska datasources, anomalirelevansvillkor, CSV-exporter och avancerad Data Validation inklusive kontroller av referensintegritet.
keywords: digna Release 2026.01, digna ändringslogg, digna datasource, digna databasanslutningar, digna Data Anomalies, digna Data Validation, validering av referensintegritet, regler för datakvalitet, dataobservabilitet, digna CSV-export
image: /assets/logo_square.png
---

# Ändringslogg – Release 2026.01  

Med Release 2026.01 introducerar digna stora förbättringar av modellering av datasources, hantering av anslutningar och användbarheten vid inspektioner.  
Denna version ökar flexibiliteten i alla moduler och utökar avsevärt täckningen för datakvalitet och validering.

---

## 🚀 Nya funktioner  

### Globala databasanslutningar  
- Databasanslutningar konfigureras nu på **global nivå**.  
- Globala anslutningar kan återanvändas i **alla projekt**, vilket förenklar konfiguration och underhåll.  
- **Påverkan:** Minskar driftmässig arbetsbelastning och säkerställer konsekvent uppkoppling över miljöer.

### Flera källanslutningar per projekt  
- Projekt kan nu referera till **flera konfigurationsinställningar för källanslutningar**.  
- Möjliggör mer flexibla uppsättningar för komplexa datalandskap per projekt.  
- **Påverkan:** Stödjer realistiska företagsarkitekturer med heterogena datakällor.

### Logiska datasources  
- Datasources representerar nu ett **logiskt lager** inom ett projekt.  
- Varje datasource kan stödjas av:
    - en **databastabell**
    - en **databasvy**
    - en **anpassad SQL-sats**  
- Denna separation förbättrar återanvändning, tydlighet och inspektionsmodellering över moduler.  
- **Påverkan:** Frikopplar inspektioner och regler för datakvalitet från fysisk lagring, vilket förbättrar underhållbarhet och återanvändning.

### Anomalirelevansvillkor  
- Ett **Anomaly Relevance Condition** kan nu definieras för att styra utvärdering av anomalistatus på dataset-nivå.  
- Statistik beräknas oberoende av huruvida villkoret är satt eller uppfyllt.  
- Om villkoret **inte uppfylls** ger **digna Data Anomalies** ingen anomalistatus (grön / gul / röd).  
- **Exempel:** Exkludera datasetet från anomalievaluering när antalet rader är under 10.  
- **Påverkan:** Säkerställer att anomalier endast utvärderas i relevanta affärskontexter.

### Notifieringskonfiguration per modul  
- Notifieringar kan nu konfigureras **per modul** direkt i digna.  
- Möjliggör oberoende styrning av varningsbeteende för **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** och andra moduler.  
- **Påverkan:** Gör det möjligt att ha precisa larmstrategier i linje med teamansvar och kritikalitet.

### Export av inspektionsresultat (CSV)  
- Användare kan nu **ladda ner inspektionsresultat som CSV-filer**.  
- Möjliggör offline-analys, rapportering och integration med externa verktyg.  
- **Påverkan:** Förenklar revisioner, rapportering och efterföljande analys av datakvalitet.

---

## 🧪 Utökade möjligheter i digna Data Validation  

Med denna release stödjer **digna Data Validation** nu ett omfattande uppsättning regler för datakvalitet:

- **Radnivåvalideringsregler**  
- **Unikhetskontroller över flera kolumner**  
- **Validering av referensintegritet över datasources**

Tillsammans möjliggör dessa kontroller upprätthållande av **strukturella och relationella regler för datakvalitet** över komplexa datalandskap.

### Unikhetskontroller för flera kolumner
- Infört **unikhetskontroller** för en konfigurerbar **uppsättning kolumner**.  
- Möjliggör validering av sammansatta nycklar och affärsnivåbegränsningar för unikhet.  
- **Påverkan:** Upptäcker dubbletter av affärsenheter som inte kan identifieras med enkelkolumns-kontroller.

### Referensintegritetskontroller
- Infört **referensintegritetskontroller** för att validera relationer mellan datasources.  
- Säkerställer att **värden för främmande nycklar** i en källdatasource finns i den refererade måldatasourcen.  
- Hjälper till att upptäcka föräldralösa poster, brutna relationer och inkonsekvenser i data tidigt.  
- Utformade för att fungera med **logiska datasources**, inklusive vyer och anpassade SQL-satser.  
- **Användningsfall:** datalagrets integritet, regulatorisk rapportering, konsistens i masterdata och pålitlig analys nedströms.

---

## 🎯 Vem gynnas av denna release  

- **Dataingenjörer:** Mer flexibel modellering av datasources och återanvändbara databasanslutningar  
- **Datakvalitet- och styrningsteam:** Utökad valideringstäckning inklusive regler för referensintegritet  
- **Analys- och BI-team:** Renare ingångsdata och exportbara inspektionsresultat  
- **Plattformsägare:** Minskad konfigurationskomplexitet och förbättrad driftsmässig underhållbarhet

---

## 🛠 CLI-uppdateringar  
- Inga förändringar

---