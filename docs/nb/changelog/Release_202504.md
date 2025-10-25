---
title: digna Release 2025.04 | Inspection Hub, flerspråklighet, Module Analytics
description: Lær hva som er nytt i digna Release 2025.04. Denne versjonen introduserer Inspection Hub, flerspråklig støtte (engelsk, tysk, polsk), import/eksport av datakilder via dignacli, den første utgaven av Module Analytics, og en forbedret dashbord-opplevelse.
keywords: digna Release 2025.04, digna changelog, digna inspection hub, digna multi-language support, digna module analytics, digna import export, digna CLI, release notes, data observability, data quality monitoring
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Endringslogg – Release 2025.04

Med Release 2025.04 tar digna et stort skritt mot å gjøre datakvalitet og observability enklere å håndtere, mer gjennomsiktig for team, og tilgjengelig for brukere over hele verden.  
Denne utgivelsen kombinerer **kraftige nye funksjoner**, **forbedringer i arbeidsflytautomasjon**, og **forfinelser i brukeropplevelsen**.  

---

## Nye funksjoner

### Inspection Hub – Et nytt kontrollsenter
**Inspection Hub** er nå tilgjengelig som det sentrale stedet for å administrere alle dine inspeksjonsjobber. I stedet for å hoppe mellom forskjellige moduler eller stole utelukkende på kommandolinjen, kan du nå overvåke og kontrollere inspeksjonene dine fra ett strømlinjeformet grensesnitt.  

Hovedfunksjoner inkluderer:  
- Inspeksjoner på forespørsel: Start nye jobber umiddelbart når du trenger ferske resultater.  
- Inspeksjonshistorikk: Se en tidslinje over inspeksjoner — hva som ble kjørt, hvem som utløste det, og når.  
- Statussporing: Jobber er tydelig merket som fullført, pågående eller ventende.  
- Innsikt om utløser: Sjekk raskt om en inspeksjon ble startet av en bruker, en scheduler eller CLI.  
- Ryddeverktøy: Slett utdaterte eller unødvendige jobber for å holde arbeidsområdet ryddig.  
- Detaljerte logger: Grav deg inn i hver jobb for å se hvor lang tid den tok, hvilke kilder som var inkludert, og hvordan terskler ble anvendt.  

Inspection Hub gir team **end-to-end synlighet og kontroll**, og gjør inspeksjoner enklere å administrere i store prosjekter.  

---

### Flerspråklig støtte – digna snakker ditt språk
digna er nå klar for internasjonale team med introduksjonen av **flerspråklig støtte**.  

I denne versjonen kan du angi ditt **foretrukne grensesnittsspråk** direkte i Brukerinnstillinger. Støttede språk inkluderer:  
- Engelsk (UK, US, CA, AU)  
- Tysk (DE, AT, CH)  
- Polsk (PL)  

Dette gjør digna enklere å bruke for flerspråklige organisasjoner og sikrer smidigere adopsjon på tvers av team som jobber i forskjellige regioner. Flere språk vil bli lagt til i kommende utgivelser.  

---

### Import & eksport av datakilder – Konfigurasjon gjort enkelt
Konsistens på tvers av miljøer er essensielt i bedriftsdistribusjoner. Med 2025.04 introduserer digna **import/eksport av datakilder** via **dignacli**, kommandolinjeverktøyet for avanserte brukere.  

Fordeler:  
- Eksporter en datakildekonfigurasjon én gang, og gjenbruk den i Development, Test og Production.  
- Eliminér manuell rekonfigurasjon og unngå kostbare feil.  
- Støtt automatiserte arbeidsflyter og CI/CD-pipelines med enkle CLI-kommandoer (`export-ds` og `import-ds`).  
- Kopier raskt datakilder mellom prosjekter for enklere samarbeid.  

Denne funksjonaliteten sørger for at team kan distribuere med selvtillit, vel vitende om at konfigurasjonene er konsistente i alle miljøer.  

---

### Module Analytics (v1) – Fra deteksjon til forståelse
digna startet som en plattform for anomali-deteksjon og overvåking av datakvalitet. Med Release 2025.04 utvikler den seg videre med **første versjon av Module Analytics**.  

Module Analytics hjelper brukere å **forstå dataene sine** i stedet for bare å reagere på problemer. Med denne nye modulen kan du:  
- Spore langsiktige trender i datasettene dine.  
- Oppdage og overvåke volatilitet for å forstå svingninger.  
- Utforske datatilførselens oppførsel over tid for dypere kontekst.  

For eksempel kan digna automatisk fremheve at *«Raderantallet økte med 15,8 % siden årets begynnelse.»*  
Ingen SQL-spørringer, ingen manuelle kontroller — bare **handlingsrettede innsikter ved et øyeblikks oversikt**.  

Dette er grunnlaget for dignas reise mot avansert dataanalyse, og gjør det mulig for datateam å gå fra reaktiv til proaktiv overvåking.  

---

### Forbedringer av dashbordet – En jevnere brukeropplevelse
Utover de store funksjonene inneholder Release 2025.04 flere **forbedringer av dashbordet** designet for å gjøre digna mer intuitivt og hyggelig å bruke:  
- Raskere navigering mellom prosjekter og inspeksjoner.  
- Et ryddigere oppsett for inspeksjonslogger og jobbinnleveringer.  
- Subtile designjusteringer som hjelper deg å finne innsikter raskere.  

Disse forbedringene er basert direkte på kundetilbakemeldinger og viser vårt kontinuerlige engasjement for å gjøre digna **en plattform bygget for daglig bruk**.  

---

## Generelle forbedringer
- Ytelsesoptimaliseringer for inspeksjonsjobber over store datasett.  
- Forbedret feilhåndtering i dignacli for å gi klarere tilbakemeldinger.  
- Stabilitetsforbedringer for prosjekter med mange samtidige jobber.  
- UI-forbedringer for filtrering av jobblogger og prosjektadministrasjon.  

---

## Oppsummering
Release 2025.04 handler om **kontroll, tilgjengelighet og innsikt**.  

- Det nye **Inspection Hub** gir brukere full synlighet i inspeksjonsjobber.  
- **Flerspråklig støtte** sørger for at digna kan brukes av globale team.  
- **Import/eksport-funksjonalitet** forenkler konfigurasjonshåndtering på tvers av miljøer.  
- **Module Analytics (v1)** flytter fokuset fra deteksjon til forståelse, med trend- og volatilitetssporing.  
- **Forbedringer av dashbordet** finjusterer den totale brukeropplevelsen.  

Sammen gjør disse oppdateringene digna mer kraftfull, brukervennlig og internasjonalt klar enn noen gang.