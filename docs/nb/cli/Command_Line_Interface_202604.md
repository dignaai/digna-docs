---
title: digna CLI Reference 2026.04 – Kommandoer og eksempler | digna-dokumentasjon
description: Komplett referanse for digna CLI-utgave 2026.04
image: /assets/logo_square.png
---

# digna CLI Reference 2026.04
**2026-04-08**

Denne siden dokumenterer hele settet av kommandoer som er tilgjengelige i ***digna*** CLI-utgave **2026.04**, inkludert bruks-eksempler og valg.

---

## CLI Basics

---

### help
Valg‑flagget `--help` gir informasjon om tilgjengelige kommandoer og hvordan de brukes. Det finnes to hovedmåter å bruke dette flagget på:

1. **Visning av generell hjelp:**
   
    Bruk --help umiddelbart etter nøkkelordet ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Hjelp for spesifikke kommandoer:**  
  
    For detaljert informasjon om en bestemt kommando, legg til `--help` etter den kommandoen.
    For eksempel, for å få hjelp til kommandoen `add-user`, kjør:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Kommandobeskrivelse:** Gir en detaljert beskrivelse av hva kommandoen gjør.  
     - **Syntaks:** Viser nøyaktig syntaks, inkludert nødvendige og valgfrie argumenter.  
     - **Valg:** Lister opp eventuelle valg som er spesifikke for kommandoen, sammen med forklaringer.  
     - **Eksempler:** Gir eksempler på hvordan kommandoen kan kjøres effektivt.

### check-config

kommandoen check-config er et verktøy i ***digna*** CLI som er utformet for å teste konfigurasjonen til ***digna***. Denne kommandoen sikrer at ***digna***-komponentene kan finne nødvendige konfigurasjonselementer i config.toml.

#### Valg

- `--configpath`, `-cp`: Fil eller mappe som inneholder konfigurasjonen. Hvis dette utelates, brukes ../config.toml.
      
#### Kommandoeksempel
```bash
dignacli check-config
```

Ved vellykket utførelse skriver kommandoen ut en bekreftelse på at konfigurasjonen er komplett.  
  
Hvis konfigurasjonen ser ut til å være ufullstendig, vil manglende konfigurasjonselementer bli listet opp.

  
### check-repo-connection

kommandoen check-repo-connection er et verktøy i ***digna*** CLI som er designet for å teste tilkobling og tilgang til et spesifisert ***digna***-repository. Denne kommandoen sikrer at CLI kan kommunisere med repositoryet.
      
#### Kommandoeksempel
```bash
dignacli check-repo-connection
```

Ved vellykket utførelse skriver kommandoen ut en bekreftelse på forbindelsen, sammen med detaljer om repositoryet: Repository-versjon, Host, Database og Schema.  
  
Hvis tilkoblingen til repositoryet ikke lykkes, sjekk config.toml-filen for riktige konfigurasjonsinnstillinger.


### version

For å sjekke installert versjon av *dignacli*, bruk --version-valget.  
  
#### Kommandoeksempel
```bash
dignacli --version
```
  
#### Eksempelutdata
```bash
dignacli version 2026.04
```

### logging options
  
Som standard er konsollutdataene fra ***digna***-kommandoene designet for å være minimalistiske. De fleste kommandoene tilbyr mulighet for å vise tillegginformasjon ved å bruke følgende valg:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
 «verbose» og «debug» definerer detaljnivået, mens «logfile»-bryteren tillater at utdataene omdirigeres til en fil i stedet for konsollvinduet.

## User Management

### add-user
  
Kommandoen add-user i ***digna*** CLI brukes for å legge til en ny bruker i ***digna***-systemet
  
#### Kommandoeksempel
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenter

- **USER_NAME**: Brukernavnet for den nye brukeren (påkrevd).
- **USER_FULL_NAME**: Fullt navn for den nye brukeren (påkrevd).
- **USER_PASSWORD**: Passordet for den nye brukeren (påkrevd).

#### Valg

- `--is_superuser`, `-su`: Flag for å gi den nye brukeren administratorrettigheter.
- `--valid_until`, `-vu`: Setter en utløpsdato for brukerkontoen i formatet `YYYY-MM-DD HH:MI:SS`. Hvis ikke satt, har kontoen ingen utløpsdato.

#### Eksempel

