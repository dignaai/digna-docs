---
title: digna CLI Referanse 2025.09 – Kommandoer & Eksempler | digna Dokumentasjon
description: Fullstendig referanse for digna CLI-utgivelse 2025.09. Lær hvordan du administrerer brukere, repositories og data med kommandoer som add-user, check-config, check-repo-connection, inspect, inspect-async og mer.
image: /assets/logo_square.png
---

# digna CLI Referanse 2025.09
**2025-09-29**

Denne siden dokumenterer det komplette settet med kommandoer som er tilgjengelige i ***digna*** CLI-utgivelsen **2025.09**, inkludert brukseksempler og alternativer.

---

## CLI-grunnleggende

---

### help
`--help`-alternativet gir informasjon om tilgjengelige kommandoer og hvordan de brukes. Det finnes to hovedmåter å bruke dette alternativet på:

1. **Vis generell hjelp:**
   
    Bruk --help umiddelbart etter nøkkelordet ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Hente hjelp for spesifikke kommandoer:**  
  
    For detaljert informasjon om en bestemt kommando, legg til `--help` etter den kommandoen.  
    For eksempel, for å få hjelp med kommandoen `add-user`, kjør:
     ```bash
     dignacli add-user --help
     ```

     ### Utdata:
      
     - **Kommandoforklaring:** Gir en detaljert beskrivelse av hva kommandoen gjør.  
     - **Syntaks:** Viser nøyaktig syntaks, inkludert påkrevde og valgfrie argumenter.  
     - **Alternativer:** Lister opp eventuelle alternativer som er spesifikke for kommandoen, sammen med forklaringer.  
     - **Eksempler:** Gir eksempler på hvordan kommandoen kan kjøres effektivt.

### check-config

check-config-kommandoen er et verktøy i ***digna*** CLI som er designet for å teste konfigurasjonen til ***digna***. Denne kommandoen sørger for at ***digna***-komponentene kan finne nødvendige konfigurasjonselementer i config.toml.

#### Alternativer

- `--configpath`, `-cp`: Fil eller katalog som inneholder konfigurasjonen. Hvis det utelates, vil ../config.toml bli brukt.
      
#### Kommandoeksempel
```bash
dignacli check-config
```

Ved vellykket kjøring gir kommandoen en bekreftelse på at konfigurasjonen er komplett.  
  
Hvis konfigurasjonen ser ut til å være ufullstendig, vil de manglende konfigurasjonselementene bli listet opp.

  
### check-repo-connection

check-repo-connection-kommandoen er et verktøy i ***digna*** CLI som er designet for å teste tilkobling og tilgang til et spesifisert ***digna*** repository. Denne kommandoen sikrer at CLI-en kan kommunisere med repositoryet.
      
#### Kommandoeksempel
```bash
dignacli check-repo-connection
```

Ved vellykket kjøring skriver kommandoen ut en bekreftelse på tilkoblingen, sammen med detaljer om repositoryet: Repository-versjon, Host, Database og Schema.  
  
Hvis repository-tilkoblingen ikke lykkes, sjekk config.toml-filen for korrekte konfigurasjonsinnstillinger.


### version

For å sjekke installert versjon av *dignacli*, bruk --version-alternativet.  
  
#### Kommandoeksempel
```bash
dignacli --version
```
  
#### Eksempelutdata
```bash
dignacli version 2025.09
```

### loggealternativer
  
Som standard er konsollutdata fra ***digna***-kommandoene designet for å være minimalistik. De fleste kommandoer tilbyr muligheten for å gi tilleggsinformasjon ved hjelp av følgende alternativer:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” og “debug” definerer detaljnivået, mens “logfile”-bryteren lar deg omdirigere utdataene slik at de strømmes til en fil i stedet for konsollvinduet.

## Brukeradministrasjon

### add-user
  
add-user-kommandoen i ***digna*** CLI brukes for å legge til en ny bruker i ***digna***-systemet.
  
#### Kommandoeksempel
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenter

- **USER_NAME**: Brukernavnet for den nye brukeren (påkrevd).
- **USER_FULL_NAME**: Fullt navn på den nye brukeren (påkrevd).
- **USER_PASSWORD**: Passordet for den nye brukeren (påkrevd).

