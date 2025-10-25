---
title: digna CLI Reference 2024.12 – Commands & Examples | digna Documentation
description: Fullstendig referanse for digna CLI-utgivelsen 2024.12. Lær hvordan du administrerer brukere, repositories og data med kommandoer som add-user, check-repo-connection, upgrade-repo, inspect og mer.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Denne siden dokumenterer hele settet med kommandoer tilgjengelig i ***digna*** CLI-utgivelsen **2024.12**, inkludert bruks eksempler og alternativer.

---


**2024-12-09**


---

## CLI-grunnleggende

---

## Bruke `help`-alternativet

`--help`-alternativet gir informasjon om tilgjengelige kommandoer og hvordan de brukes. Det finnes to hovedmåter å bruke dette-alternativet på:

1. **Vise generell hjelp:**
   
    Bruk --help umiddelbart etter kommandoen `dignacli`  
   ```bash
   dignacli --help

3.  **Få hjelp for spesifikke kommandoer:**  
  
    For detaljert informasjon om en spesifikk kommando, legg til `--help` etter den kommandoen.
    For eksempel, for å få hjelp med `add-user`-kommandoen, kjør:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Kommando­beskrivelse:** Gir en detaljert beskrivelse av hva kommandoen gjør.  
     - **Syntaks:** Viser nøyaktig syntaks, inkludert nødvendige og valgfrie argumenter.  
     - **Alternativer:** Lister eventuelle alternativer spesifikke for kommandoen, sammen med forklaringer.  
     - **Eksempler:** Gir eksempler på hvordan kommandoen kan kjøres effektivt.

  
## Bruke `check-repo-connection`-kommandoen

`check-repo-connection`-kommandoen er et verktøy i ***digna*** CLI som er designet for å teste tilkobling og tilgang til et spesifisert ***digna*** repository. Denne kommandoen sikrer at CLI-en kan kommunisere med repositoryet.
      
### Kommando-bruk
```bash
dignacli check-repo-connection
```

Ved vellykket kjøring vil kommandoen gi en bekreftelse på tilkoblingen, sammen med detaljer om repositoryet: Repository-versjon, Host, Database og Schema.  
  
Hvis repository-tilkoblingen ikke lykkes, sjekk filen config.toml for korrekte konfigurasjonsinnstillinger.

## Bruke `version`-kommandoen

For å sjekke installert versjon av *dignacli*, bruk --version-alternativet.  
  
### Kommando-bruk
```bash
dignacli --version
```
  
### Eksempelutgang
```bash
dignacli version 2024.12
```

## Bruke loggingsalternativer
  
Som standard er konsollutskriften fra ***digna***-kommandoer utformet for å være minimalistisk. De fleste kommandoer tilbyr muligheten til å gi tilleggsinformasjon ved å bruke følgende alternativer:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” og “debug” definerer detaljnivået, mens “logfile”-bryteren tillater omdirigering av utskriften til en fil i stedet for konsollvinduet.

# Brukeradministrasjon

## Bruke `add-user`-kommandoen
  
`add-user`-kommandoen i ***digna*** CLI brukes for å legge til en ny bruker i ***digna***-systemet.
  
### Kommando-bruk
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenter

- **USER_NAME**: Brukernavnet for den nye brukeren (påkrevd).
- **USER_FULL_NAME**: Fullt navn for den nye brukeren (påkrevd).
- **USER_PASSWORD**: Passordet for den nye brukeren (påkrevd).

### Alternativer

- `--is_superuser`, `-su`: Flag for å angi den nye brukeren som administrator.
- `--valid_until`, `-vu`: Setter en utløpsdato for brukerkontoen i formatet `YYYY-MM-DD HH:MI:SS`. Hvis ikke satt, har kontoen ingen utløpsdato.

### Eksempel

For å legge til en ny bruker med brukernavn `jdoe`, fullt navn `John Doe`, og passord `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
For å legge til en ny bruker og sette en utløpsdato for kontoen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Bruke `delete-user`-kommandoen
  
`delete-user`-kommandoen i ***digna*** CLI brukes for å fjerne en eksisterende bruker fra ***digna***-systemet.
  
### Kommando-bruk
```bash
dignacli delete-user USER_NAME
```
  
### Argumenter
- **USER_NAME**: Brukernavnet til brukeren som skal slettes (påkrevd). Dette er det eneste argumentet kommandoen krever.

### Eksempel
```bash
dignacli delete-user jdoe
```
  
Å kjøre denne kommandoen vil fjerne brukeren `jdoe` fra ***digna***-systemet, tilbakekalle deres tilgang og slette tilknyttede data og tillatelser fra repositoryet.

## Bruke `modify-user`-kommandoen

