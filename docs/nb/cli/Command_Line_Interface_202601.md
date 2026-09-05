---
title: digna CLI-referanse 2026.01 – Kommandoer og eksempler | digna-dokumentasjon
description: Fullstendig referanse for digna CLI-utgivelsen 2026.01. Lær hvordan du administrerer brukere, repositories og data med kommandoer som add-user, check-config, check-repo-connection, inspect, inspect-async med mer.
image: /assets/logo_square.png
---

# digna CLI Reference 2026.01
**2026-01-15**

Denne siden dokumenterer hele settet av kommandoer som er tilgjengelige i ***digna*** CLI-utgivelsen **2026.01**, inkludert brukseksempler og alternativer.

---

## CLI-grunnleggende

---

### help
`--help`-alternativet gir informasjon om tilgjengelige kommandoer og hvordan de brukes. Det finnes to hovedmåter å bruke dette alternativet på:

1. **Visning av generell hjelp:**
   
   Bruk --help umiddelbart etter nøkkelordet ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Hente hjelp for spesifikke kommandoer:**  
  
   For detaljert informasjon om en spesifikk kommando, legg til `--help` etter den kommandoen.
   For eksempel, for å få hjelp med `add-user`-kommandoen, kjør:
   ```bash
   dignacli add-user --help
   ```

   ### output:
      
   - **Command Description:** Gir en detaljert beskrivelse av hva kommandoen gjør.  
   - **Syntax:** Viser nøyaktig syntaks, inkludert påkrevde og valgfrie argumenter.  
   - **Options:** Lister opp eventuelle alternativer som er spesifikke for kommandoen, sammen med forklaringer.  
   - **Examples:** Gir eksempler på hvordan kommandoen kan kjøres effektivt.

### check-config

check-config-kommandoen er et verktøy i ***digna*** CLI for å teste konfigurasjonen av ***digna***. Denne kommandoen sikrer at ***digna***-komponentene finner nødvendige konfigurasjonselementer i config.toml.

#### Options

- `--configpath`, `-cp`: Fil eller katalog som inneholder konfigurasjonen. Hvis ikke spesifisert, brukes ../config.toml.
      
#### Command Usage
```bash
dignacli check-config
```

Ved vellykket gjennomføring skriver kommandoen ut en bekreftelse på at konfigurasjonen er komplett.  
  
Hvis konfigurasjonen ser ut til å være ufullstendig, vil de manglende konfigurasjonselementene bli oppført.

  
### check-repo-connection

check-repo-connection-kommandoen er et verktøy i ***digna*** CLI for å teste tilkobling og tilgang til et spesifisert ***digna*** repository. Denne kommandoen sikrer at CLI-en kan kommunisere med repositoryet.
      
#### Command Usage
```bash
dignacli check-repo-connection
```

Ved vellykket gjennomføring skriver kommandoen ut en bekreftelse på tilkoblingen, sammen med detaljer om repositoryet: Repository version, Host, Database og Schema.  
  
Hvis tilkoblingen til repositoryet ikke er vellykket, sjekk config.toml-filen for riktige konfigurasjonsinnstillinger.


### version

For å sjekke hvilken versjon av *dignacli* som er installert, bruk --version-alternativet.  
  
#### Command Usage
```bash
dignacli --version
```
  
#### Example Output
```bash
dignacli version 2026.01
```

### loggingsalternativer
  
Som standard er konsollutskriften fra ***digna***-kommandoene designet for å være minimalistisk. De fleste kommandoer tilbyr mulighet for å gi ekstra informasjon ved å bruke følgende alternativer:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” og “debug” definerer detaljnivået, mens “logfile”-bryteren lar deg omdirigere utskriften til en fil i stedet for konsollvinduet.

## Brukeradministrasjon

### add-user
  
add-user-kommandoen i ***digna*** CLI brukes til å legge til en ny bruker i ***digna***-systemet.
  
#### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Arguments

- **USER_NAME**: Brukernavnet for den nye brukeren (påkrevd).
- **USER_FULL_NAME**: Fullt navn på den nye brukeren (påkrevd).
- **USER_PASSWORD**: Passordet for den nye brukeren (påkrevd).

#### Options

- `--is_superuser`, `-su`: Flagget for å angi at den nye brukeren er administrator.
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

