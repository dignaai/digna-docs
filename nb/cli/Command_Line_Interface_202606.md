# digna CLI-referanse 2026.06
**2026-09-05**

Denne siden dokumenterer det komplette settet med kommandoer som er tilgjengelige i ***digna*** CLI-utgivelse **2026.06**, inkludert bruksområder og alternativer.

Den kjørbare filen heter `digna`.

---

## CLI-grunnlaget

---

### Oversikt og syntaks

CLI-en i utgivelse **2026.06** bruker et strukturert, kategoribasert kommandohierarki:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` og `serve` er enkeltstående kommandoer uten underkommando:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Globale alternativer

Følgende globale alternativer gjelder for alle kommandoer:

- `--help`, `-h`: Viser hjelpeinformasjon for CLI-en eller for en bestemt kommandokategori eller underkommando.
- `--stacktrace`: Viser hele feilkjeden ved feil, i stedet for bare meldingen på øverste nivå.

`--stacktrace` er et globalt alternativ i streng forstand: det må angis **før** kommandokategorien, ikke etter.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Det finnes ikke noe `--version`-flagg. Bruk kommandoen [`version`](#version) i stedet.

### Forutsetninger

De fleste kommandoer trenger en lesbar, gyldig `config.toml`; noen krever i tillegg en gyldig lisens.
Tabellen nedenfor viser hva hver kommandokategori laster inn før den foretar seg noe som helst:

| Kommandokategori | Trenger `config.toml` | Trenger en gyldig lisens |
|---|---|---|
| `version` | nei | nei |
| `config check` | nei (det er nettopp dette kommandoen rapporterer om) | nei |
| `license check` | nei | den *er* selve kontrollen |
| `crypt` | ja | nei |
| `serve` | ja | nei |
| `windows` | nei (tjenesten leser den når den starter) | nei |
| `project` | ja | nei |
| `user` | ja | ja |
| `inspection` | ja | ja |
| `repo` | ja | ja |

Der en lisens kreves, kontrolleres både signaturen og utløpsdatoen, og kommandoen avbrytes før den berører repositoriet dersom én av delene feiler.

### Avslutningskoder

- `0`: kommandoen lyktes.
- `1`: kommandoen mislyktes. Feilmeldingen skrives til stderr med prefikset `Error: `.

### help

Alternativet `--help` gir informasjon om tilgjengelige kommandokategorier, underkommandoer og alternativer:

1. **Vise generell hjelp:**
   ```bash
   digna --help
   ```

2. **Hente hjelp for bestemte kategorier og kommandoer:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Utdataene omfatter:**
   - **Kommandobeskrivelse:** Sammendrag av kommandoens formål.
   - **Syntaks:** Påkrevde og valgfrie argumenter.
   - **Alternativer:** Flagg og parametere som er spesifikke for kommandoen.

### version

Kommandoen `version` skriver ut den installerte ***digna***-utgivelsen. Den leser ingen konfigurasjon og validerer ingen lisens, så den fungerer også på en installasjon der `config.toml` eller lisensen mangler eller er ugyldig.

Utgivelsesversjonen er uavhengig av repositorieskjemaversjonen som [`repo check`](#repo-check) rapporterer.

#### Kommandobruk
```bash
digna version
```

#### Eksempelutdata
```text
2026.06
```

---

## Konfigurasjonsbehandling

---

### config check

Kommandoen `config check` validerer konfigurasjonsfilen (`config.toml`) og kontrollerer at alle obligatoriske seksjoner og innstillinger finnes og er riktig formatert. Hver seksjon valideres for seg, slik at en ødelagt `[app]`-seksjon ikke skjuler tilstanden til `[repo]`.

Seksjonene det rapporteres om, er:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — valgfri; en manglende nøkkel består, mens en liste som finnes, men er feilformatert, ikke består

Kommandoen laster bevisst ikke applikasjonskonfigurasjonen slik de andre kommandoene gjør, slik at den kan diagnostisere en `config.toml` som ville hindret ***digna*** i å starte i det hele tatt.

#### Kommandobruk
```bash
digna config check [OPTIONS]
```

#### Alternativer
- `--configpath`, `-c`: Sti til konfigurasjonsfilen, eller til en katalog som inneholder `config.toml` (standard `./config.toml`).
- `--json`: Skriver ut valideringsrapporten som JSON. Har forrang framfor `--quiet`.
- `--quiet`, `-q`: Undertrykker rapporten og støtter seg utelukkende på avslutningskoden.

#### Eksempel
```bash
digna config check
```

Validere en bestemt konfigurasjonsfil og formatere utdataene som JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Eksempelutdata
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

En manglende fil eller en TOML-syntaksfeil etterlater ingenting å validere seksjon for seksjon, og rapporteres som én enkelt feil i stedet for en rapport, uavhengig av `--quiet` eller `--json`.

---

## Repositoriebehandling

---

### repo check

Kommandoen `repo check` tester databasetilkoblingen og bekrefter repositoriets installasjon og versjon. Den feiler hvis det konfigurerte skjemaet ikke finnes, eller hvis det finnes, men ikke inneholder noe ***digna***-repositorium.

Versjonen som rapporteres, er versjonen av repositorieskjemaet, som versjoneres uavhengig av ***digna***-utgivelsen [`version`](#version) skriver ut.

#### Kommandobruk
```bash
digna repo check
```

#### Eksempelutdata
```text
Repo version 3.0.0 installed
```

### repo install

Kommandoen `repo install` installerer et nytt ***digna***-repositorium i skjemaet som er konfigurert i `config.toml`, og oppretter alle nødvendige sekvenser, tabeller, indekser, begrensninger og innledende poster.

Selve skjemaet opprettes **ikke** av denne kommandoen — det må finnes på forhånd. Kommandoen nekter også å kjøre dersom et repositorium allerede er installert i det skjemaet, og peker på [`repo upgrade`](#repo-upgrade) hvis den installerte versjonen er eldre.

#### Kommandobruk
```bash
digna repo install
```

#### Eksempelutdata
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Kommandoen `repo upgrade` bruker skjemamigreringer i databasen for å løfte et eksisterende repositorium til versjonen den installerte utgivelsen forventer. Oppgraderinger utføres ett versjonssteg om gangen langs en fast oppgraderingssti, og hvert fullførte steg registreres i repositoriet.

Hvis repositoriet allerede er på forventet versjon, melder kommandoen at ingen oppgradering er nødvendig, og gjør ingen endringer.

#### Kommandobruk
```bash
digna repo upgrade
```

#### Eksempelutdata
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

### repo prune

Kommandoen `repo prune` fjerner rader som har overlevd prosjektet eller datakilden de tilhørte.
Når et prosjekt eller en datakilde slettes, fjernes selve objektet, men profilene, prediksjonene,
statusene og radtellingene blir liggende igjen — et bevisst valg, siden en sletting som også ryddet
disse tabellene ville latt brukeren vente. `repo prune` er ryddejobben som fjerner dem, og den er trygg
å kjøre når som helst: den fjerner bare rader der prosjektet eller datakilden ikke lenger finnes.

Rader som Python-backenden har skrevet til tabeller som den gjeldende utgivelsen ikke lenger bruker, blir latt være i fred.

#### Kommandobruk
```bash
digna repo prune [OPTIONS]
```

#### Alternativer
- `--dry-run`: Rapporter hva som ville blitt fjernet, uten å fjerne noe.

Bare tabeller med foreldreløse rader blir listet opp. Finnes det ingen, melder kommandoen
`No orphaned rows found.` og avslutter.

#### Eksempel
```bash
digna repo prune
```

#### Eksempelutdata
```text
"check"                                 29342
check_profile                           29342
check_prediction                        29342
check_status                            29342
column_status                              32
inspection_query                          253
---------------------------------------------
total                                  117854

