---
title: digna CLI Referanse 2025.04 – Kommandoer & Eksempler | digna Dokumentasjon
description: Komplett referanse for digna CLI-utgivelsen 2025.04. Lær hvordan du administrerer brukere, repositoryer og data med kommandoer som add-user, check-repo-connection, upgrade-repo, inspect og mer.
image: /assets/logo_square.png
---

# digna CLI Referanse 2025.04
**2025-04-01**

Denne siden dokumenterer hele settet med kommandoer tilgjengelig i ***digna*** CLI-utgivelsen **2025.04**, inkludert brukseksempler og alternativer.

---

## CLI Grunnleggende

---

## Bruke `help`-alternativet

`--help`-alternativet gir informasjon om tilgjengelige kommandoer og hvordan de brukes. Det finnes to hovedmåter å bruke dette alternativet på:

1. **Visning av generell hjelp:**
   
    Bruk --help umiddelbart etter nøkkelordet ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Hjelp for spesifikke kommandoer:**  
  
    For detaljert informasjon om en spesifikk kommando, legg til `--help` etter den kommandoen.  
    For eksempel, for å få hjelp med kommandoen `add-user`, kjør:
     ```bash
     dignacli add-user --help
     ```

     ### Utdata:
      
     - **Kommando-beskrivelse:** Gir en detaljert forklaring på hva kommandoen gjør.  
     - **Syntaks:** Viser nøyaktig syntaks, inkludert påkrevde og valgfrie argumenter.  
     - **Alternativer:** Lister opp alternativer spesifikke for kommandoen, sammen med forklaringer.  
     - **Eksempler:** Gir eksempler på hvordan kommandoen kan kjøres effektivt.

  
## Bruke `check-repo-connection`-kommandoen

`check-repo-connection`-kommandoen er et verktøy i ***digna*** CLI som er designet for å teste tilkobling og tilgang til et spesifisert ***digna*** repository. Denne kommandoen sikrer at CLI kan kommunisere med repositoryet.
      
#### Kommando-bruk
```bash
dignacli check-repo-connection
```

Ved vellykket kjøring vil kommandoen vise en bekreftelse på tilkoblingen, sammen med detaljer om repositoryet: Repository-versjon, Host, Database og Schema.  
  
Hvis tilkoblingen til repositoryet mislykkes, sjekk config.toml-filen for riktige konfigurasjonsinnstillinger.

## Bruke `version`-kommandoen

For å sjekke installert versjon av *dignacli*, bruk --version-alternativet.  
  
#### Kommando-bruk
```bash
dignacli --version
```
  
#### Eksempel på utdata
```bash
dignacli version 2025.04
```

## Bruke loggingsalternativer
  
Som standard er konsollutdata fra ***digna***-kommandoer minimalisert. De fleste kommandoer tilbyr muligheten til å gi mer informasjon ved hjelp av følgende alternativer:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” og “debug” angir detaljnivået, mens “logfile”-bryteren lar deg omdirigere utdata til en fil i stedet for konsollen.

## Brukeradministrasjon

### Bruke `add-user`-kommandoen
  
`add-user`-kommandoen i ***digna*** CLI brukes til å legge til en ny bruker i ***digna***-systemet.
  
#### Kommando-bruk
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumenter

- **USER_NAME**: Brukernavnet for den nye brukeren (påkrevd).
- **USER_FULL_NAME**: Fullt navn på den nye brukeren (påkrevd).
- **USER_PASSWORD**: Passordet for den nye brukeren (påkrevd).

#### Alternativer

- `--is_superuser`, `-su`: Flag for å gjøre den nye brukeren til administrator.
- `--valid_until`, `-vu`: Setter en utløpsdato for brukerkontoen i formatet `YYYY-MM-DD HH:MI:SS`. Hvis ikke satt, har kontoen ingen utløpsdato.

#### Eksempel