### delete-user
  
`delete-user`-kommandoen i ***digna*** CLI brukes til å fjerne en eksisterende bruker fra ***digna***-systemet.
  
#### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
#### Arguments
- **USER_NAME**: Brukernavnet til brukeren som skal slettes (påkrevd). Dette er det eneste argumentet som kreves av kommandoen.

#### Eksempel
```bash
dignacli delete-user jdoe
```
  
Kjøring av denne kommandoen fjerner brukeren `jdoe` fra ***digna***-systemet, tilbakekaller deres tilgang og sletter tilknyttede data og tillatelser fra repositoryet.

### modify-user

`modify-user`-kommandoen i ***digna*** CLI brukes til å oppdatere informasjonen for en eksisterende bruker i ***digna***-systemet.

#### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Arguments
  
- **USER_NAME**: Brukernavnet til brukeren som skal endres (påkrevd).
- **USER_FULL_NAME**: Det nye fulle navnet for brukeren (påkrevd).
  
#### Options  
  
- `--is_superuser`, `-su`: Angir brukeren som superbruker, og gir opphøyde rettigheter. Dette flagget krever ikke en verdi.  
- `--valid_until`, `-vu`: Setter en utløpsdato for brukerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke angitt, forblir kontoen gyldig på ubestemt tid.  
  
#### Eksempel
  
For å endre fullt navn for brukeren `jdoe` til “Johnathan Doe” og angi brukeren som superbruker:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd`-kommandoen i ***digna*** CLI brukes til å endre passordet for en eksisterende bruker i ***digna***-systemet.
  
#### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Arguments
  
- **USER_NAME**: Brukernavnet til brukeren hvis passord skal endres (påkrevd).
- **USER_PWD**: Det nye passordet for brukeren (påkrevd).
  
#### Eksempel
  
For å endre passordet for brukeren `jdoe` til `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users`-kommandoen i ***digna*** CLI viser en liste over alle brukere som er registrert i ***digna***-systemet.

#### Command Usage

```bash
dignacli list-users
```

Kjøring av denne kommandoen i ***digna*** CLI kobler til ***digna***-repositoryet og lister opp alle brukere, og viser deres ID, brukernavn, fullt navn, superbrukerstatus og utløpstidspunkter.

## Repository-administrasjon

### upgrade-repo
  
`upgrade-repo`-kommandoen i ***digna*** CLI brukes til å oppgradere eller initialisere ***digna***-repositoryet. Denne kommandoen er nødvendig for å anvende oppdateringer eller sette opp repository-infrastrukturen for første gang.
  
#### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: Når aktivert kjører dette alternativet kommandoen i simulasjonsmodus, som skriver ut SQL-setningene som ville blitt kjørt, men utfører dem ikke. Dette er nyttig for å forhåndsvise endringer uten å gjøre faktiske modifikasjoner i repositoryet.  

  
#### Eksempel
  
For å oppgradere ***digna***-repositoryet kan du kjøre kommandoen uten alternativer:
  
```bash
dignacli upgrade-repo
```  
For å kjøre oppgraderingen i simulasjonsmodus (for å se SQL-setningene uten å anvende dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Denne kommandoen er viktig for å vedlikeholde ***digna***-systemet og sørge for at databaseskjemaet og andre repository-komponenter er oppdaterte med den nyeste versjonen av programvaren.

### encrypt
  
`encrypt`-kommandoen i ***digna*** CLI brukes til å kryptere et passord.
  
#### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Arguments
- **PASSWORD**: Passordet som skal krypteres (påkrevd).
  
#### Eksempel
  
For å kryptere et passord må du oppgi passordet som et argument.   
For eksempel, for å kryptere passordet `mypassword123`, bruker du:
```bash
dignacli encrypt mypassword123
```
Denne kommandoen skriver ut den krypterte versjonen av det oppgitte passordet, som deretter kan brukes i sikre sammenhenger. Hvis passordargumentet ikke er oppgitt, vil CLI-en vise en feil som indikerer det manglende argumentet.

### generate-key
  
`generate-key`-kommandoen brukes til å generere en Fernet-nøkkel, som er nødvendig for å sikre passord lagret i ***digna***-repositoryet.
  
#### Command Usage
```bash
dignacli generate-key
```
  
## Datahåndtering

### clean-up

`clean-up`-kommandoen i ***digna*** CLI brukes til å fjerne profiler, prediksjoner og trafikklysdata for en eller flere datakilder innenfor et spesifisert prosjekt. Denne kommandoen er essensiell for livssyklusstyring av data og hjelper med å holde et organisert og effektivt dataområde ved å rydde ut utdaterte eller unødvendige data.

#### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: Navnet på prosjektet fra hvilket data skal fjernes (påkrevd). Bruk av nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og -tid for datafjerningen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datafjerningen, i samme formater som FROM_DATE (påkrevd).
  
#### Options
  
- `--table-name`, `-tn`: Begrens clean-up-operasjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtre for å begrense clean-up til tabeller som inneholder den angitte delstrengen i navnene sine.
- `--timing`, `-tm`: Viser tidsvarigheten for clean-up-prosessen etter fullføring.
- `--help`: Viser hjelpeinformasjon for clean-up-kommandoen og avslutter.
  
#### Eksempel
  
For å fjerne data fra prosjektet ProjectA mellom 1. januar 2023 og 30. juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
For å fjerne data bare fra en spesifikk tabell kalt `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Denne kommandoen hjelper med å styre datalagring og sikrer at repositoryet kun inneholder relevant informasjon.

