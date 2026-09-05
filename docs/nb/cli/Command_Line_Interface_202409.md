---
title: digna CLI Reference 2024.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.09. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
image: /assets/logo_square.png
---

# digna CLI Reference 2024.09
**2024-08-24**

---

## CLI-grunnleggende

---

###   help

--help-alternativet gir informasjon om tilgjengelige kommandoer og hvordan de brukes. Det finnes to hovedmåter å bruke dette alternativet på:

1. **Viser generell hjelp:**
   
    Bruk --help umiddelbart etter nøkkelordet ***digna***cl  
   bash
   dignacli --help

3.  **Hente hjelp for spesifikke kommandoer:**  
  
    For detaljert informasjon om en bestemt kommando, legg til --help etter den kommandoen.
    For eksempel, for å få hjelp med add-user-kommandoen, kjør:
     bash
     dignacli add-user --help
     

     ### output:
      
     - **Kommando beskrivelse:** Gir en detaljert beskrivelse av hva kommandoen gjør.  
     - **Syntaks:** Viser nøyaktig syntaks, inkludert påkrevde og valgfrie argumenter.  
     - **Valg:** Lister opp eventuelle valg som er spesifikke for kommandoen, sammen med forklaringer.  
     - **Eksempler:** Gir eksempler på hvordan kommandoen kan utføres effektivt.

  
###   check-repo-connection

check-repo-connection-kommandoen er et verktøy i ***digna*** CLI som er laget for å teste tilkobling og tilgang til et angitt ***digna***-repository. Denne kommandoen sikrer at CLI-en kan kommunisere med repositoryet.
      
##### Command Usage
bash
dignacli check-repo-connection


Ved vellykket kjøring gir kommandoen en bekreftelse på tilkoblingen, sammen med detaljer om repositoryet: Repository version, Host, Database og Schema.  
  
Hvis repository-tilkoblingen ikke lykkes, sjekk config.toml-filen for riktige konfigurasjonsinnstillinger.

###   version

For å sjekke hvilken versjon av *dignacli* som er installert, bruk --version-alternativet.  
  
#### Command Usage
bash
dignacli --version

  
#### Example Output
bash
dignacli version 2024.09


###   logging options
  
Som standard er konsollutskriften fra ***digna***-kommandoene designet for å være minimalistisk. De fleste kommandoer gir mulighet for å vise mer informasjon ved å bruke følgende alternativer:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
«verbose» og «debug» angir detaljnivået, mens «logfile»-bryteren lar deg omdirigere utdataene slik at de skrives til en fil i stedet for til konsollen.

## Brukeradministrasjon

###   add-user
  
add-user-kommandoen i ***digna*** CLI brukes til å legge til en ny bruker i ***digna***-systemet
  
#### Command Usage
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Arguments

- **USER_NAME**: Brukernavnet for den nye brukeren (påkrevd).
- **USER_FULL_NAME**: Fullt navn på den nye brukeren (påkrevd).
- **USER_PASSWORD**: Passordet for den nye brukeren (påkrevd).

#### Options

- --is_superuser, -su: Flag for å gi den nye brukeren admin-rettigheter.
- --valid_until, -vu: Setter en utløpsdato for brukerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke satt, har kontoen ingen utløpsdato.

#### Example

For å legge til en ny bruker med brukernavn jdoe, fullt navn John Doe, og passord password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
For å legge til en ny bruker og sette en utløpsdato for kontoen:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
delete-user-kommandoen i ***digna*** CLI brukes til å fjerne en eksisterende bruker fra ***digna***-systemet.
  
##### Command Usage
bash
dignacli delete-user USER_NAME

  
#### Arguments
- **USER_NAME**: Brukernavnet til brukeren som skal slettes (påkrevd). Dette er det eneste argumentet som kreves av kommandoen.

#### Example
bash
dignacli delete-user jdoe

  
Ved å kjøre denne kommandoen fjernes brukeren jdoe fra ***digna***-systemet, og deres tilgang samt tilknyttede data og rettigheter i repositoryet blir fjernet.

###   modify-user

modify-user-kommandoen i ***digna*** CLI brukes til å oppdatere detaljene for en eksisterende bruker i ***digna***-systemet.

##### Command Usage
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Arguments
  
- **USER_NAME**: Brukernavnet til brukeren som skal endres (påkrevd).
- **USER_FULL_NAME**: Det nye fulle navnet for brukeren (påkrevd).
  
#### Options  
  
