---
title: digna Release 2025.04 | Inspection Hub, Meertalige ondersteuning, Module Analytics
description: Leer wat nieuw is in digna Release 2025.04. Deze versie introduceert de Inspection Hub, meertalige ondersteuning (Engels, Duits, Pools), import/export van data sources via dignacli, de eerste release van Module Analytics en een verbeterde dashboard-ervaring.
keywords: digna Release 2025.04, digna changelog, digna inspection hub, digna meertalige ondersteuning, digna module analytics, digna import export, digna CLI, release-opmerkingen, data observability, data quality monitoring
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Changelog – Release 2025.04

Met Release 2025.04 zet digna een grote stap in het eenvoudiger beheren van datakwaliteit en observability, het transparanter maken voor teams en het toegankelijker maken voor gebruikers wereldwijd.  
Deze release combineert **krachtige nieuwe functies**, **verbeteringen in workflow-automatisering** en **verfijningen in de gebruikerservaring**.  

---

## Nieuwe functies

### Inspection Hub – Een nieuw commandocentrum
De **Inspection Hub** is nu beschikbaar als de centrale plek om al je inspectiejobs te beheren. In plaats van te moeten schakelen tussen verschillende modules of volledig afhankelijk te zijn van command-line uitvoering, kun je nu je inspecties vanuit één gestroomlijnde interface monitoren en aansturen.  

Belangrijke mogelijkheden zijn onder andere:  
- Inspecties op aanvraag: Start nieuwe jobs direct wanneer je verse resultaten nodig hebt.  
- Inspectiegeschiedenis: Zie een tijdlijn van inspecties — wat is uitgevoerd, wie het heeft gestart en wanneer.  
- Statustracking: Jobs zijn duidelijk gemarkeerd als voltooid, bezig of in behandeling.  
- Inzicht in aanroepen: Controleer snel of een inspectie is gestart door een gebruiker, een scheduler of de CLI.  
- Opschoonhulpmiddelen: Verwijder verouderde of onnodige jobs om je werkomgeving overzichtelijk te houden.  
- Gedetailleerde logs: Bekijk per job hoe lang deze duurde, welke bronnen waren inbegrepen en hoe drempels werden toegepast.  

De Inspection Hub geeft teams **end-to-end zichtbaarheid en controle**, waardoor inspecties eenvoudiger te beheren zijn in grote projecten.  

---

### Meertalige ondersteuning – digna spreekt jouw taal
digna is nu klaar voor internationale teams met de introductie van **meertalige ondersteuning**.  

In deze release kun je je **voorkeursinterface-taal** direct instellen in de Gebruikersvoorkeuren. Ondersteunde talen zijn:  
- Engels (VK, VS, CA, AU)  
- Duits (DE, AT, CH)  
- Pools (PL)  

Dit maakt digna toegankelijker voor meertalige organisaties en zorgt voor soepelere adoptie binnen teams in verschillende regio's. Meer talen worden in komende releases toegevoegd.  

---

### Import & Export van data sources – Configuratie eenvoudig gemaakt
Consistentie tussen omgevingen is essentieel in enterprise-implementaties. Met 2025.04 introduceert digna **import/export van data sources** via **dignacli**, het command-line tool voor gevorderde gebruikers.  

Voordelen:  
- Exporteer eenmaal een data source-configuratie en hergebruik deze in Development, Test en Production.  
- Elimineer handmatige herconfiguratie en voorkom kostbare fouten.  
- Ondersteun geautomatiseerde workflows en CI/CD-pipelines met eenvoudige CLI-commando’s (`export-ds` en `import-ds`).  
- Kopieer snel data sources tussen projecten voor betere samenwerking.  

Deze functionaliteit zorgt ervoor dat teams met vertrouwen kunnen uitrollen, wetende dat configuraties in elke omgeving consistent zijn.  

---

### Module Analytics (v1) – Van detectie naar begrip
digna begon als een platform voor anomaliedetectie en monitoring van datakwaliteit. Met Release 2025.04 evolueert het verder met de **eerste versie van Module Analytics**.  

Module Analytics helpt gebruikers **hun data te begrijpen** in plaats van alleen op problemen te reageren. Met deze nieuwe module kun je:  
- Langetermijntrends in je datasets volgen.  
- Volatiliteit detecteren en monitoren om fluctuaties te begrijpen.  
- Het gedrag van data in de tijd verkennen voor diepere context.  

Bijvoorbeeld, digna kan automatisch benadrukken dat *“Het aantal rijen sinds het begin van het jaar met 15,8% is toegenomen.”*  
Geen SQL-query’s, geen handmatige controles — alleen **actiegerichte inzichten in één oogopslag**.  

Dit is de basis van digna’s ontwikkeling richting geavanceerde data-analyse, waardoor datateams kunnen verschuiven van reactieve naar proactieve monitoring.  

---

### Dashboardverbeteringen – Een soepelere gebruikerservaring
Naast de grote functies bevat Release 2025.04 diverse **dashboardverfijningen** die bedoeld zijn om digna intuïtiever en aangenamer in gebruik te maken:  
- Snellere navigatie tussen projecten en inspecties.  
- Een schonere lay-out voor inspectielogs en job-submissies.  
- Subtiele ontwerpaanpassingen die helpen inzichten sneller te vinden.  

Deze verbeteringen zijn direct gebaseerd op klantfeedback en tonen onze voortdurende inzet om digna **een platform voor dagelijks gebruik** te maken.  

---

## Algemene verbeteringen
- Prestatieoptimalisaties voor inspectiejobs over grote datasets.  
- Verbeterde foutafhandeling in dignacli voor duidelijkere feedback.  
- Stabiliteitsverbeteringen voor projecten met veel gelijktijdige jobs.  
- UI-verfijningen voor het filteren van joblogs en projectbeheer.  

---

## Samenvatting
Release 2025.04 draait om **controle, toegankelijkheid en inzicht**.  

- De nieuwe **Inspection Hub** geeft gebruikers volledig zicht op inspectiejobs.  
- **Meertalige ondersteuning** zorgt dat digna binnen wereldwijde teams gebruikt kan worden.  
- **Import/export-functionaliteit** vereenvoudigt configuratiebeheer tussen omgevingen.  
- **Module Analytics (v1)** verlegt de focus van detectie naar begrip, met trend- en volatiliteitsanalyse.  
- **Dashboardverbeteringen** verfijnen de algehele gebruikerservaring.  

Samen maken deze updates digna krachtiger, gebruiksvriendelijker en internationaler inzetbaar dan ooit tevoren.