### remove-orphans
  
`remove-orphans`-kommandoen i ***digna*** CLI brukes til vedlikehold i ***digna***-repositoryet.  
Når en bruker sletter prosjekter eller datakilder, kan profiler og prediksjoner bli liggende igjen i repositoryet. Med denne kommandoen fjernes slike foreldreløse rader fra repositoryet.
  
#### Command Usage
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects`-kommandoen i ***digna*** CLI brukes til å vise en liste over alle tilgjengelige prosjekter i ***digna***-systemet.
  
#### Command Usage
  
```bash
dignacli list-projects
```

Denne kommandoen er spesielt nyttig for administratorer og brukere som administrerer flere prosjekter, og gir en rask oversikt over tilgjengelige prosjekter i ***digna***-repositoryet.

### list-ds

`list-ds`-kommandoen i ***digna*** CLI brukes til å vise en liste over alle tilgjengelige datakilder innenfor et spesifisert prosjekt. Denne kommandoen er nyttig for å få oversikt over hvilke dataressurser som er tilgjengelige for analyse og administrasjon i ***digna***-systemet.

#### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME**: Navnet på prosjektet det listes datakilder for (påkrevd).
  
#### Eksempel
  
For å liste alle datakilder i prosjektet med navnet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Denne kommandoen gir brukerne en oversikt over datakildene som er tilgjengelige i et prosjekt, og hjelper dem å navigere og administrere datalandskapet mer effektivt.


### inspect

`inspect`-kommandoen i ***digna*** CLI brukes til å opprette profiler, prediksjoner og trafikklysdata for en eller flere datakilder innenfor et spesifisert prosjekt. Denne kommandoen hjelper med å analysere og overvåke data over en definert periode. Etter fullført inspeksjon returneres verdien av det kalkulerte trafikklyssystemet:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: Navnet på prosjektet som skal inspiseres (påkrevd). Bruk av nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og -tid for datainspeksjonen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datainspeksjonen, i samme formater som FROM_DATE (påkrevd).
  
#### Options

- `--table-name`, `-tn`: Begrens inspeksjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtrer for å inspisere kun tabeller som inneholder den angitte delstrengen i navnene sine.
- `--enable_notification`, `-en`: Aktiverer sending av varsler ved hendelser.
- `--bypass-backend`, `-bb`: Bypass backend og kjør inspeksjon direkte fra CLI (kun for testformål!).

  
#### Eksempel
  
For å inspisere data for prosjektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
For å inspisere kun en spesifikk tabell og tvinge rekalkulering av prediksjoner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Denne kommandoen er nyttig for å generere oppdaterte profiler og prediksjoner, overvåke dataintegritet og administrere varslingssystemer innenfor en angitt prosjektperiode.

### inspect-async

`inspect-async`-kommandoen i ***digna*** CLI brukes til å opprette profiler, prediksjoner og trafikklysdata for en eller flere datakilder innenfor et spesifisert prosjekt. Denne kommandoen hjelper med å analysere og overvåke data over en definert periode. I motsetning til `inspect`-kommandoen venter denne ikke på at inspeksjonen fullføres.
I stedet returnerer den request id for den innsendte inspeksjonsforespørselen. For å spørre om fremdriften i inspeksjonsprosessen, bruk kommandoen `inspect-status`.

#### Command Usage

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: Navnet på prosjektet som skal inspiseres (påkrevd). Bruk av nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og -tid for datainspeksjonen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datainspeksjonen, i samme formater som FROM_DATE (påkrevd).
  
#### Options

- `--table-name`, `-tn`: Begrens inspeksjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtrer for å inspisere kun tabeller som inneholder den angitte delstrengen i navnene sine.
- `--enable_notification`, `-en`: Aktiverer sending av varsler ved hendelser.

  
#### Eksempel
  
For å inspisere data for prosjektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status`-kommandoen i ***digna*** CLI brukes til å sjekke fremdriften til en asynkron inspeksjon basert på request ID.