- --is_superuser, -su: Setter brukeren som superuser, og gir forhøyede privilegier. Dette flagget krever ingen verdi.  
- --valid_until, -vu: Setter en utløpsdato for brukerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke angitt, forblir kontoen gyldig på ubestemt tid.  
  
#### Example
  
For å endre fullt navn til brukeren jdoe til «Johnathan Doe» og sette brukeren som superuser:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
modify-user-pwd-kommandoen i ***digna*** CLI brukes til å endre passord for en eksisterende bruker i ***digna***-systemet.
  
##### Command Usage
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Arguments
  
- **USER_NAME**: Brukernavnet til brukeren hvis passord skal endres (påkrevd).
- **USER_PWD**: Det nye passordet for brukeren (påkrevd).
  
#### Example
  
For å endre passordet til brukeren jdoe til newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

list-users-kommandoen i ***digna*** CLI viser en liste over alle brukere registrert i ***digna***-systemet.

##### Command Usage

bash
dignacli list-users


Når du kjører denne kommandoen i ***digna*** CLI, kobler den til ***digna***-repositoryet og viser alle brukere med deres ID, brukernavn, fulle navn, superuser-status og utløpstidspunkter.

# Repository-administrasjon

###   upgrade-repo
  
upgrade-repo-kommandoen i ***digna*** CLI brukes for å oppgradere eller initialisere ***digna***-repositoryet. Denne kommandoen er essensiell for å anvende oppdateringer eller sette opp repository-infrastrukturen for første gang.
  
#### Command Usage

bash
dignacli upgrade-repo [options]

  
#### Options
  
- --simulation-mode, -s: Når dette er aktivert, kjører kommandoen i simulasjonsmodus, som skriver ut SQL-setningene som ville blitt kjørt, men utfører dem ikke. Dette er nyttig for å forhåndsvise endringer uten å gjøre faktiske modifikasjoner i repositoryet.  

  
#### Example
  
For å oppgradere ***digna***-repositoryet kan du kjøre kommandoen uten noen valg:
  
bash
dignacli upgrade-repo
  
For å kjøre oppgraderingen i simulasjonsmodus (for å se SQL-setningene uten å anvende dem):
  
bash
dignacli upgrade-repo --simulation-mode

  
Denne kommandoen er viktig for vedlikehold av ***digna***-systemet, og sikrer at databaseskjemaet og andre repository-komponenter er oppdatert i henhold til nyeste versjon av programvaren.

###   encrypt
  
encrypt-kommandoen i ***digna*** CLI brukes til å kryptere et passord.
  
#### Command Usage
  
bash
dignacli encrypt <PASSWORD>

    
#### Arguments
- **PASSWORD**: Passordet som skal krypteres (påkrevd).
  
#### Example
  
For å kryptere et passord må du oppgi passordet som et argument.   
For eksempel, for å kryptere passordet mypassword123, ville du bruke:
bash
dignacli encrypt mypassword123

Denne kommandoen returnerer den krypterte versjonen av det oppgitte passordet, som deretter kan brukes i sikre sammenhenger. Hvis passord-argumentet ikke oppgis, vil CLI-en vise en feilmelding som indikerer det manglende argumentet.

###   generate-key
  
generate-key-kommandoen brukes til å generere en Fernet-nøkkel, som er viktig for å sikre passord som lagres i ***digna***-repositoryet.
  
#### Command Usage
bash
dignacli generate-key

  
## Databehandling

###   clean-up

clean-up-kommandoen i ***digna*** CLI brukes til å fjerne profiler, prediksjoner og data fra trafikklyssystemet for en eller flere datakilder innen et spesifisert prosjekt. Denne kommandoen er viktig for datalivssyklushåndtering, og hjelper med å holde et organisert og effektivt dataomfang ved å fjerne utdaterte eller unødvendige data.

#### Command Usage

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Navnet på prosjektet hvor data skal fjernes fra (påkrevd). Bruker du nøkkelordet all-projects i dette argumentet, instruerer du ***digna*** til å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og -tid for datarensingen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datarensingen, med samme formater som FROM_DATE (påkrevd).
  
#### Options
  
- --table-name, -tn: Begrens clean-up-operasjonen til en spesifikk tabell innen prosjektet.
- --table-filter, -tf: Filtrerer for å begrense clean-up til tabeller som inneholder den angitte understrengen i navnet.
- --timing, -tm: Viser tidsbruken for clean-up-prosessen etter fullføring.
- --help: Viser hjelpeinformasjon for clean-up-kommandoen og avslutter.
  
#### Example
  