#### Alternativer

- `--is_superuser`, `-su`: Flag for å angi den nye brukeren som administrator.
- `--valid_until`, `-vu`: Setter en utløpsdato for brukerkontoen i formatet `YYYY-MM-DD HH:MI:SS`. Hvis ikke satt, vil kontoen ikke ha en utløpsdato.

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
  
`delete-user`-kommandoen i ***digna*** CLI brukes for å fjerne en eksisterende bruker fra ***digna***-systemet.
  
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
  
Å kjøre denne kommandoen vil fjerne brukeren `jdoe` fra ***digna***-systemet, tilbakekalle deres tilgang og slette tilknyttede data og tillatelser fra repositoryet.

### modify-user

`modify-user`-kommandoen i ***digna*** CLI brukes for å oppdatere detaljene til en eksisterende bruker i ***digna***-systemet.

#### Kommandoeksempel
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenter
  
- **USER_NAME**: Brukernavnet til brukeren som skal endres (påkrevd).
- **USER_FULL_NAME**: Det nye fulle navnet for brukeren (påkrevd).
  
#### Alternativer  
  
- `--is_superuser`, `-su`: Angir brukeren som superbruker og gir forhøyede rettigheter. Dette flagget krever ikke en verdi.  
- `--valid_until`, `-vu`: Setter en utløpsdato for brukerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke oppgitt, forblir kontoen gyldig på ubestemt tid.  
  
#### Eksempel
  
For å endre fullt navn for brukeren `jdoe` til “Johnathan Doe” og angi brukeren som superbruker:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd`-kommandoen i ***digna*** CLI brukes for å endre passordet for en eksisterende bruker i ***digna***-systemet.
  
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

`list-users`-kommandoen i ***digna*** CLI viser en liste over alle brukere som er registrert i ***digna***-systemet.

#### Kommandoeksempel

```bash
dignacli list-users
```

Å kjøre denne kommandoen i ***digna*** CLI vil koble til ***digna***-repositoryet og liste alle brukere, og vise deres ID, brukernavn, fullt navn, superbrukerstatus og utløpstidspunkter.

## Repository-administrasjon

### upgrade-repo
  
`upgrade-repo`-kommandoen i ***digna*** CLI brukes for å oppgradere eller initialisere ***digna***-repositoryet. Denne kommandoen er essensiell for å anvende oppdateringer eller sette opp repository-infrastrukturen for første gang.
  
#### Kommandoeksempel

```bash
dignacli upgrade-repo [options]
```
  
#### Alternativer
  
- `--simulation-mode`, `-s`: Når aktivert, kjører dette alternativet kommandoen i simulasjonsmodus, som skriver ut SQL-setningene som ville blitt kjørt, men som ikke faktisk utfører dem. Dette er nyttig for å forhåndsvise endringer uten å gjøre modifikasjoner i repositoryet.  

  
#### Eksempel
  
For å oppgradere ***digna***-repositoryet kan du kjøre kommandoen uten alternativer:
  
```bash
dignacli upgrade-repo
```  
For å kjøre oppgraderingen i simulasjonsmodus (for å se SQL-setningene uten å anvende dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Denne kommandoen er viktig for å vedlikeholde ***digna***-systemet og sørge for at databaseskjema og andre repository-komponenter er oppdatert i forhold til siste versjon av programvaren.

### encrypt
  
`encrypt`-kommandoen i ***digna*** CLI brukes for å kryptere et passord.
  
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
Denne kommandoen gir ut den krypterte versjonen av det oppgitte passordet, som deretter kan brukes i sikre sammenhenger. Hvis passordargumentet ikke er oppgitt, vil CLI-en vise en feil som indikerer manglende argument.

### generate-key
  
`generate-key`-kommandoen brukes for å generere en Fernet-nøkkel, som er essensiell for å sikre passord som lagres i ***digna***-repositoryet.
  
#### Kommandoeksempel
```bash
dignacli generate-key
```
  
## Datahåndtering

### clean-up

`clean-up`-kommandoen i ***digna*** CLI brukes for å fjerne profiler, prediksjoner og data fra trafikklyssystemet for én eller flere datakilder innenfor et spesifisert prosjekt. Denne kommandoen er viktig for styring av datalivssyklus, og hjelper med å opprettholde et organisert og effektivt dataomfang ved å rydde ut foreldede eller unødvendige data.

#### Kommandoeksempel

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet hvor data skal fjernes fra (påkrevd). Å bruke nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende kommandoen.
- **FROM_DATE**: Startdato og -tid for datarengjøringen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datarengjøringen, med samme formater som FROM_DATE (påkrevd).
  
#### Alternativer
  
- `--table-name`, `-tn`: Begrens clean-up-operasjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtrerer for å begrense clean-up til tabeller som inneholder den angitte understrengen i navnene sine.
- `--timing`, `-tm`: Viser tidsforbruket for clean-up-prosessen etter fullført kjøring.
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
  
Denne kommandoen hjelper til med å styre datalagring og sikrer at repositoryet kun inneholder relevant informasjon.

### remove-orphans
  
`remove-orphans`-kommandoen i ***digna*** CLI brukes for vedlikehold i ***digna***-repositoryet.  
Når en bruker sletter prosjekter eller datakilder, blir profiler og prediksjoner stående igjen i repositoryet. Med denne kommandoen vil slike foreldreløse rader bli fjernet fra repositoryet.
  
#### Kommandoeksempel
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects`-kommandoen i ***digna*** CLI brukes for å vise en liste over alle tilgjengelige prosjekter i ***digna***-systemet.
  