✅ Removed 117854 orphaned row(s).
```

Slik ser du den samme rapporten uten å fjerne noe:
```bash
digna repo prune --dry-run
```

Radtellingene er identiske; bare den siste linjen er forskjellig:
```text
---------------------------------------------
total                                  117854

Dry run - nothing was removed.
```

---

## Krypteringsbehandling

---

### crypt gen-key

Kommandoen `crypt gen-key` genererer en ny AES-GCM-krypteringsnøkkel til bruk som krypteringsnøkkel i `config.toml`. En lesbar `config.toml` må allerede finnes, selv om den genererte nøkkelen ikke avhenger av den.

#### Kommandobruk
```bash
digna crypt gen-key
```

#### Eksempelutdata
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Kommandoen `crypt encrypt` krypterer en streng (for eksempel et databasepassord) med AES-GCM-nøkkelen som er konfigurert i `config.toml`, og skriver ut chifferteksten.

#### Kommandobruk
```bash
digna crypt encrypt <VALUE>
```

#### Argumenter
- **VALUE**: Klartekststrengen som skal krypteres (påkrevd).

#### Eksempel
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Kommandoen `crypt decrypt` dekrypterer en AES-GCM-kryptert streng med nøkkelen som er konfigurert i `config.toml`, og skriver ut klarteksten.

#### Kommandobruk
```bash
digna crypt decrypt <VALUE>
```

#### Argumenter
- **VALUE**: Den krypterte chiffertekststrengen som skal dekrypteres (påkrevd).

#### Eksempel
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Brukerbehandling

---

### user add

Kommandoen `user add` oppretter en ny brukerkonto i ***digna***-repositoriet. Kommandoen feiler hvis en bruker med den oppgitte e-postadressen allerede finnes.

#### Kommandobruk
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenter
- **EMAIL**: Brukerens e-postadresse (påkrevd).
- **PASSWORD**: Brukerens innledende passord (påkrevd).
- **DISPLAY_NAME**: Brukerens fulle visningsnavn (påkrevd).

#### Alternativer
- `--admin`, `-a`: Oppretter brukeren med administratorrettigheter (superbruker).

#### Eksempel
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Slik oppretter du en administratorkonto:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Eksempelutdata
```text
User created with ID: 42
```

### user list

Kommandoen `user list` lister opp alle registrerte brukere i tabellform med ID, e-post, visningsnavn og administratorflagg.

#### Kommandobruk
```bash
digna user list
```

#### Eksempelutdata
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Kommandoen `user modify` oppdaterer visningsnavnet og administratorrettighetene til en eksisterende brukerkonto, identifisert ved e-postadresse.

Både visningsnavnet og administratorflagget skrives alltid. `--admin` er en bryter, ikke en verdi: **å utelate det opphever administratorrettighetene**, så angi det hver gang brukeren skal beholde eller få dem.

#### Kommandobruk
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenter
- **EMAIL**: E-postadressen til brukeren som skal endres (påkrevd).
- **DISPLAY_NAME**: Det oppdaterte visningsnavnet (påkrevd).

#### Alternativer
- `--admin`, `-a`: Gir administratorrettigheter. Utelat for å oppheve dem.
- `--valid-until`, `-v`: Godtas av kompatibilitetshensyn, men **brukes ikke for øyeblikket**. Angis det, skrives det ut en advarsel, og ingenting endres.

#### Eksempel
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Eksempelutdata
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Kommandoen `user modify-pwd` oppdaterer passordet til en eksisterende brukerkonto.

#### Kommandobruk
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumenter
- **EMAIL**: E-postadressen til brukeren som skal få oppdatert passord (påkrevd).
- **PASSWORD**: Det nye passordet (påkrevd).

#### Eksempel
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Kommandoen `user delete` fjerner en brukerkonto fra systemet.

#### Kommandobruk
```bash
digna user delete <EMAIL>
```

#### Argumenter
- **EMAIL**: E-postadressen til brukeren som skal slettes (påkrevd).

#### Eksempel
```bash
digna user delete jdoe@example.com
```

---

## Prosjekt- og datakildebehandling

---

### project list

Kommandoen `project list` lister opp alle tilgjengelige prosjekter i repositoriet og viser ID, navn og beskrivelse.

#### Kommandobruk
```bash
digna project list
```

#### Eksempelutdata
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Kommandoen `project list-ds` lister opp alle datakilder knyttet til et gitt prosjekt og viser ID, navn, type, skjema og tabellnavn.

#### Kommandobruk
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet hvis datakilder skal listes opp (påkrevd). Navnet må stemme nøyaktig.

#### Eksempel
```bash
digna project list-ds ProjectA
```

#### Eksempelutdata
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Kommandoen `project export-ds` eksporterer datakilder fra et prosjekt til et JSON-dokument.

Hvis verken `--table-name` eller `--table-id` er angitt, eksporteres alle datakildene i prosjektet.

#### Kommandobruk
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på prosjektet det skal eksporteres datakilder fra (påkrevd).

#### Alternativer
- `--table-name`, `-n`: Navn på datakildene som skal eksporteres. Flere navn kan angis atskilt med mellomrom.
- `--table-id`, `-i`: ID-er til datakildene som skal eksporteres. Flere ID-er kan angis atskilt med mellomrom.
- `--exportfile`, `-f`: Sti der de eksporterte datakildene lagres (standard: `data_sources_export.json`).

#### Eksempel
Slik eksporterer du alle datakilder fra `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Slik eksporterer du bestemte tabeller:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Eksempelutdata
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Kommandoen `project import-ds` importerer datakilder fra en eksportfil til et målprosjekt og rapporterer per objekt hva som ble opprettet, oppdatert eller hoppet over.