For å legge til en ny bruker med brukernavn `jdoe`, fullt navn `John Doe`, og passord `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
For å legge til en ny bruker og sette en utløpsdato for kontoen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Kommandoen `delete-user` i ***digna*** CLI brukes for å fjerne en eksisterende bruker fra ***digna***-systemet.
  
#### Kommandoeksempel
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenter
- **USER_NAME**: Brukernavnet til brukeren som skal slettes (påkrevd). Dette er det eneste argumentet som kreves av kommandoen.

#### Eksempel
```bash
dignacli delete-user jdoe
```
  
Ved kjøring av denne kommandoen fjernes brukeren `jdoe` fra ***digna***-systemet, og deres tilgang samt tilknyttede data og rettigheter i repositoryet blir slettet.

### modify-user

Kommandoen `modify-user` i ***digna*** CLI brukes for å oppdatere opplysninger for en eksisterende bruker i ***digna***-systemet.

#### Kommandoeksempel
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenter
  
- **USER_NAME**: Brukernavnet til brukeren som skal endres (påkrevd).
- **USER_FULL_NAME**: Det nye fulle navnet for brukeren (påkrevd).
  
#### Valg  
  
- `--is_superuser`, `-su`: Setter brukeren som superbruker, og gir forhøyede privilegier. Dette flagget krever ingen verdi.  
- `--valid_until`, `-vu`: Setter en utløpsdato for brukerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke oppgitt, forblir kontoen gyldig på ubestemt tid.  
  
#### Eksempel
  
For å endre fullt navn for brukeren `jdoe` til “Johnathan Doe” og sette brukeren som superbruker:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Kommandoen `modify-user-pwd` i ***digna*** CLI brukes for å endre passordet for en eksisterende bruker i ***digna***-systemet.
  
#### Kommandoeksempel
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenter
  
- **USER_NAME**: Brukernavnet til brukeren hvis passord skal endres (påkrevd).
- **USER_PWD**: Det nye passordet for brukeren (påkrevd).
  
#### Eksempel
  
For å endre passordet for brukeren `jdoe` til `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Kommandoen `list-users` i ***digna*** CLI viser en liste over alle brukere registrert i ***digna***-systemet.

#### Kommandoeksempel

```bash
dignacli list-users
```

Ved kjøring av denne kommandoen kobler ***digna*** CLI seg til ***digna***-repositoryet og viser alle brukere med ID, brukernavn, fullt navn, superbrukerstatus og utløpstidspunkter.

## Repository Management

### upgrade-repo
  
Kommandoen `upgrade-repo` i ***digna*** CLI brukes for å oppgradere eller initialisere ***digna***-repositoryet. Denne kommandoen er viktig for å anvende oppdateringer eller sette opp repository-infrastrukturen for første gang.
  
#### Kommandoeksempel

```bash
dignacli upgrade-repo [options]
```
  
#### Valg
  
- `--simulation-mode`, `-s`: Når dette er aktivert, kjører kommandoen i simuleringsmodus, som skriver ut SQL-setningene som ville blitt kjørt, men utfører dem ikke. Dette er nyttig for å forhåndsvise endringer uten å gjøre faktiske modifikasjoner i repositoryet.  

  
#### Eksempel
  
For å oppgradere ***digna***-repositoryet kan du kjøre kommandoen uten noen valg:
  