For å legge til en ny bruker med brukernavn `jdoe`, fullt navn `John Doe` og passord `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
For å legge til en ny bruker og sette en utløpsdato for kontoen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Bruke `delete-user`-kommandoen
  
`delete-user`-kommandoen i ***digna*** CLI brukes til å fjerne en eksisterende bruker fra ***digna***-systemet.
  
#### Kommando-bruk
```bash
dignacli delete-user USER_NAME
```
  
##### Argumenter
- **USER_NAME**: Brukernavnet til brukeren som skal slettes (påkrevd). Dette er det eneste argumentet som kreves av kommandoen.

#### Eksempel
```bash
dignacli delete-user jdoe
```
  
Å kjøre denne kommandoen vil fjerne brukeren `jdoe` fra ***digna***-systemet, frata vedkommende tilgang og slette tilknyttede data og rettigheter fra repositoryet.

### Bruke `modify-user`-kommandoen

`modify-user`-kommandoen i ***digna*** CLI brukes til å oppdatere detaljer for en eksisterende bruker i ***digna***-systemet.

#### Kommando-bruk
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumenter
  
- **USER_NAME**: Brukernavnet til brukeren som skal endres (påkrevd).
- **USER_FULL_NAME**: Det nye fulle navnet for brukeren (påkrevd).
  
#### Alternativer  
  
- `--is_superuser`, `-su`: Setter brukeren som superuser og gir forhøyede rettigheter. Dette flagget krever ingen verdi.  
- `--valid_until`, `-vu`: Setter en utløpsdato for brukerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke gitt, forblir kontoen gyldig på ubestemt tid.  
  
#### Eksempel
  
For å endre fullt navn for brukeren `jdoe` til “Johnathan Doe” og sette brukeren som superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Bruke `modify-user-pwd`-kommandoen
  
`modify-user-pwd`-kommandoen i ***digna*** CLI brukes til å endre passordet for en eksisterende bruker i ***digna***-systemet.
  
#### Kommando-bruk
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumenter
  
- **USER_NAME**: Brukernavnet til brukeren hvis passord skal endres (påkrevd).
- **USER_PWD**: Det nye passordet for brukeren (påkrevd).
  
#### Eksempel
  
For å endre passordet for brukeren `jdoe` til `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Bruke `list-users`-kommandoen

`list-users`-kommandoen i ***digna*** CLI viser en liste over alle brukere registrert i ***digna***-systemet.

#### Kommando-bruk

```bash
dignacli list-users
```

Å kjøre denne kommandoen i ***digna*** CLI vil koble til ***digna***-repositoryet og liste opp alle brukere, vise deres ID, brukernavn, fulle navn, superuser-status og utløpstidspunkter.

## Repository-administrasjon

### Bruke `upgrade-repo`-kommandoen
  
`upgrade-repo`-kommandoen i ***digna*** CLI brukes for å oppgradere eller initialisere ***digna***-repositoryet. Denne kommandoen er essensiell for å anvende oppdateringer eller sette opp repository-infrastrukturen for første gang.
  
#### Kommando-bruk

```bash
dignacli upgrade-repo [options]
```
  
#### Alternativer
  
- `--simulation-mode`, `-s`: Når aktivert, kjører denne opsjonen kommandoen i simulasjonsmodus, som skriver ut SQL-setningene som ville blitt kjørt, men utfører dem ikke. Dette er nyttig for å forhåndsvise endringer uten å gjøre modifikasjoner i repositoryet.  

  
#### Eksempel
  
For å oppgradere ***digna***-repositoryet kan du kjøre kommandoen uten noen alternativer:
  