#### Command Usage

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Arguments
  
- **REQUEST_ID**: Request-ID-en som returneres av `inspect-async`-kommandoen 
  
#### Eksempel
  
For å sjekke fremdriften til en inspeksjon med request ID 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel`-kommandoen i ***digna*** CLI brukes til å avbryte inspeksjoner basert på request ID eller den kan brukes til å kansellere alle gjeldende forespørsler.

#### Command Usage

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Arguments
  
- **REQUEST_ID**: Request-ID-en som returneres av `inspect-async`-kommandoen 
  
#### Eksempel
  
For å kansellere inspeksjonen med request ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

For å kansellere alle forespørsler som for øyeblikket kjører eller venter:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds`-kommandoen i ***digna*** CLI brukes til å opprette en eksport av datakilder fra ***digna***-repositoryet. Som standard vil alle datakilder fra et gitt prosjekt eksporteres.

#### Command Usage
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Arguments
- **PROJECT_NAME**: Navnet på prosjektet som datakildene skal eksporteres fra.

#### Options

- `--table_name`, `-tn`: Eksporter en bestemt datakilde fra et prosjekt.
- `--exportfile`, `-ef`: Spesifiser filnavnet for eksporten.
    
#### Eksempel
  
For å eksportere alle datakilder fra prosjektet med navnet `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Denne kommandoen eksporterer alle datakilder fra `ProjectA` som et JSON-dokument som kan importeres til et annet prosjekt eller ***digna***-repository.

### import-ds

`import-ds`-kommandoen i ***digna*** CLI brukes til å importere datakilder inn i et målprosjekt og lage en importrapport.

#### Command Usage
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: Navnet på prosjektet som datakildene skal importeres til.
- **EXPORT_FILE**: Filnavnet til eksportfilen med datakildene som skal importeres.

#### Options

- `--output-file`, `-o`: Fil for å lagre importrapporten (hvis ikke spesifisert, skrives den til terminalen i tabellform).
- `--output-format`, `-f`: Format for å lagre importrapporten (json, csv).
    
#### Eksempel
  
For å importere alle datakilder fra eksportfilen `my_export.json` inn i `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Etter importen vil denne kommandoen også vise en rapport over importerte og hoppede objekter. Bare nye datakilder vil bli importert til `ProjectB`. For å finne ut hvilke objekter som ville blitt importert og hvilke som ville blitt hoppet over, kan du bruke kommandoen `plan-import-ds`.

### plan-import-ds

`plan-import-ds`-kommandoen i ***digna*** CLI brukes til å analysere en eksport av datakilder mot et målprosjekt og lage en plan-/importrapport uten å utføre selve importen.

#### Command Usage
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: Navnet på prosjektet som datakildene ville blitt importert til.
- **EXPORT_FILE**: Filnavnet til eksportfilen med datakildene som skal analyseres før import.

#### Options

- `--output-file`, `-o`: Fil for å lagre importrapporten (hvis ikke spesifisert, skrives den til terminalen i tabellform).
- `--output-format`, `-f`: Format for å lagre importrapporten (json, csv).
    
#### Eksempel
  
For å sjekke hvilke datakilder som ville blitt importert og hvilke som ville blitt hoppet over fra eksportfilen `my_export.json` ved import til `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Denne kommandoen vil kun vise en importplan over objekter som vil bli importert og hoppet over.