#### Kommandobruk
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på målprosjektet det skal importeres til (påkrevd).
- **EXPORT_FILE**: Sti til JSON-eksportfilen (påkrevd).

#### Alternativer
- `--output-file`, `-o`: Fil som importrapporten skrives til. Uten den går rapporten til stdout.
- `--output-format`, `-f`: Format på importrapporten — `table`, `json` eller `csv` (standard: `table`).

#### Eksempel
```bash
digna project import-ds ProjectB my_export.json
```

Slik får du en maskinlesbar rapport:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Rapporten dekker fire objektnivåer — datakilde, datasettdefinisjon, attributt og valideringsregel — hvert med sin importhandling, sitt resultat, ID-en til objektet som ble til, og eventuell tilleggsinformasjon.

### project plan-import-ds

Kommandoen `project plan-import-ds` forhåndsviser en datakildeimport til et målprosjekt og viser hvilke objekter som ville blitt opprettet, oppdatert eller hoppet over, uten å endre noe. Den tar den samme eksportfilen og de samme rapportalternativene som [`project import-ds`](#project-import-ds), og legger til et trinnummer per planlagt objekt.

#### Kommandobruk
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på målprosjektet (påkrevd).
- **EXPORT_FILE**: Sti til eksportfilen (påkrevd).

#### Alternativer
- `--output-file`, `-o`: Fil som importplanen skrives til. Uten den går planen til stdout.
- `--output-format`, `-f`: Format på importplanen — `table`, `json` eller `csv` (standard: `table`).

#### Eksempel
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

### project cleanup

Kommandoen `project cleanup` fjerner inspeksjonsresultatene et prosjekt har samlet opp over et datointervall
— profiler, prediksjoner, radtellinger og alle statuser for sjekker, attributter, datasett og datakilder. Den
fjerner nøyaktig det en inspeksjon av disse datoene skrev, slik at intervallet kan inspiseres på nytt etterpå
for å bygge det opp igjen.

Historikken for Timeliness og Schema Tracker blir **ikke** fjernet: den registrerer hva digna observerte en
gitt dag, ikke et resultat som er avledet av det, så en opprydding av et tidligere datointervall lar den være
urørt.

Hver datakilde ryddes i sin egen transaksjon, så en avbrutt kjøring etterlater hele datakilder
i stedet for en halvveis ryddet en.

#### Kommandobruk
```bash
digna project cleanup <PROJECT_NAME> <FROM_DATE> <TO_DATE> [OPTIONS]
```

#### Argumenter
- **PROJECT_NAME**: Prosjektet som skal ryddes (påkrevd). Ett prosjekt per kjøring.
- **FROM_DATE**: Første dato det skal fjernes resultater for, `YYYY-MM-DD` (påkrevd).
- **TO_DATE**: Siste dato det skal fjernes resultater for, inklusive, `YYYY-MM-DD` (påkrevd).

#### Alternativer
- `--table-name`, `-n`: Begrens oppryddingen til disse datakildene. Flere navn kan angis
  atskilt med mellomrom.
- `--table-filter`: Begrens oppryddingen til datakilder der navnet inneholder denne delstrengen.
- `--dry-run`: List opp datakildene som ville blitt ryddet, uten å fjerne noe.
- `--timing`: Vis hvor lang tid oppryddingen tok.

`--table-name` og `--table-filter` kombineres som ELLER — en datakilde ryddes hvis den er navngitt eller
hvis delstrengen samsvarer. Kommandoen feiler hvis ingen datakilde samsvarer, i stedet for å melde
suksess for en opprydding som ikke gjorde noe.

#### Eksempel
```bash
digna project cleanup ProjectA 2026-01-01 2026-06-30
```

Begrenset til én datakilde:
```bash
digna project cleanup ProjectA 2026-01-01 2026-06-30 --table-name Table1
```

#### Eksempelutdata
```text
Cleaning up project 'ProjectA' from 2026-01-01 to 2026-06-30:
- Table1
- Table2
- Table3

✅ Cleaned up 3 data source(s).
```

Slik ser du hvilke datakilder som ville blitt ryddet, uten å fjerne noe:
```bash
digna project cleanup ProjectA 2026-01-01 2026-06-30 --dry-run
```

Hver linje er merket, så en prøvekjøring kan ikke forveksles med en ekte kjøring:
```text
Cleaning up project 'ProjectA' from 2026-01-01 to 2026-06-30:
- Table1 (dry run, nothing removed)
- Table2 (dry run, nothing removed)
- Table3 (dry run, nothing removed)

Dry run - 3 data source(s) would be cleaned up.
```

---

## Inspeksjonsbehandling

---

### inspection run

Kommandoen `inspection run` oppretter en inspeksjonsforespørsel for et prosjekt og et datointervall, og deretter — avhengig av alternativene som er angitt — venter den på den, returnerer umiddelbart, eller kjører den i sin egen prosess.

De tre kjøremodusene er:

- **Standard (uten flagg)**: forespørselen legges i kø for backend-en, og CLI-en spør den hvert andre sekund og skriver ut oppgavefremdriften til inspeksjonen når en sluttilstand. En kjørende `digna serve` er påkrevd, ellers er det ingen som plukker opp forespørselen.
- **`--async-mode`**: forespørselen legges i kø, og ID-en skrives ut umiddelbart. Bruk [`inspection status`](#inspection-status) for å følge den.
- **`--bypass-backend`**: inspeksjonen kjøres av CLI-prosessen selv og legges ikke i kø, så det trengs ingen kjørende server.

`--async-mode` og `--bypass-backend` utelukker hverandre.

I alle modusene avsluttes kommandoen med en avslutningskode ulik null dersom inspeksjonen ikke ble fullført på riktig måte.

#### Kommandobruk
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på målprosjektet (påkrevd). Navnet må stemme nøyaktig.
- **START_DATE**: Startdato for datointervallet i formatet `YYYY-MM-DD` (påkrevd).
- **END_DATE**: Sluttdato for datointervallet i formatet `YYYY-MM-DD` (påkrevd).

#### Alternativer
- `--table-name`: Begrenser inspeksjonen til én enkelt datakilde i prosjektet, angitt ved datakildenavnet. Uten den inspiseres alle datakildene i prosjektet.
- `--async-mode`: Legger inspeksjonen i kø og skriver ut forespørsels-ID-en i stedet for å vente på den. Kan ikke kombineres med `--bypass-backend`.
- `--bypass-backend`: Kjører inspeksjonen direkte i CLI-prosessen i stedet for å legge den i kø for backend-en. Kan ikke kombineres med `--async-mode`.

#### Eksempel
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Slik sender du inn en asynkron inspeksjon:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Slik inspiserer du én enkelt datakilde:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Eksempelutdata
Standardmodus:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asynkron modus:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Kommandoen `inspection status` henter tilstanden og oppgavefremdriften til en inspeksjonsforespørsel ut fra forespørsels-ID-en.

#### Kommandobruk
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumenter
- **INSPECTION_REQUEST_ID**: Den numeriske ID-en til inspeksjonsforespørselen (påkrevd).

#### Eksempel
```bash
digna inspection status 1024
```

#### Eksempelutdata
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Kommandoen `inspection abort` ber om at kjørende eller ventende inspeksjonsforespørsler avbrytes. Den registrerer en stopphendelse for hver berørt forespørsel; backend-en handler ut fra den, så et avbrudd er en anmodning om å stoppe snarere enn en umiddelbar terminering.

#### Kommandobruk
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumenter
- **INSPECTION_REQUEST_ID**: ID-en til inspeksjonsforespørselen som skal avbrytes. Påkrevd med mindre `--killall` er angitt.

#### Alternativer
- `--killall`: Avbryter alle inspeksjonsforespørsler som kjører eller venter nå. Har forrang framfor en forespørsels-ID som angis sammen med den.

#### Eksempel
Slik avbryter du en bestemt forespørsel:
```bash
digna inspection abort 1024
```

Slik avbryter du alle aktive og køsatte inspeksjoner:
```bash
digna inspection abort --killall
```

#### Eksempelutdata
`--killall` rapporterer hva den gjorde; avbrudd av én enkelt forespørsel gir ingen utdata og melder om suksess gjennom avslutningskoden sin.
```text
All running and pending inspections have been aborted.
```

---

## Lisensbehandling

---

### license check

Kommandoen `license check` validerer `license.toml`, kontrollerer signaturen mot den offentlige nøkkelen som følger med installasjonen, og sjekker at lisensen ikke er utløpt. Den leser ingen applikasjonskonfigurasjon, så den fungerer også før `config.toml` er satt opp.

#### Kommandobruk
```bash
digna license check
```

#### Eksempelutdata
```text
License is valid
```

En ugyldig signatur og en utløpt lisens rapporteres som to ulike feil, begge med avslutningskode 1.

---

## Server- og bakgrunnstjenester

---

### serve

Kommandoen `serve` starter ***digna***-REST-API-serveren sammen med bakgrunnsplanleggeren for inspeksjoner og inspeksjonsbehandleren. Ved oppstart lar den også enhver inspeksjon som repositoriet fortsatt registrerer som kjørende, feile, siden ingenting kan ha overlevd fra en tidligere prosess.

Kommandoen kjører i forgrunnen til den stoppes.

#### Kommandobruk
```bash
digna serve [OPTIONS]
```

#### Alternativer
- `--address`: Nettverksadressen API-serveren skal bindes til (standard: `127.0.0.1`).
- `--port`: Portnummeret det lyttes på (standard: `8000`).

#### Eksempel
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Eksempelutdata
```text
Server running on http://0.0.0.0:8000
```

---

## Windows-tjenestebehandling

Kun tilgjengelig på Windows. Kommandoene registrerer ***digna***-backenden hos Windows-tjenestebehandleren
og styrer den; selve tjenesten kjører `serve` i bakgrunnen. Alle kommandoer
må kjøres fra en ledetekst med administratorrettigheter, og hver av dem godtar `--name`, slik at en tjeneste
som er registrert under et annet navn enn standardnavnet, kan adresseres.

---

### windows install

Kommandoen `windows install` registrerer ***digna*** som en Windows-tjeneste.

Adressen og porten som angis her, lagres i tjenesteregistreringen og er det tjenesten binder seg til
— de leses ikke fra `config.toml`. For å endre dem senere må du avinstallere
tjenesten og installere den på nytt.

#### Kommandobruk
```bash
digna windows install [OPTIONS]
```

#### Alternativer
- `--name`: Navnet tjenesten registreres under (standard: `digna`).
- `--display-name`: Navnet som vises i services.msc (standard: `digna`).
- `--description`: Beskrivelsen som vises i services.msc (standard: `digna data quality backend`).
- `--address`: Adressen tjenesten binder API-et sitt til (standard: `127.0.0.1`).
- `--port`: Porten tjenesten binder API-et sitt til (standard: `8000`).
- `--working-dir`: Katalogen som inneholder `config.toml` og `license.toml`, og som tjenesten bruker
  som arbeidskatalog (standard: katalogen til den kjørbare filen `digna`).
- `--start-type`: Når tjenesten starter — `auto` sammen med Windows, `manual` bare på forespørsel,
  `disabled` registrert, men nekter å starte (standard: `auto`).
- `--account`: Kontoen tjenesten kjører som, f.eks. `DOMAIN\user` eller `.\user` (standard: `LocalSystem`).
- `--password`: Passordet til `--account`.

#### Eksempel
```bash
digna windows install --address 0.0.0.0 --port 8082
```

Registrer under et annet navn og kjør som en domenekonto:
```bash
digna windows install --name digna-test --display-name "digna (test)" --account DOMAIN\svc_digna --password <password>
```

---

### windows start

Kommandoen `windows start` starter en registrert tjeneste.

#### Kommandobruk
```bash
digna windows start [OPTIONS]
```

#### Alternativer
- `--name`: Navnet tjenesten er registrert under (standard: `digna`).

---

### windows stop

Kommandoen `windows stop` stopper en kjørende tjeneste. Stopp tjenesten før du erstatter noen
applikasjonsfil.

#### Kommandobruk
```bash
digna windows stop [OPTIONS]
```

#### Alternativer
- `--name`: Navnet tjenesten er registrert under (standard: `digna`).

---

### windows uninstall

Kommandoen `windows uninstall` avregistrerer tjenesten. Stopp den først.

#### Kommandobruk
```bash
digna windows uninstall [OPTIONS]
```

#### Alternativer
- `--name`: Navnet tjenesten er registrert under (standard: `digna`).