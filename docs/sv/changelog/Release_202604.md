---
title: digna Release 2026.04 | Analytics Chart, Enumerations & Validation Rule Templates
description: Läs vad som är nytt i digna Release 2026.04. Denna version introducerar avancerad tidsserieanalys med Analytics Chart, återanvändbara valideringsmallar, uppräkningsvärden för tillåtna värden och relevansvillkor på kolumnnivå.
keywords: digna Release 2026.04, digna changelog, digna Data Analytics, tidsserieanalys, regression, valideringsmallar för data, enumerations, validering av tillåtna värden, data kvalitet regler, data observability
image: /assets/logo_square.png
---

# Changelog – Release 2026.04  

Med Release 2026.04 förbättrar digna avsevärt sina kapabiliteter inom analys och Data Validation.  
Denna release introducerar avancerad tidsserieanalys, återanvändbara valideringskomponenter och centraliserad värdestandardisering.

---

## Nyheter  

### Analytics Chart – Tidsserieanalys utan data science  
- Nytt **Analytics Chart** för interaktiv tidsserieanalys  
- Inbyggda analysmetoder:
    - Linjär, kvadratisk och kubisk regression  
    - Piecewise-regression med konfigurerbara brytpunkter  
    - Utjämningstekniker  
    - Kvantilanalys  
- Automatisk identifiering av trender, säsongsvariationer och mönsterförändringar  
- Residualanalys för djupare insikt i avvikelser  
- Tidsserier beräknas automatiskt för varje dataset  

**Påverkan:** Gör det möjligt för användare att förstå komplex databeteende över tid utan att kräva data science-expertis eller externa verktyg.

---

### Enumerations – Central definition av tillåtna värden  
- Definiera återanvändbara uppsättningar av tillåtna värden (t.ex. länder, delstater, statuskoder)  
- Validera kolumnvärden mot fördefinierade enumerations i **digna Data Validation**  
- Återanvänd enumerations över projekt och datakällor  
- Använd enumerations överallt via `#ENUM:MY_ENUM#`  
- Alla kontroller körs **direkt i källdatabasen**  

**Påverkan:** Säkerställer konsekventa och standardiserade datavärden i hela organisationen.

---

### Validation Rule Templates – Återanvändbar data kvalitetslogik  
- Definiera återanvändbara valideringsregler (t.ex. kontroll av blanksteg, NOT NULL, formatkontroller)  
- Applicera mallar över flera dataset  
- Säkerställ konsekvent regel-logik över projekt  
- Minska duplicering och manuell konfiguration  
- Alla kontroller körs **direkt i källdatabasen**  

**Påverkan:** Möjliggör skalbar och högpresterande datavalidering utan dataprovflyttning.

---

### Relevansvillkor på statistiknivå  
- Definiera relevansvillkor på **kolumnnivå för varje statistik**  
- Utökar konceptet för anomalirelevansvillkor  
- Styr när en statistik ska anses relevant  
- Minska brus genom att exkludera icke-kritiska situationer  

**Påverkan:** Förbättrar signal-kvaliteten genom att fokusera endast på meningsfulla avvikelser.

---

## Utökade Data Analytics & valideringsmöjligheter  

Med denna release utökar digna både förståelsen av data och standardiseringen av datavalidering:

- Avancerad **tidsserieinterpretation** utan data science-kunskap  
- Centraliserad definition av **tillåtna värden via enumerations**  
- Återanvändbar **valideringslogik via mallar**  
- Finkornig kontroll över **relevans för statistik och alerting**  

Tillsammans gör dessa kapabiliteter det möjligt för organisationer att inte bara upptäcka problem, utan också **förstå, standardisera och kontrollera datakvaliteten**.

---

## Vem gynnas av denna release  

- **Data Engineers:** Återanvändbar valideringslogik och förbättrad kontroll över övervakningsbeteende  
- **Data Quality & Governance Teams:** Standardiserade regler och konsekvent datavalidering över system  
- **Analytics & BI Teams:** Bättre förståelse för trender och avvikelser  
- **Platform Owners:** Ökad adoption genom förenklad analys och skalbar validering  

---

## CLI-uppdateringar  
- Inga ändringar  

---