`modify-user`-kommandoen i ***digna*** CLI brukes for å oppdatere detaljer for en eksisterende bruker i ***digna***-systemet.

### Kommando-bruk
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenter
  
- **USER_NAME**: Brukernavnet til brukeren som skal endres (påkrevd).
- **USER_FULL_NAME**: Det nye fulle navnet for brukeren (påkrevd).
  
### Alternativer  
  
- `--is_superuser`, `-su`: Setter brukeren som superbruker og gir forhøyede privilegier. Dette flagget krever ingen verdi.  
- `--valid_until`, `-vu`: Setter en utløpsdato for brukerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke oppgitt, forblir kontoen gyldig på ubestemt tid.  
  
### Eksempel
  
For å endre fullt navn for brukeren `jdoe` til “Johnathan Doe” og sette brukeren som superbruker:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Bruke `modify-user-pwd`-kommandoen
  
`modify-user-pwd`-kommandoen i ***digna*** CLI brukes for å endre passordet for en eksisterende bruker i ***digna***-systemet.
  
### Kommando-bruk
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenter
  
- **USER_NAME**: Brukernavnet til brukeren hvis passord skal endres (påkrevd).
- **USER_PWD**: Det nye passordet for brukeren (påkrevd).
  
### Eksempel
  
For å endre passordet for brukeren `jdoe` til `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Bruke `list-users`-kommandoen

`list-users`-kommandoen i ***digna*** CLI viser en liste over alle brukere registrert i ***digna***-systemet.

### Kommando-bruk

```bash
dignacli list-users
```

Å kjøre denne kommandoen i ***digna*** CLI vil koble til ***digna***-repositoryet og liste opp alle brukere, vise deres ID, brukernavn, fullt navn, superbruker-status og utløpstidspunkter.

# Repository-administrasjon

### Bruke `upgrade-repo`-kommandoen
  
`upgrade-repo`-kommandoen i ***digna*** CLI brukes for å oppgradere eller initialisere ***digna***-repositoryet. Denne kommandoen er essensiell for å anvende oppdateringer eller sette opp repository-infrastrukturen for første gang.
  
### Kommando-bruk

```bash
dignacli upgrade-repo [options]
```
  
### Alternativer
  
- `--simulation-mode`, `-s`: Når aktivert kjører dette alternativet kommandoen i simulasjonsmodus, som skriver ut SQL-setningene som ville blitt kjørt, men utfører dem ikke. Dette er nyttig for å forhåndsvise endringer uten å gjøre faktiske modifikasjoner i repositoryet.  

  
### Eksempel
  
For å oppgradere ***digna***-repositoryet kan du kjøre kommandoen uten alternativer:
  
```bash
dignacli upgrade-repo
```  
For å kjøre oppgraderingen i simulasjonsmodus (for å se SQL-setningene uten å anvende dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Denne kommandoen er viktig for å vedlikeholde ***digna***-systemet, og sikrer at databaseskjema og andre repository-komponenter er oppdatert med siste versjon av programvaren.

## Bruke `encrypt`-kommandoen
  
`encrypt`-kommandoen i ***digna*** CLI brukes for å kryptere et passord.
  
### Kommando-bruk
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenter
- **PASSWORD**: Passordet som skal krypteres (påkrevd).
  
### Eksempel
  
For å kryptere et passord må du oppgi passordet som et argument.   
For eksempel, for å kryptere passordet `mypassword123`, bruker du:
```bash
dignacli encrypt mypassword123
```
Denne kommandoen gir ut den krypterte versjonen av det oppgitte passordet, som deretter kan brukes i sikre sammenhenger. Hvis passord-argumentet ikke oppgis, vil CLI-en vise en feil som indikerer manglende argument.

## Bruke `generate-key`-kommandoen
  
`generate-key`-kommandoen brukes for å generere en Fernet-nøkkel, som er viktig for å sikre passord lagret i ***digna***-repositoryet.
  
### Kommando-bruk
```bash
dignacli generate-key
```
  
# Datahåndtering

## Bruke `clean-up`-kommandoen

`clean-up`-kommandoen i ***digna*** CLI brukes for å fjerne profiler, prediksjoner og data fra Traffic Light System for én eller flere datakilder innenfor et spesifisert prosjekt. Denne kommandoen er viktig for datalivssyklusadministrasjon, og hjelper med å opprettholde et organisert og effektivt data-miljø ved å rydde ut utdaterte eller unødvendige data.

### Kommando-bruk

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet som data skal fjernes fra (påkrevd). Å bruke nøkkelordet `all-projects` i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og tid for datarensingen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og tid for datarensingen, med samme formater som FROM_DATE (påkrevd).
  
### Alternativer
  
- `--table-name`, `-tn`: Begrens clean-up-operasjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtrerer for å begrense clean-up til tabeller som inneholder den angitte delstrengen i navnet.
- `--timing`, `-tm`: Viser tidsforbruket for clean-up-prosessen etter fullføring.
- `--help`: Viser hjelpeinformasjon for clean-up-kommandoen og avslutter.
  
### Eksempel
  
For å fjerne data fra prosjektet ProjectA mellom 1. januar 2023 og 30. juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
For å fjerne data kun fra en spesifikk tabell kalt `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Denne kommandoen hjelper til med å styre datalagring og sikre at repositoryet kun inneholder relevant informasjon.