```bash
dignacli upgrade-repo
```  
For å kjøre oppgraderingen i simuleringsmodus (for å se SQL-setningene uten å anvende dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Denne kommandoen er essensiell for å vedlikeholde ***digna***-systemet og sørge for at databaseskjema og andre repository-komponenter er oppdatert med siste versjon av programvaren.

### encrypt
  
Kommandoen `encrypt` i ***digna*** CLI brukes for å kryptere et passord.
  
#### Kommandoeksempel
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenter
- **PASSWORD**: Passordet som skal krypteres (påkrevd).
  
#### Eksempel
  
For å kryptere et passord må du oppgi passordet som et argument.   
For eksempel, for å kryptere passordet `mypassword123`, vil du bruke:
```bash
dignacli encrypt mypassword123
```
Denne kommandoen skriver ut den krypterte versjonen av det oppgitte passordet, som deretter kan brukes i sikre sammenhenger. Hvis passord-argumentet ikke oppgis, vil CLI vise en feil som angir det manglende argumentet.

### generate-key
  
Kommandoen `generate-key` brukes for å generere en Fernet-nøkkel, som er nødvendig for å sikre passord lagret i ***digna***-repositoryet.
  
#### Kommandoeksempel
```bash
dignacli generate-key
```
  
## Data Management

### clean-up

Kommandoen `clean-up` i ***digna*** CLI brukes for å fjerne profiler, prediksjoner og data fra trafikklyssystemet for én eller flere datakilder innen et angitt prosjekt. Denne kommandoen er viktig for livssyklusadministrasjon av data, og hjelper med å holde et organisert og effektivt datamiljø ved å tømme utdaterte eller unødvendige data.

#### Kommandoeksempel

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet fra hvilket data skal fjernes (påkrevd). Å bruke nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og klokkeslett for datarensingen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og klokkeslett for datarensingen, med samme formater som FROM_DATE (påkrevd).
  
#### Valg
  
- `--table-name`, `-tn`: Begrens clean-up-operasjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtre for å begrense clean-up til tabeller som inneholder den angitte delstreng i navnet.
- `--timing`, `-tm`: Viser tidsbruk for clean-up-prosessen etter at den er fullført.
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
  
Denne kommandoen hjelper med å administrere datalagring og sikre at repositoryet kun inneholder relevant informasjon.

### remove-orphans
  
Kommandoen `remove-orphans` i ***digna*** CLI brukes for opprydding i ***digna***-repositoryet.  
Når en bruker sletter prosjekter eller datakilder, kan profiler og prediksjoner bli liggende igjen i repositoryet. Med denne kommandoen vil slike foreldreløse rader bli fjernet fra repositoryet.
  
#### Kommandoeksempel
  
```bash
dignacli list-projects
```

### list-projects
  
Kommandoen `list-projects` i ***digna*** CLI brukes for å vise en liste over alle tilgjengelige prosjekter i ***digna***-systemet.
  
#### Kommandoeksempel
  
```bash
dignacli list-projects
```

Denne kommandoen er spesielt nyttig for administratorer og brukere som håndterer flere prosjekter, og gir en rask oversikt over tilgjengelige prosjekter i ***digna***-repositoryet.

### list-ds

Kommandoen `list-ds` i ***digna*** CLI brukes for å vise en liste over alle tilgjengelige datakilder innen et spesifisert prosjekt. Denne kommandoen er nyttig for å få oversikt over dataressursene som er tilgjengelige for analyse og administrasjon i ***digna***-systemet.

#### Kommandoeksempel
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene listes for (påkrevd).
  
#### Eksempel
  
For å liste alle datakilder i prosjektet med navn `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Denne kommandoen gir brukerne en oversikt over datakildene som er tilgjengelige i et prosjekt, og hjelper dem å navigere og administrere datalandskapet mer effektivt.


### inspect

Kommandoen `inspect` i ***digna*** CLI brukes for å opprette profiler, prediksjoner og data for trafikklyssystemet for én eller flere datakilder innen et angitt prosjekt. Denne kommandoen hjelper med å analysere og overvåke data over en definert periode. Etter fullført inspeksjon returneres verdien for det beregnede trafikklyssystemet:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Kommandoeksempel

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet som skal inspiseres (påkrevd). Å bruke nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og klokkeslett for inspeksjonen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og klokkeslett for inspeksjonen, med samme formater som FROM_DATE (påkrevd).
  
#### Valg

- `--table-name`, `-tn`: Begrenser inspeksjonen til en spesifikk tabell i prosjektet.
- `--table-filter`, `-tf`: Filtrerer slik at kun tabeller som inneholder den spesifiserte delstrengen i navnet blir inspisert.
- `--enable_notification`, `-en`: Aktiverer sending av varsler ved alarmer.
- `--bypass-backend`, `-bb`: Hopp over backend og kjør inspeksjon direkte fra CLI (kun for testing!).

  
#### Eksempel
  
For å inspisere data for prosjektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
For å inspisere kun en bestemt tabell og tvinge nyberegning av prediksjoner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Denne kommandoen er nyttig for å generere oppdaterte profiler og prediksjoner, overvåke dataintegritet og administrere alarmsystemer innenfor et angitt prosjektintervall.

### inspect-async

Kommandoen `inspect-async` i ***digna*** CLI brukes for å opprette profiler, prediksjoner og data for trafikklyssystemet for én eller flere datakilder innen et angitt prosjekt. Denne kommandoen hjelper med å analysere og overvåke data over en definert periode. I motsetning til kommandoen `inspect` venter denne ikke på at inspeksjonen skal fullføres. I stedet returnerer den request-id for den sendte inspeksjonsforespørselen. For å spørre om fremdriften i inspeksjonsprosessen, bruk kommandoen `inspect-status`.

#### Kommandoeksempel

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet som skal inspiseres (påkrevd). Å bruke nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og klokkeslett for inspeksjonen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og klokkeslett for inspeksjonen, med samme formater som FROM_DATE (påkrevd).
  
#### Valg

- `--table-name`, `-tn`: Begrenser inspeksjonen til en spesifikk tabell i prosjektet.
- `--table-filter`, `-tf`: Filtrerer slik at kun tabeller som inneholder den spesifiserte delstrengen i navnet blir inspisert.
- `--enable_notification`, `-en`: Aktiverer sending av varsler ved alarmer.

  
#### Eksempel
  
For å inspisere data for prosjektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Kommandoen `inspect-status` i ***digna*** CLI brukes for å sjekke fremdriften for en asynkron inspeksjon basert på request-id.

#### Kommandoeksempel

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenter
  
- **REQUEST_ID**: Request-id som ble returnert av `inspect-async`-kommandoen 
  
#### Eksempel
  
For å sjekke fremdriften for en inspeksjon med request-id 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Kommandoen `inspect-cancel` i ***digna*** CLI brukes for å avbryte inspeksjoner basert på request-id, eller den kan brukes for å avbryte alle pågående forespørsler.

#### Kommandoeksempel

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenter
  
- **REQUEST_ID**: Request-id som ble returnert av `inspect-async`-kommandoen 
  
#### Eksempel
  
For å avbryte inspeksjonen med request-id 12345:
  
```bash
dignacli inspect-cancel 12345
```

For å avbryte alle forespørsler som for øyeblikket kjører eller venter:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Kommandoen `export-ds` i ***digna*** CLI brukes for å lage en eksport av datakilder fra ***digna***-repositoryet. Som standard vil alle datakilder fra et gitt prosjekt eksporteres.

#### Kommandoeksempel
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene skal eksporteres fra.

#### Valg

- `--table_name`, `-tn`: Eksporter en bestemt datakilde fra et prosjekt.
- `--exportfile`, `-ef`: Angi filnavnet for eksporten.
    
#### Eksempel
  
For å eksportere alle datakilder fra prosjektet kalt `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Denne kommandoen eksporterer alle datakilder fra `ProjectA` som et JSON-dokument som kan importeres til et annet prosjekt eller ***digna***-repository.


### import-ds

Kommandoen `import-ds` i ***digna*** CLI brukes for å importere datakilder til et målsprosjekt og lage en importrapport.

#### Kommandoeksempel
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene skal importeres til.
- **EXPORT_FILE**: Filnavnet på datakilde-eksporten som skal importeres.

#### Valg

- `--output-file`, `-o`: Fil for å lagre importrapporten (hvis ikke angitt, skrives den til terminalen i tabellform).
- `--output-format`, `-f`: Format for å lagre importrapporten (json, csv).
    
#### Eksempel
  
For å importere alle datakilder fra eksportfilen `my_export.json` inn i `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Etter importen vil denne kommandoen også vise en rapport over importerte og hoppede objekter. Kun nye datakilder vil bli importert til `ProjectB`. For å finne ut hvilke objekter som ville blitt importert og hoppet over, kan du bruke kommandoen `plan-import-ds`

### plan-import-ds

Kommandoen `plan-import-ds` i ***digna*** CLI brukes for å planlegge import av datakilder til et målsprosjekt og lage en importrapport uten å utføre selve importen.

#### Kommandoeksempel
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene ville blitt importert til.
- **EXPORT_FILE**: Filnavnet på datakilde-eksporten som skal analyseres før import.

#### Valg

- `--output-file`, `-o`: Fil for å lagre importrapporten (hvis ikke angitt, skrives den til terminalen i tabellform).
- `--output-format`, `-f`: Format for å lagre importrapporten (json, csv).
    
#### Eksempel
  
For å sjekke hvilke datakilder som ville blitt importert og hvilke som ville blitt hoppet over fra eksportfilen `my_export.json` når den importeres til `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Denne kommandoen viser kun en importplan over objekter som vil bli importert og hoppet over.