```bash
dignacli upgrade-repo
```  
For å kjøre oppgraderingen i simulasjonsmodus (for å se SQL-setningene uten å anvende dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Denne kommandoen er viktig for vedlikehold av ***digna***-systemet og sørger for at databaseskjemaet og andre repository-komponenter er oppdaterte med siste versjon av programvaren.

### Bruke `encrypt`-kommandoen
  
`encrypt`-kommandoen i ***digna*** CLI brukes til å kryptere et passord.
  
#### Kommando-bruk
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenter
- **PASSWORD**: Passordet som skal krypteres (påkrevd).
  
#### Eksempel
  
For å kryptere et passord må du oppgi passordet som argument.   
For eksempel, for å kryptere passordet `mypassword123`, bruker du:
```bash
dignacli encrypt mypassword123
```
Denne kommandoen returnerer den krypterte versjonen av angitt passord, som deretter kan brukes i sikre sammenhenger. Hvis passordargumentet ikke er gitt, vil CLI vise en feil som indikerer det manglende argumentet.

## Bruke `generate-key`-kommandoen
  
`generate-key`-kommandoen brukes til å generere en Fernet-nøkkel, som er nødvendig for å sikre passord lagret i ***digna***-repositoryet.
  
#### Kommando-bruk
```bash
dignacli generate-key
```
  
## Databehandling

## Bruke `clean-up`-kommandoen

`clean-up`-kommandoen i ***digna*** CLI brukes til å fjerne profiler, prediksjoner og data fra Traffic Light System for én eller flere datakilder innen et spesifisert prosjekt. Denne kommandoen er viktig for datalivssyklusforvaltning, og hjelper med å holde et organisert og effektivt data-miljø ved å rydde ut foreldet eller unødvendig data.

#### Kommando-bruk

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet hvor data skal fjernes fra (påkrevd). Bruk av nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og -tid for datarengjøring. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datarengjøring, i samme formater som FROM_DATE (påkrevd).
  
#### Alternativer
  
- `--table-name`, `-tn`: Begrens clean-up-operasjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtrerer for å begrense clean-up til tabeller som inneholder den angitte delstrengen i navnet.
- `--timing`, `-tm`: Viser tidsbruken for clean-up-prosessen etter fullføring.
- `--help`: Viser hjelpeinformasjon for clean-up-kommandoen og avslutter.
  
#### Eksempel
  
For å fjerne data fra prosjektet ProjectA mellom 1. januar 2023 og 30. juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
For å fjerne data kun fra en spesifikk tabell kalt `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Denne kommandoen hjelper med å håndtere datalagring og sørger for at repositoryet kun inneholder relevant informasjon.

## Bruke `list-projects`-kommandoen
  
`list-projects`-kommandoen i ***digna*** CLI brukes for å vise en liste over alle tilgjengelige prosjekter i ***digna***-systemet.
  
#### Kommando-bruk
  
```bash
dignacli list-projects
```

Denne kommandoen er spesielt nyttig for administratorer og brukere som administrerer flere prosjekter, og gir en rask oversikt over tilgjengelige prosjekter i ***digna***-repositoryet.

## Bruke `list-ds`-kommandoen

`list-ds`-kommandoen i ***digna*** CLI brukes til å vise en liste over alle tilgjengelige datakilder innen et spesifisert prosjekt. Denne kommandoen er nyttig for å få oversikt over dataressursene som er tilgjengelige for analyse og håndtering i ***digna***-systemet.

#### Kommando-bruk
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet datakildene listes for (påkrevd).
  
#### Eksempel
  
For å liste alle datakilder i prosjektet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Denne kommandoen gir brukerne en oversikt over datakildene tilgjengelig i et prosjekt, og hjelper dem å navigere og administrere datalandskapet mer effektivt.


## Bruke `inspect`-kommandoen

`inspect`-kommandoen i ***digna*** CLI brukes til å opprette profiler, prediksjoner og data for Traffic Light System for én eller flere datakilder innen et spesifisert prosjekt. Denne kommandoen hjelper til med å analysere og overvåke data over en definert periode.

#### Kommando-bruk

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet som skal inspiseres (påkrevd). Bruk av nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og -tid for datainspeksjonen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datainspeksjonen, i samme formater som FROM_DATE (påkrevd).
  
#### Alternativer

- `--table-name`, `-tn`: Begrens inspeksjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtrerer for å inspisere kun tabeller som inneholder den angitte delstrengen i navnet.
- `--do-profile`: Trigger recollection/reinnhenting av profiler. Standard er do-profile.
- `--no-do-profile`: Forhindrer reinnhenting av profiler.
- `--do-prediction`: Trigger rekalkulering av prediksjoner. Standard er do-prediction.
- `--no-do-prediction`: Forhindrer rekalkulering av prediksjoner.
- `--do-alert-status`: Trigger rekalkulering av alert-status. Standard er do-alert-status.
- `--no-do-alert-status`: Forhindrer rekalkulering av alert-status.
- `--iterative`: Trigger inspeksjon av en periode ved å bruke daglige iterasjoner. Standard er iterative.
- `--no-iterative`: Trigger inspeksjon av hele perioden i ett kjør.
- `--enable_notification`, `-en`: Aktiverer sending av varsler ved alerts.
- `--timing`, `-tm`: Viser varigheten av inspeksjonsprosessen etter fullføring.
  
#### Eksempel
  
For å inspisere data for prosjektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
For å inspisere kun en spesifikk tabell og tvinge rekalkulering av prediksjoner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Denne kommandoen er nyttig for å generere oppdaterte profiler og prediksjoner, overvåke dataintegritet og administrere varslingssystemer innen en spesifisert prosjekt-tidsramme.

## Bruke `tls-status`-kommandoen

`tls-status`-kommandoen i ***digna*** CLI brukes for å slå opp status for Traffic Light System (TLS) for en spesifikk tabell innen et prosjekt på en gitt dato. Traffic Light System gir innsikt i datakvalitet og tilstand, og indikerer eventuelle problemer eller varsler som kan kreve oppmerksomhet.
  
#### Kommando-bruk
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet som TLS-statusen forespørres for (påkrevd).
- **TABLE_NAME**: Den spesifikke tabellen innen prosjektet som TLS-statusen gjelder for (påkrevd).
- **DATE**: Datoen for hvilken TLS-statusen forespørres, vanligvis i formatet %Y-%m-%d (påkrevd).
  
#### Eksempel
  
For å sjekke TLS-statusen for en tabell kalt UserData i prosjektet ProjectA den 1. juli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Denne kommandoen hjelper brukere med å overvåke og vedlikeholde datakvalitet ved å gi en klar og handlingsrettet statusrapport basert på forhåndsdefinerte kriterier.

## Bruke `inspect-async`-kommandoen

`inspect-async`-kommandoen i ***digna*** CLI brukes for å instruere backend om å asynkront utføre inspeksjon for én eller flere datakilder for et gitt prosjekt. Hvis project_name er satt til all-projects, vil inspeksjonen iterere over alle tilgjengelige prosjekter og utføre inspeksjonen. Kommandoen returnerer en request id som kan brukes til å spore fremdriften av inspeksjonen.

#### Kommando-bruk

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet som skal inspiseres (påkrevd). Bruk av nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og -tid for datainspeksjonen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datainspeksjonen, i samme formater som FROM_DATE (påkrevd).
  
#### Alternativer

- `--table-name`, `-tn`: Begrens inspeksjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtrerer for å inspisere kun tabeller som inneholder den angitte delstrengen i navnet.

  
#### Eksempel
  
For å asynkront inspisere data for prosjektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Bruke `inspect-status`-kommandoen

`inspect-status`-kommandoen i ***digna*** CLI brukes for å sjekke fremdriften til en asynkron inspeksjon basert på request ID.

#### Kommando-bruk

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumenter
  
- **REQUEST_ID**: Request id returnert av `inspect-async`-kommandoen 
  
#### Alternativer

- `--report_level`, `-rl`: Sett rapportnivå: 'task' eller 'step' [default: task]
  
#### Eksempel
  
For å sjekke fremdriften av en inspeksjon med request ID 12345 på detaljert stegnivå:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Bruke `export-ds`-kommandoen

`export-ds`-kommandoen i ***digna*** CLI brukes for å lage en eksport av datakilder fra ***digna***-repositoryet. Som standard vil alle datakilder fra et gitt prosjekt bli eksportert.

#### Kommando-bruk
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene skal eksporteres fra.

#### Alternativer

- `--table_name`, `-tn`: Eksporter en bestemt datakilde fra et prosjekt.
- `--exportfile`, `-ef`: Angi filnavn for eksporten.
    
#### Eksempel
  
For å eksportere alle datakilder fra prosjektet `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Denne kommandoen eksporterer alle datakilder fra `ProjectA` som et JSON-dokument som kan importeres til et annet prosjekt eller ***digna***-repository.

## Bruke `import-ds`-kommandoen

`import-ds`-kommandoen i ***digna*** CLI brukes for å importere datakilder til et målprosjekt og lage en importrapport.

#### Kommando-bruk
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene skal importeres til.
- **EXPORT_FILE**: Filnavnet for eksportfilen som skal importeres.

#### Alternativer

- `--output-file`, `-o`: Fil for å lagre importrapporten (hvis ikke angitt, skrives den ut i terminalen i tabellform).
- `--output-format`, `-f`: Format for å lagre importrapporten (json, csv).
    
#### Eksempel
  
For å importere alle datakilder fra eksportfilen `my_export.json` inn i `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Etter importen vil denne kommandoen også vise en rapport over importerte og hoppede objekter. Kun nye datakilder vil bli importert til `ProjectB`. For å finne ut hvilke objekter som ville bli importert og hoppet over, kan du bruke kommandoen `plan-import-ds`.

## Bruke `plan-import-ds`-kommandoen

`plan-import-ds`-kommandoen i ***digna*** CLI brukes for å analysere en eksportfil og vise en plan for hvilke datakilder som ville bli importert til et målprosjekt.

#### Kommando-bruk
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene ville blitt importert til.
- **EXPORT_FILE**: Filnavnet for eksporten som skal analyseres før import.

#### Alternativer

- `--output-file`, `-o`: Fil for å lagre importrapporten (hvis ikke angitt, skrives den ut i terminalen i tabellform).
- `--output-format`, `-f`: Format for å lagre importrapporten (json, csv).
    
#### Eksempel
  
For å sjekke hvilke datakilder som ville blitt importert og hvilke som ville blitt hoppet over fra eksportfilen `my_export.json` når den importeres til `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Denne kommandoen vil kun vise en importplan for objekter som vil bli importert og hoppet over.