#### Kommandoeksempel
  
```bash
dignacli list-projects
```

Denne kommandoen er spesielt nyttig for administratorer og brukere som administrerer flere prosjekter, og gir en rask oversikt over prosjektene som finnes i ***digna***-repositoryet.

### list-ds

`list-ds`-kommandoen i ***digna*** CLI brukes for å vise en liste over alle tilgjengelige datakilder innen et spesifisert prosjekt. Denne kommandoen er nyttig for å forstå hvilke dataressurser som er tilgjengelige for analyse og administrasjon i ***digna***-systemet.

#### Kommandoeksempel
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene listes for (påkrevd).
  
#### Eksempel
  
For å liste alle datakilder i prosjektet med navnet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Denne kommandoen gir brukerne en oversikt over datakildene som er tilgjengelige i et prosjekt, og hjelper dem med å navigere og administrere datalandskapet mer effektivt.


### inspect

`inspect`-kommandoen i ***digna*** CLI brukes for å opprette profiler, prediksjoner og data til trafikklyssystemet for én eller flere datakilder innen et spesifisert prosjekt. Denne kommandoen hjelper med å analysere og overvåke data over en definert periode. Etter ferdigstilt inspeksjon returneres verdien for det beregnede trafikklyssystemet:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Kommandoeksempel

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet som data skal inspiseres for (påkrevd). Å bruke nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende kommandoen.
- **FROM_DATE**: Startdato og -tid for datainspeksjonen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datainspeksjonen, med samme formater som FROM_DATE (påkrevd).
  
#### Alternativer

- `--table-name`, `-tn`: Begrens inspeksjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtrerer for å inspisere kun tabeller som inneholder den angitte understrengen i navnene sine.
- `--enable_notification`, `-en`: Aktiverer utsending av varsler ved hendelser.
- `--bypass-backend`, `-bb`: Omgå backend og kjør inspeksjonen direkte fra CLI (kun for testformål!).

  
#### Eksempel
  
For å inspisere data for prosjektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
For å kun inspisere en spesifikk tabell og tvinge nyberegning av prediksjoner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Denne kommandoen er nyttig for å generere oppdaterte profiler og prediksjoner, overvåke dataintegritet og administrere varslingssystemer innenfor et spesifisert prosjektintervall.

### inspect-async

`inspect-async`-kommandoen i ***digna*** CLI brukes for å opprette profiler, prediksjoner og trafikklyssystemdata for én eller flere datakilder innen et spesifisert prosjekt. Denne kommandoen hjelper med å analysere og overvåke data over en definert periode. I motsetning til `inspect` venter ikke denne kommandoen på at inspeksjonen skal fullføres.
I stedet returnerer den request-id for den innsatte inspeksjonsforespørselen. For å spørre om fremdriften i inspeksjonsprosessen, bruk kommandoen `inspect-status`.

