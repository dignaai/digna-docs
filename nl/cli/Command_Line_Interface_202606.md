# digna CLI-referentie 2026.06
**2026-09-05**

Deze pagina documenteert de volledige set opdrachten die beschikbaar is in ***digna*** CLI-release **2026.06**, inclusief gebruiksvoorbeelden en opties.

Het uitvoerbare bestand heet `digna`.

---

## CLI-basisprincipes

---

### Overzicht & syntaxis

De CLI van release **2026.06** gebruikt een gestructureerde, op categorieën gebaseerde opdrachthiërarchie:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` en `serve` zijn losse opdrachten zonder subopdracht:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Globale opties

De volgende globale opties gelden voor alle opdrachten:

- `--help`, `-h`: Toont hulpinformatie over de CLI of over een specifieke opdrachtcategorie of subopdracht.
- `--stacktrace`: Toont bij een fout de volledige foutketen in plaats van alleen het bovenste bericht.

`--stacktrace` is in strikte zin een globale optie: hij moet **vóór** de opdrachtcategorie worden opgegeven, niet erna.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Er is geen `--version`-vlag. Gebruik in plaats daarvan de opdracht [`version`](#version).

### Vereisten

De meeste opdrachten hebben een leesbare, geldige `config.toml` nodig; sommige vereisen daarnaast een geldige licentie.
De volgende tabel legt vast wat elke opdrachtcategorie laadt voordat ze ook maar iets doet:

| Opdrachtcategorie | Vereist `config.toml` | Vereist een geldige licentie |
|---|---|---|
| `version` | nee | nee |
| `config check` | nee (het is precies waarover de opdracht rapporteert) | nee |
| `license check` | nee | het *is* de controle |
| `crypt` | ja | nee |
| `serve` | ja | nee |
| `project` | ja | nee |
| `user` | ja | ja |
| `inspection` | ja | ja |
| `repo` | ja | ja |

Waar een licentie vereist is, worden zowel de handtekening als de vervaldatum gecontroleerd, en de opdracht breekt af voordat ze de repository aanraakt als een van beide faalt.

### Afsluitcodes

- `0`: de opdracht is geslaagd.
- `1`: de opdracht is mislukt. Het foutbericht wordt naar stderr geschreven, voorafgegaan door `Error: `.

### help

De optie `--help` geeft informatie over beschikbare opdrachtcategorieën, subopdrachten en opties:

1. **Algemene hulp weergeven:**
   ```bash
   digna --help
   ```

2. **Hulp opvragen voor specifieke categorieën en opdrachten:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **De uitvoer bevat:**
   - **Opdrachtbeschrijving:** Samenvatting van het doel van de opdracht.
   - **Syntaxis:** Vereiste en optionele argumenten.
   - **Opties:** Vlaggen en parameters die specifiek zijn voor de opdracht.

### version

De opdracht `version` toont de geïnstalleerde ***digna***-release. Ze leest geen configuratie en valideert geen licentie, dus ze werkt ook op een installatie waarvan de `config.toml` of de licentie ontbreekt of ongeldig is.

De releaseversie staat los van de versie van het repositoryschema die door [`repo check`](#repo-check) wordt gemeld.

#### Gebruik van de opdracht
```bash
digna version
```

#### Voorbeelduitvoer
```text
2026.06
```

---

## Configuratiebeheer

---

### config check

De opdracht `config check` valideert het configuratiebestand (`config.toml`) en controleert of alle verplichte secties en instellingen aanwezig en correct opgemaakt zijn. Elke sectie wordt afzonderlijk gevalideerd, zodat een defecte `[app]`-sectie de toestand van `[repo]` niet verbergt.

De gerapporteerde secties zijn:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — optioneel; een ontbrekende sleutel slaagt, een aanwezige maar onjuist opgemaakte lijst faalt

De opdracht laadt de applicatieconfiguratie bewust niet op de manier waarop de andere opdrachten dat doen, zodat ze een `config.toml` kan diagnosticeren die ***digna*** volledig zou beletten te starten.

#### Gebruik van de opdracht
```bash
digna config check [OPTIONS]
```

#### Opties
- `--configpath`, `-c`: Pad naar het configuratiebestand of naar een map die `config.toml` bevat (standaard `./config.toml`).
- `--json`: Geeft het validatierapport als JSON uit. Heeft voorrang op `--quiet`.
- `--quiet`, `-q`: Onderdrukt het rapport en vertrouwt uitsluitend op de afsluitcode.

#### Voorbeeld
```bash
digna config check
```

Een specifiek configuratiebestand valideren en de uitvoer als JSON opmaken:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Voorbeelduitvoer
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

Een ontbrekend bestand of een TOML-syntaxisfout laat niets over om sectie voor sectie te valideren en wordt als één enkele fout gerapporteerd in plaats van als een rapport, ongeacht `--quiet` of `--json`.

---

## Repositorybeheer

---

### repo check

De opdracht `repo check` test de databaseverbinding en verifieert de installatie en versie van de repository. Ze mislukt als het geconfigureerde schema niet bestaat, of als het wel bestaat maar geen ***digna***-repository bevat.

De gemelde versie is de versie van het repositoryschema, dat los van de door [`version`](#version) getoonde ***digna***-release wordt geversioneerd.

#### Gebruik van de opdracht
```bash
digna repo check
```

#### Voorbeelduitvoer
```text
Repo version 3.0.0 installed
```

### repo install

De opdracht `repo install` installeert een nieuwe ***digna***-repository in het schema dat in `config.toml` is geconfigureerd en maakt daarbij alle vereiste sequenties, tabellen, indices, constraints en initiële records aan.

Het schema zelf wordt **niet** door deze opdracht aangemaakt — het moet vooraf bestaan. De opdracht weigert ook te draaien als er al een repository in dat schema is geïnstalleerd, en verwijst naar [`repo upgrade`](#repo-upgrade) als de geïnstalleerde versie een oudere is.

#### Gebruik van de opdracht
```bash
digna repo install
```

#### Voorbeelduitvoer
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

De opdracht `repo upgrade` past databaseschemamigraties toe om een bestaande repository op de versie te brengen die de geïnstalleerde release verwacht. Upgrades worden één versiestap tegelijk toegepast langs een vast upgradepad, en elke voltooide stap wordt in de repository vastgelegd.

Als de repository al op de verwachte versie staat, meldt de opdracht dat er geen upgrade nodig is en brengt ze geen wijzigingen aan.

#### Gebruik van de opdracht
```bash
digna repo upgrade
```

#### Voorbeelduitvoer
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Versleutelingsbeheer

---

### crypt gen-key

De opdracht `crypt gen-key` genereert een nieuwe AES-GCM-versleutelingssleutel, bedoeld voor gebruik als versleutelingssleutel in `config.toml`. Er moet al een laadbare `config.toml` aanwezig zijn, ook al is de gegenereerde sleutel er niet van afhankelijk.

#### Gebruik van de opdracht
```bash
digna crypt gen-key
```

#### Voorbeelduitvoer
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

De opdracht `crypt encrypt` versleutelt een tekenreeks (zoals een databasewachtwoord) met de AES-GCM-sleutel die in `config.toml` is geconfigureerd, en toont de versleutelde tekst.

#### Gebruik van de opdracht
```bash
digna crypt encrypt <VALUE>
```

#### Argumenten
- **VALUE**: De platte tekst die versleuteld moet worden (vereist).

#### Voorbeeld
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

De opdracht `crypt decrypt` ontsleutelt een met AES-GCM versleutelde tekenreeks met de sleutel die in `config.toml` is geconfigureerd, en toont de platte tekst.

#### Gebruik van de opdracht
```bash
digna crypt decrypt <VALUE>
```

#### Argumenten
- **VALUE**: De versleutelde tekenreeks die ontsleuteld moet worden (vereist).

#### Voorbeeld
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Gebruikersbeheer

---

### user add

De opdracht `user add` maakt een nieuw gebruikersaccount aan in de ***digna***-repository. De opdracht mislukt als er al een gebruiker met het opgegeven e-mailadres bestaat.

#### Gebruik van de opdracht
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenten
- **EMAIL**: Het e-mailadres van de gebruiker (vereist).
- **PASSWORD**: Het initiële wachtwoord van de gebruiker (vereist).
- **DISPLAY_NAME**: De volledige weergavenaam van de gebruiker (vereist).

#### Opties
- `--admin`, `-a`: Maakt de gebruiker aan met beheerdersrechten (superuser).

#### Voorbeeld
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Een beheerdersaccount aanmaken:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Voorbeelduitvoer
```text
User created with ID: 42
```

### user list

De opdracht `user list` toont alle geregistreerde gebruikers in tabelvorm met ID, e-mailadres, weergavenaam en beheerdersvlag.

#### Gebruik van de opdracht
```bash
digna user list
```

#### Voorbeelduitvoer
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

De opdracht `user modify` werkt de weergavenaam en de beheerdersrechten van een bestaand gebruikersaccount bij, geïdentificeerd op e-mailadres.

Zowel de weergavenaam als de beheerdersvlag worden altijd weggeschreven. `--admin` is een schakelaar, geen waarde: **wanneer u hem weglaat, worden de beheerdersrechten ingetrokken**, dus geef hem mee telkens wanneer de gebruiker die rechten moet behouden of krijgen.

#### Gebruik van de opdracht
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenten
- **EMAIL**: Het e-mailadres van de te wijzigen gebruiker (vereist).
- **DISPLAY_NAME**: De bijgewerkte weergavenaam (vereist).

#### Opties
- `--admin`, `-a`: Kent beheerdersrechten toe. Weglaten om ze in te trekken.
- `--valid-until`, `-v`: Wordt om compatibiliteitsredenen geaccepteerd, maar **momenteel niet toegepast**. Meegeven levert een waarschuwing op en verandert niets.

#### Voorbeeld
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Voorbeelduitvoer
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

De opdracht `user modify-pwd` werkt het wachtwoord van een bestaand gebruikersaccount bij.

#### Gebruik van de opdracht
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumenten
- **EMAIL**: Het e-mailadres van de gebruiker wiens wachtwoord bijgewerkt moet worden (vereist).
- **PASSWORD**: Het nieuwe wachtwoord (vereist).

#### Voorbeeld
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

De opdracht `user delete` verwijdert een gebruikersaccount uit het systeem.

#### Gebruik van de opdracht
```bash
digna user delete <EMAIL>
```

#### Argumenten
- **EMAIL**: Het e-mailadres van de te verwijderen gebruiker (vereist).

#### Voorbeeld
```bash
digna user delete jdoe@example.com
```

---

## Project- en gegevensbronbeheer

---

### project list

De opdracht `project list` toont alle beschikbare projecten in de repository, met hun ID, naam en beschrijving.

#### Gebruik van de opdracht
```bash
digna project list
```

#### Voorbeelduitvoer
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

De opdracht `project list-ds` toont alle gegevensbronnen die bij een bepaald project horen, met hun ID, naam, soort, schema en tabelnaam.

#### Gebruik van de opdracht
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarvan de gegevensbronnen getoond moeten worden (vereist). De naam moet exact overeenkomen.

#### Voorbeeld
```bash
digna project list-ds ProjectA
```

#### Voorbeelduitvoer
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

De opdracht `project export-ds` exporteert gegevensbronnen van een project naar een JSON-document.

Als noch `--table-name` noch `--table-id` wordt opgegeven, worden alle gegevensbronnen van het project geëxporteerd.

#### Gebruik van de opdracht
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waaruit gegevensbronnen geëxporteerd moeten worden (vereist).

#### Opties
- `--table-name`, `-n`: Namen van de te exporteren gegevensbronnen. Meerdere namen kunnen gescheiden door spaties worden opgegeven.
- `--table-id`, `-i`: ID's van de te exporteren gegevensbronnen. Meerdere ID's kunnen gescheiden door spaties worden opgegeven.
- `--exportfile`, `-f`: Pad waarnaar de geëxporteerde gegevensbronnen worden opgeslagen (standaard: `data_sources_export.json`).

#### Voorbeeld
Om alle gegevensbronnen uit `ProjectA` te exporteren:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Om specifieke tabellen te exporteren:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Voorbeelduitvoer
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

De opdracht `project import-ds` importeert gegevensbronnen uit een exportbestand in een doelproject en rapporteert per object wat er is aangemaakt, bijgewerkt of overgeslagen.

#### Gebruik van de opdracht
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenten
- **PROJECT_NAME**: Naam van het doelproject waarin geïmporteerd wordt (vereist).
- **EXPORT_FILE**: Pad naar het JSON-exportbestand (vereist).

#### Opties
- `--output-file`, `-o`: Bestand waarnaar het importrapport wordt geschreven. Zonder deze optie gaat het rapport naar stdout.
- `--output-format`, `-f`: Formaat van het importrapport — `table`, `json` of `csv` (standaard: `table`).

#### Voorbeeld
```bash
digna project import-ds ProjectB my_export.json
```

Om een machineleesbaar rapport vast te leggen:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Het rapport beslaat vier objectniveaus — gegevensbron, definitie van de gegevensset, attribuut en validatieregel — elk met de bijbehorende importactie, het resultaat, het resulterende object-ID en eventuele aanvullende informatie.

### project plan-import-ds

De opdracht `project plan-import-ds` toont een voorbeeld van een gegevensbronimport in een doelproject en laat zien welke objecten zouden worden aangemaakt, bijgewerkt of overgeslagen, zonder iets te wijzigen. Ze neemt hetzelfde exportbestand en dezelfde rapportageopties als [`project import-ds`](#project-import-ds), en voegt per gepland object een stapnummer toe.

#### Gebruik van de opdracht
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenten
- **PROJECT_NAME**: Naam van het doelproject (vereist).
- **EXPORT_FILE**: Pad naar het exportbestand (vereist).

#### Opties
- `--output-file`, `-o`: Bestand waarnaar het importplan wordt geschreven. Zonder deze optie gaat het plan naar stdout.
- `--output-format`, `-f`: Formaat van het importplan — `table`, `json` of `csv` (standaard: `table`).

#### Voorbeeld
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Inspectiebeheer

---

### inspection run

De opdracht `inspection run` maakt een inspectieverzoek aan voor een project en een datumbereik, en wacht er vervolgens — afhankelijk van de opgegeven opties — op, keert onmiddellijk terug of voert het uit binnen het eigen proces.

De drie uitvoeringsmodi zijn:

- **Standaard (geen vlag)**: het verzoek wordt in de wachtrij geplaatst voor de backend, en de CLI pollt het elke twee seconden en toont de voortgang van de taken totdat de inspectie een eindtoestand bereikt. Een draaiende `digna serve` is vereist, anders pikt niets het verzoek op.
- **`--async-mode`**: het verzoek wordt in de wachtrij geplaatst en het ID wordt onmiddellijk getoond. Gebruik [`inspection status`](#inspection-status) om het te volgen.
- **`--bypass-backend`**: de inspectie wordt door het CLI-proces zelf uitgevoerd en niet in de wachtrij geplaatst, zodat er geen draaiende server nodig is.

`--async-mode` en `--bypass-backend` sluiten elkaar uit.

In elke modus eindigt de opdracht met een afsluitcode die niet nul is als de inspectie niet succesvol is afgerond.

#### Gebruik van de opdracht
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het doelproject (vereist). De naam moet exact overeenkomen.
- **START_DATE**: Begindatum van het datumbereik in de notatie `YYYY-MM-DD` (vereist).
- **END_DATE**: Einddatum van het datumbereik in de notatie `YYYY-MM-DD` (vereist).

#### Opties
- `--table-name`: Beperkt de inspectie tot één gegevensbron van het project, opgegeven met de naam van die gegevensbron. Zonder deze optie worden alle gegevensbronnen van het project geïnspecteerd.
- `--async-mode`: Plaatst de inspectie in de wachtrij en toont het verzoek-ID in plaats van erop te wachten. Kan niet worden gecombineerd met `--bypass-backend`.
- `--bypass-backend`: Voert de inspectie rechtstreeks uit in het CLI-proces in plaats van ze in de wachtrij te plaatsen voor de backend. Kan niet worden gecombineerd met `--async-mode`.

#### Voorbeeld
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Om een asynchrone inspectie in te dienen:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Om één enkele gegevensbron te inspecteren:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Voorbeelduitvoer
Standaardmodus:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asynchrone modus:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

De opdracht `inspection status` vraagt de toestand en de taakvoortgang van een inspectieverzoek op aan de hand van het verzoek-ID.

#### Gebruik van de opdracht
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumenten
- **INSPECTION_REQUEST_ID**: Het numerieke ID van het inspectieverzoek (vereist).

#### Voorbeeld
```bash
digna inspection status 1024
```

#### Voorbeelduitvoer
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

De opdracht `inspection abort` vraagt de annulering aan van lopende of wachtende inspectieverzoeken. Ze legt voor elk betrokken verzoek een stopgebeurtenis vast; de backend handelt daarop, dus een afbreking is een verzoek om te stoppen en geen onmiddellijke beëindiging.

#### Gebruik van de opdracht
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumenten
- **INSPECTION_REQUEST_ID**: Het ID van het af te breken inspectieverzoek. Vereist tenzij `--killall` wordt opgegeven.

#### Opties
- `--killall`: Breekt alle momenteel lopende en wachtende inspectieverzoeken af. Heeft voorrang op een verzoek-ID dat er tegelijk mee wordt opgegeven.

#### Voorbeeld
Om een specifiek verzoek af te breken:
```bash
digna inspection abort 1024
```

Om alle actieve en in de wachtrij staande inspecties af te breken:
```bash
digna inspection abort --killall
```

#### Voorbeelduitvoer
`--killall` rapporteert wat het heeft gedaan; het afbreken van één enkel verzoek levert geen uitvoer op en meldt succes via de afsluitcode.
```text
All running and pending inspections have been aborted.
```

---

## Licentiebeheer

---

### license check

De opdracht `license check` valideert `license.toml`, verifieert de handtekening ervan aan de hand van de openbare sleutel die met de installatie wordt meegeleverd, en controleert of de licentie niet is verlopen. Ze leest geen applicatieconfiguratie, dus ze werkt ook voordat `config.toml` is ingesteld.

#### Gebruik van de opdracht
```bash
digna license check
```

#### Voorbeelduitvoer
```text
License is valid
```

Een ongeldige handtekening en een verlopen licentie worden als afzonderlijke fouten gerapporteerd, beide met afsluitcode 1.

---

## Server- en achtergrondservices

---

### serve

De opdracht `serve` start de ***digna*** REST API-server samen met de achtergrondplanner voor inspecties en de inspectiebeheerder. Bij het opstarten laat ze ook elke inspectie mislukken die de repository nog als lopend registreert, aangezien niets een eerder proces kan hebben overleefd.

De opdracht draait op de voorgrond totdat ze wordt gestopt.

#### Gebruik van de opdracht
```bash
digna serve [OPTIONS]
```

#### Opties
- `--address`: Netwerkadres waaraan de API-server wordt gebonden (standaard: `127.0.0.1`).
- `--port`: Poortnummer waarop geluisterd wordt (standaard: `8000`).

#### Voorbeeld
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Voorbeelduitvoer
```text
Server running on http://0.0.0.0:8000
```