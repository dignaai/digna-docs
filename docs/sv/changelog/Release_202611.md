---
title: digna Release 2026.11 | Data Reconciliation, digna Agentic & digna Engine
description: Läs vad som är nytt i digna Release 2026.11. Denna version introducerar tre stora tillägg - digna Data Reconciliation, digna Agentic med digna MCP Server, och digna Engine, som möjliggör kontroller av referensintegritet mellan olika databastekniker.
keywords: digna Release 2026.11, digna ändringslogg, digna Data Reconciliation, dataavstämning, ETL-validering, avstämning från källa till mål, digna Agentic, digna MCP Server, AI-agenter datakvalitet, digna Engine, referensintegritet mellan anslutningar, frågeattribut, dataprofilering, data observability
image: /assets/logo_square.png
---

# Ändringslogg – Release 2026.11  

Release 2026.11 är uppbyggd kring tre stora tillägg:

- **digna Data Reconciliation**: kontrollerar att data förblir konsekventa när de flyttas mellan system  
- **digna Agentic**: öppnar digna för AI-agenter via digna MCP Server  
- **digna Engine**: profilerar valfritt data inuti digna och möjliggör kontroller av referensintegritet mellan olika databastekniker  

---

## Nya funktioner  

### digna Data Reconciliation (Beta) – Konsekvens från källa till mål  
Data passerar ofta flera system innan de når en rapport. digna Data Reconciliation jämför en **mål**-datakälla med de **källor** den byggdes från och larmar när de inte längre stämmer överens.

- Konfigureras som namngivna regler på den nya fliken **Data Reconciliation** i måldatakällan  
- Varje datakälla i projektet där Data Reconciliation är aktiverat kan vara en källa  
- Användningsområden är bland annat standardiserade avstämningsrutiner och validering av resultaten från ETL-processer  
- Två typer av regler: **Exact** och **AI**  

**Exact-regler – Avstämning som en datakvalitetsregel**: Du definierar exakt vad som måste stämma överens mellan en källa och ett mål, som i en datakvalitetsregel.

  - Jämför en källdatakälla med en måldatakälla  
  - Para ihop en kontroll i målet med en kontroll i källan efter statistik och attribut, t.ex. radantal eller summan av en beloppskolumn  
  - Tillåt en differens med en **absolute** tolerans (t.ex. ± 10) eller en **relative** tolerans (t.ex. ± 0,5 % av källan)  
  - Tidslinjen visar varje dags differens mot toleransen  

**AI-regler – Avstämning som data observability**: digna lär sig hur ett mål följer sina källor, på samma sätt som digna observerar data i andra moduler, och larmar när sambandet bryts.

  - Kombinera kontroller från flera källdatakällor med kontrollerna i ett mål  
  - Du behöver inte känna till eller skriva ner logiken mellan dem (joins, filter, aggregeringar)  
  - En modell lär sig av historiken hur målet följer sina källor samma dag  
  - Varje kontroll i målet prediceras från dagens källvärden, och digna larmar när målet lämnar bandet som bildas av regelns egna tidigare fel  
  - Varje regel har egna **Model settings**: **Sensitivity**, **Memory** och **Model Complexity**  

Avstämningskontroller visas på Dashboard med en tidslinje per regel. De räknas in i den övergripande inspektionsstatusen och utlöser notifieringar.

**Påverkan:** Täcker båda sidorna av avstämningen. Exact-regler upprätthåller kända kontroller mellan källa och mål, och AI-regler övervakar komplexa flöden som ETL-processer, så att data som går förlorade eller ändras på vägen upptäcks utan handskriven avstämnings-SQL.

---

### digna Agentic (Beta) – digna för AI-agenter  
Den första versionen av digna Agentic. AI-agenter kan nu arbeta med digna, besvara affärsfrågor om dina data och hjälpa till att förbättra din konfiguration.

**digna MCP Server**: Låter Claude och andra AI-agenter arbeta med digna via Model Context Protocol.

  - Hantera projekt, datakällor, regler, inspektionsscheman och prenumerationer  
  - Läs inspektionsstatus ner till den enskilda kontrollen för att utreda larm  

**Beskrivningar av datakällor och attribut**: Beskriv med vanligt språk vad en datakälla eller ett attribut innehåller.

  - AI-agenter använder beskrivningarna för att tolka dina data  
  - Ställ affärsfrågor om dina data, så besvarar AI-agenter dem utifrån det som digna övervakar  
  - Om dignas nuvarande konfiguration inte kan besvara en fråga föreslår AI-agenten där det är möjligt ändringar av datakällan och dess attribut, t.ex. att lägga till ett nytt dataset  

**Påverkan:** Låter dig ställa affärsfrågor om dina data med vanligt språk, och låter AI-agenter hjälpa till att konfigurera digna och utreda datakvalitetsproblem.

---

### digna Engine – Profilera där du väljer  
Som standard profilerar digna data där de finns, i källdatabasen. digna Engine lägger till ett alternativ: digna exporterar data från källan och profilerar dem inuti digna Engine.

- Valfritt, inte obligatoriskt: profilering i källdatabasen finns kvar  
- Väljs per databasanslutning som dess **profileringsplats**: **Source Database** eller **digna Engine**  
- Tillgängligt för alla källtekniker som stöds  

**Referensintegritet mellan anslutningar**: Vissa kontroller kräver att data exporteras. digna Engine utökar **digna Data Validation** för dessa fall.

  - **Kontroller av referensintegritet** mellan datakällor på **olika databasanslutningar**, även med olika databastekniker (t.ex. Oracle och PostgreSQL)  
  - Fungerar med båda profileringsplatserna: för Source Database exporteras endast nyckelkolumnerna till digna Engine  
  - Dashboarden visar när en kontroll körs över två anslutningar  

**Påverkan:** Låter dig välja var data profileras, och upprätthåller relationer mellan system som körs på olika databastekniker.

---

## Förbättringar av profilering  

Den här releasen ger också användarna mer kontroll över vad som profileras och hur.

### Frågeattribut – Användardefinierade kolumner  
- Definiera artificiella kolumner: ett SQL-uttryck över en eller flera kolumner i datakällan  
- Varje frågeattribut har ett eget namn  
- Profileras och kontrolleras som vilket annat attribut som helst  

### Kolumnkategorin DATE  
- Ny kategori **Date** för attribut  
- Mätvärden relativa till det inspekterade datumet  

### Profilering på begäran  
- Profilera valfritt attribut mot en dags fullständiga ögonblicksbild, utan att köra en inspektion  
- Hjälper dig att ställa in attributets kolumntyp: **Numerical**, **Categorical**, **Date** eller **Unspecified**  

---

## Vem gynnas av denna release  

- **Dataingenjörer:** Validering av ETL-resultat med digna Data Reconciliation  
- **Ekonomi-, risk- och controllingteam:** Standardiserade avstämningsrutiner som exakta regler i digna Data Reconciliation  
- **Team för datakvalitet och data governance:** Referensintegritet över databastekniker med digna Engine  
- **Affärsanvändare:** Affärsfrågor om data som besvaras av AI-agenter med digna Agentic  
- **AI- och automationsteam:** AI-agenter som arbetar med digna via digna Agentic  

---

## CLI-uppdateringar  
- Inga ändringar  

---