For å fjerne data fra prosjektet ProjectA mellom 1. januar 2023 og 30. juni 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
For å fjerne data kun fra en spesifikk tabell kalt Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Denne kommandoen hjelper med å administrere datalagring og sikre at repositoryet kun inneholder relevant informasjon.

###   inspect

inspect-kommandoen i ***digna*** CLI brukes til å opprette profiler, prediksjoner og data for trafikklyssystemet for en eller flere datakilder innen et spesifisert prosjekt. Denne kommandoen hjelper med å analysere og overvåke data over en definert periode.

#### Command Usage

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Navnet på prosjektet som data skal inspiseres for (påkrevd). Bruker du nøkkelordet all-projects i dette argumentet, instruerer du ***digna*** til å iterere over alle eksisterende prosjekter og anvende denne kommandoen.
- **FROM_DATE**: Startdato og -tid for datainspeksjonen. Akseptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrevd).
- **TO_DATE**: Sluttdato og -tid for datainspeksjonen, med samme formater som FROM_DATE (påkrevd).
  
#### Options

- --table-name, -tn: Begrens inspeksjonen til en spesifikk tabell i prosjektet.
- --table-filter, -tf: Filtrerer for å inspisere kun tabeller som inneholder den angitte understrengen i navnet.
- --force-profile: Tvinger re-innsamling av profiler. Standard er force-profile.
- --no-force-profile: Forhindrer re-innsamling av profiler.
- --force-prediction: Tvinger nyberegning av prediksjoner. Standard er force-prediction.
- --no-force-prediction: Forhindrer nyberegning av prediksjoner.
- --force-alert-status: Tvinger nyberegning av varslingsstatus. Standard er force-alert-status.
- --no-force-alert-status: Forhindrer nyberegning av varslingsstatus.
- --timing, -tm: Viser varigheten av inspeksjonsprosessen etter fullføring.
- --alert-notification, -an: Sender varslingsmeldinger til påmeldte kanaler.
  
#### Example
  
For å inspisere data for prosjektet ProjectA fra 1. januar 2024 til 31. januar 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
For å inspisere kun en bestemt tabell og tvinge nyberegning av prediksjoner:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Denne kommandoen er nyttig for å generere oppdaterte profiler og prediksjoner, overvåke dataintegritet og administrere varslingssystemer innen et spesifisert prosjekttidsrom.

###   tls-status

tls-status-kommandoen i ***digna*** CLI brukes for å spørre om statusen til Trafikklyssystemet (TLS) for en spesifikk tabell innen et prosjekt på en gitt dato. Trafikklyssystemet gir innsikt i datakvalitet og helse, og indikerer eventuelle problemer eller varsler som kan kreve oppmerksomhet.
  
#### Command Usage
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Arguments
  
- **PROJECT_NAME**: Navnet på prosjektet som TLS-statusen blir spurt for (påkrevd).
- **TABLE_NAME**: Den spesifikke tabellen i prosjektet som TLS-statusen gjelder for (påkrevd).
- **DATE**: Datoen for hvilken TLS-statusen forespørres, vanligvis i formatet %Y-%m-%d (påkrevd).
  
#### Example
  
For å sjekke TLS-statusen for en tabell kalt UserData i prosjektet ProjectA den 1. juli 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Denne kommandoen hjelper brukere med å overvåke og opprettholde datakvalitet ved å gi en klar og handlingsrettet statusrapport basert på forhåndsdefinerte kriterier.

###   list-projects
  
list-projects-kommandoen i ***digna*** CLI brukes for å vise en liste over alle tilgjengelige prosjekter i ***digna***-systemet.
  
#### Command Usage
  
bash
dignacli list-projects


Denne kommandoen er spesielt nyttig for administratorer og brukere som håndterer flere prosjekter, og gir en rask oversikt over tilgjengelige prosjekter i ***digna***-repositoryet.

###   list-ds

list-ds-kommandoen i ***digna*** CLI brukes for å vise en liste over alle tilgjengelige datakilder innen et spesifisert prosjekt. Denne kommandoen er nyttig for å få oversikt over dataressursene som er tilgjengelige for analyse og administrasjon i ***digna***-systemet.

#### Command Usage
  
bash
dignacli list-ds <PROJECT_NAME>


#### Arguments
- **PROJECT_NAME**: Navnet på prosjektet som datakildene skal listes for (påkrevd).
  
#### Example
  
For å liste alle datakilder i prosjektet kalt ProjectA:
  
bash
dignacli list-ds ProjectA

  
Denne kommandoen gir brukerne en oversikt over datakildene som er tilgjengelige i et prosjekt, og hjelper dem med å navigere og administrere datalandskapet mer effektivt.