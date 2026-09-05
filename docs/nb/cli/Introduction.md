---
title: digna CLI-referanse – Introduksjon | digna-dokumentasjon
description: Introduksjon til digna kommandolinjegrensesnitt (CLI) — et tekstbasert verktøy for å automatisere og administrere digna-ressurser, inkludert grunnleggende installasjon på Windows.
keywords: digna cli, digna kommandolinje, digna automatisering, digna skripting, cli-referanse, dignacli installasjon
image: /assets/logo_square.png
---

## Formål med kommandolinjegrensesnittet (CLI)

Kommandolinjegrensesnittet (CLI) for ***digna*** er et kraftig verktøy utviklet for å effektivisere interaksjoner med ***digna***-plattformen. Det gir et tekstbasert grensesnitt som lar brukere utføre et bredt spekter av oppgaver effektivt, uten behov for et grafisk brukergrensesnitt.

### Nøkkelfunksjoner:

- **Effektivitet og fleksibilitet:** CLI-en muliggjør rask kjøring av kommandoer og forbedrer produktiviteten.
- **Automatisering:** Støtter skripting for å automatisere repeterende oppgaver.
- **Fjerntilgang:** Administrer ***digna***-ressurser fra hvor som helst.
- **Konsistens og pålitelighet:** Sikrer pålitelige operasjoner med dokumenterte, versjonskontrollerte kommandoer.
- **Skalerbarhet:** Håndterer storskalaoperasjoner for bedriftsoppgaver.
- **Læring og mestring:** Gir dypere forståelse av ***digna***'s funksjonalitet.
- **Integrasjon med andre verktøy:** Integreres sømløst med automatiseringsverktøy som Control-M, UC4, AutomateNOW!

---

## Installasjonsinstruksjoner for Windows

For å komme i gang, følg trinnene nedenfor for å pakke ut de nødvendige filene, distribuere *dignacli*-mappen og konfigurere tilkoblingen til ***digna*** repository. Sørg for at du har repository-påloggingsinformasjon og eventuelle nødvendige konfigurasjonsdetaljer klare før du begynner.

1. **Utpakking av ***digna*** CLI:**
   - Hent `.zip`-filen som inneholder ***digna*** CLI.
   - Pakk ut filen til ønsket katalog.

2. **Distribuering av `dignacli`-mappen:**
   - Kopier `dignacli`-mappen til ønsket installasjonssted (f.eks. `C:\Program Files\***digna***`).

3. **Konfigurering av `config.toml`:**
   - Sjekk om `config.toml` finnes inne i `dignacli`.
   - Gi nytt navn til `config_template.toml` til `config.toml` om nødvendig, og konfigurer den ved hjelp av den medfølgende dokumentasjonen.