#### Kommandoeksempel

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på prosjektet som data skal inspiseres for (påkrevd). Å bruke nøkkelordet all-projects i dette argumentet instruerer ***digna*** om å iterere over alle eksisterende prosjekter og anvende kommandoen.
- **FROM_DATE**: Startdato og -tid for datainspeksjonen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datainspeksjonen, med samme formater som FROM_DATE (påkrevd).
  
#### Alternativer

- `--table-name`, `-tn`: Begrens inspeksjonen til en spesifikk tabell innen prosjektet.
- `--table-filter`, `-tf`: Filtrerer for å inspisere kun tabeller som inneholder den angitte understrengen i navnene sine.
- `--enable_notification`, `-en`: Aktiverer utsending av varsler ved hendelser.

  
#### Eksempel
  
For å kjøre en asynkron inspeksjon av data for prosjektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status`-kommandoen i ***digna*** CLI brukes for å sjekke fremdriften for en asynkron inspeksjon basert på request-id.

#### Kommandoeksempel

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenter
  
- **REQUEST_ID**: Request-id returnert av `inspect-async`-kommandoen 
  
#### Eksempel
  
For å sjekke fremdriften til en inspeksjon med request-id 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel`-kommandoen i ***digna*** CLI brukes for å avbryte inspeksjoner basert på request-id, eller den kan brukes for å avbryte alle nåværende forespørsler.

#### Kommandoeksempel

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenter
  
- **REQUEST_ID**: Request-id returnert av `inspect-async`-kommandoen 
  
#### Eksempel
  
For å avbryte inspeksjonen med request-id 12345:
  
```bash
dignacli inspect-cancel 12345
```

For å avbryte alle forespørsler som for øyeblikket kjører eller er i kø:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds`-kommandoen i ***digna*** CLI brukes for å lage en eksport av datakilder fra ***digna***-repositoryet. Som standard blir alle datakilder fra et gitt prosjekt eksportert.

#### Kommandoeksempel
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene skal eksporteres fra.

#### Alternativer

- `--table_name`, `-tn`: Eksporter en bestemt datakilde fra et prosjekt.
- `--exportfile`, `-ef`: Spesifiser filnavn for eksporten.
    
#### Eksempel
  
For å eksportere alle datakilder fra prosjektet `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Denne kommandoen eksporterer alle datakilder fra `ProjectA` som et JSON-dokument som kan importeres til et annet prosjekt eller ***digna***-repository.

### import-ds

`import-ds`-kommandoen i ***digna*** CLI brukes for å importere datakilder inn i et målprosjekt og lage en importerklæring.

#### Kommandoeksempel
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene skal importeres til.
- **EXPORT_FILE**: Filnavnet til eksporten av datakildene som skal importeres.

#### Alternativer

- `--output-file`, `-o`: Fil for å lagre importrapporten (hvis ikke spesifisert, skrives den til terminalen i tabellform).
- `--output-format`, `-f`: Format for å lagre importrapporten (json, csv).
    
#### Eksempel
  
For å importere alle datakilder fra eksportfilen `my_export.json` inn i `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Etter importen vil kommandoen også vise en rapport over importerte og hoppede objekter. Kun nye datakilder vil bli importert til `ProjectB`. For å finne ut hvilke objekter som ville blitt importert og hoppet over, kan du bruke kommandoen `plan-import-ds`.

### plan-import-ds

`plan-import-ds`-kommandoen i ***digna*** CLI brukes for å analysere en eksportfil før faktisk import, og lage en importplan/rapport.

#### Kommandoeksempel
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet som datakildene eventuelt ville blitt importert til.
- **EXPORT_FILE**: Filnavnet til eksporten av datakildene som skal analyseres før import.

#### Alternativer

- `--output-file`, `-o`: Fil for å lagre importrapporten (hvis ikke spesifisert, skrives den til terminalen i tabellform).
- `--output-format`, `-f`: Format for å lagre importrapporten (json, csv).
    
#### Eksempel
  
For å sjekke hvilke datakilder som ville blitt importert og hvilke som ville blitt hoppet over fra eksportfilen `my_export.json` når den importeres til `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Denne kommandoen vil kun vise en importplan over objekter som vil bli importert og hoppet over.