## Bruke `inspect`-kommandoen

`inspect`-kommandoen i ***digna*** CLI brukes for å opprette profiler, prediksjoner og data for Traffic Light System for én eller flere datakilder innen et spesifisert prosjekt. Denne kommandoen hjelper med å analysere og overvåke data over en definert periode.

### Kommando-bruk

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet som data skal inspiseres for (påkrevd). Å bruke nøkkelordet `all-projects` i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og tid for data-inspeksjonen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og tid for data-inspeksjonen, med samme formater som FROM_DATE (påkrevd).
  
### Alternativer

- `--table-name`, `-tn`: Begrens inspeksjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtrer for kun å inspisere tabeller som inneholder den angitte delstrengen i navnet.
- `--do-profile`: Trigger gjeninnsamling av profiler. Standard er do-profile.
- `--no-do-profile`: Forhindrer gjeninnsamling av profiler.
- `--do-prediction`: Trigger nyberegning av prediksjoner. Standard er do-prediction.
- `--no-do-prediction`: Forhindrer nyberegning av prediksjoner.
- `--do-alert-status`: Trigger nyberegning av varslingsstatus. Standard er do-alert-status.
- `--no-do-alert-status`: Forhindrer nyberegning av varslingsstatus.
- `--iterative`: Trigger inspeksjon av en periode ved bruk av daglige iterasjoner. Standard er iterative.
- `--no-iterative`: Trigger inspeksjon av hele perioden i én omgang.
- `--timing`, `-tm`: Viser varigheten av inspeksjonsprosessen etter fullføring.
  
### Eksempel
  
For å inspisere data for prosjektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
For å inspisere kun en spesifikk tabell og tvinge nyberegning av prediksjoner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Denne kommandoen er nyttig for å generere oppdaterte profiler og prediksjoner, overvåke dataintegritet og administrere varslingssystemer innen en spesifisert prosjekt-tidsramme.

## Bruke `tls-status`-kommandoen

`tls-status`-kommandoen i ***digna*** CLI brukes for å spørre om statusen til Traffic Light System (TLS) for en spesifikk tabell innen et prosjekt på en gitt dato. Traffic Light System gir innsikt i datakvalitet og helsetilstand, og indikerer eventuelle problemer eller varsler som krever oppmerksomhet.
  
### Kommando-bruk
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet som TLS-statusen forespørres for (påkrevd).
- **TABLE_NAME**: Den spesifikke tabellen innen prosjektet som TLS-statusen gjelder for (påkrevd).
- **DATE**: Datoen som TLS-statusen forespørres for, vanligvis i formatet %Y-%m-%d (påkrevd).
  
### Eksempel
  
For å sjekke TLS-status for en tabell kalt UserData i prosjektet ProjectA den 1. juli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Denne kommandoen hjelper brukere med å overvåke og opprettholde datakvalitet ved å gi en klar og handlingsrettet statusrapport basert på forhåndsdefinerte kriterier.

## Bruke `list-projects`-kommandoen
  
`list-projects`-kommandoen i ***digna*** CLI brukes for å vise en liste over alle tilgjengelige prosjekter i ***digna***-systemet.
  
### Kommando-bruk
  
```bash
dignacli list-projects
```

Denne kommandoen er spesielt nyttig for administratorer og brukere som administrerer flere prosjekter, og gir en rask oversikt over tilgjengelige prosjekter i ***digna***-repositoryet.

## Bruke `list-ds`-kommandoen

`list-ds`-kommandoen i ***digna*** CLI brukes for å vise en liste over alle tilgjengelige datakilder innen et spesifisert prosjekt. Denne kommandoen er nyttig for å få oversikt over dataressursene som er tilgjengelige for analyse og administrasjon i ***digna***-systemet.

### Kommando-bruk
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene skal listes for (påkrevd).
  
### Eksempel
  
For å liste alle datakilder i prosjektet med navnet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Denne kommandoen gir brukerne en oversikt over datakildene som er tilgjengelige i et prosjekt, og hjelper dem å navigere og administrere datalandskapet mer effektivt.