# Referenční příručka digna CLI 2026.06
**2026-09-05**

Tato stránka dokumentuje úplnou sadu příkazů dostupných ve vydání ***digna*** CLI **2026.06**, včetně příkladů použití a voleb.

Spustitelný soubor se jmenuje `digna`.

---

## Základy CLI

---

### Přehled a syntaxe

CLI vydání **2026.06** používá strukturovanou hierarchii příkazů založenou na kategoriích:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

Příkazy `version` a `serve` jsou samostatné příkazy bez podpříkazu:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Globální volby

Následující globální volby platí pro všechny příkazy:

- `--help`, `-h`: Zobrazí nápovědu k CLI nebo ke konkrétní kategorii příkazů či podpříkazu.
- `--stacktrace`: Při selhání zobrazí celý řetězec chyb místo pouhé zprávy nejvyšší úrovně.

Volba `--stacktrace` je globální v úzkém slova smyslu: musí být uvedena **před** kategorií příkazu, nikoli za ní.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Přepínač `--version` neexistuje. Použijte místo něj příkaz [`version`](#version).

### Předpoklady

Většina příkazů potřebuje čitelný a platný soubor `config.toml`; některé navíc vyžadují platnou licenci.
Následující tabulka zaznamenává, co každá kategorie příkazů načte, než cokoli udělá:

| Kategorie příkazu | Potřebuje `config.toml` | Potřebuje platnou licenci |
|---|---|---|
| `version` | ne | ne |
| `config check` | ne (je právě tím, o čem příkaz podává zprávu) | ne |
| `license check` | ne | *je* tou kontrolou |
| `crypt` | ano | ne |
| `serve` | ano | ne |
| `project` | ano | ne |
| `user` | ano | ano |
| `inspection` | ano | ano |
| `repo` | ano | ano |

Tam, kde je licence vyžadována, se kontroluje jak její podpis, tak datum expirace, a pokud kterákoli z kontrol selže, příkaz se ukončí dříve, než se dotkne repozitáře.

### Návratové kódy

- `0`: příkaz uspěl.
- `1`: příkaz selhal. Chybová zpráva se zapisuje na stderr s předponou `Error: `.

### help

Volba `--help` poskytuje informace o dostupných kategoriích příkazů, podpříkazech a volbách:

1. **Zobrazení obecné nápovědy:**
   ```bash
   digna --help
   ```

2. **Získání nápovědy ke konkrétním kategoriím a příkazům:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Výstup obsahuje:**
   - **Popis příkazu:** Shrnutí účelu příkazu.
   - **Syntaxe:** Povinné a volitelné argumenty.
   - **Volby:** Přepínače a parametry specifické pro daný příkaz.

### version

Příkaz `version` vypíše nainstalované vydání ***digna***. Nenačítá žádnou konfiguraci ani neověřuje licenci, takže funguje i na instalaci, jejíž `config.toml` nebo licence chybí nebo je neplatná.

Verze vydání je nezávislá na verzi schématu repozitáře, kterou hlásí [`repo check`](#repo-check).

#### Použití příkazu
```bash
digna version
```

#### Ukázkový výstup
```text
2026.06
```

---

## Správa konfigurace

---

### config check

Příkaz `config check` ověřuje konfigurační soubor (`config.toml`) a kontroluje, zda jsou všechny povinné sekce a nastavení přítomné a správně naformátované. Každá sekce se ověřuje samostatně, takže poškozená sekce `[app]` nezakryje stav sekce `[repo]`.

Hlášené sekce jsou:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — volitelné; chybějící klíč projde, přítomný, ale chybně zapsaný seznam selže

Příkaz záměrně nenačítá konfiguraci aplikace stejným způsobem jako ostatní příkazy, aby dokázal diagnostikovat `config.toml`, který by ***digna*** vůbec zabránil ve spuštění.

#### Použití příkazu
```bash
digna config check [OPTIONS]
```

#### Volby
- `--configpath`, `-c`: Cesta ke konfiguračnímu souboru nebo k adresáři obsahujícímu `config.toml` (výchozí `./config.toml`).
- `--json`: Vypíše ověřovací zprávu ve formátu JSON. Má přednost před `--quiet`.
- `--quiet`, `-q`: Potlačí zprávu a spoléhá pouze na návratový kód.

#### Příklad
```bash
digna config check
```

Ověření konkrétního konfiguračního souboru a výstup ve formátu JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Ukázkový výstup
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

Chybějící soubor nebo syntaktická chyba v TOML nezanechá nic, co by šlo ověřovat sekci po sekci, a je hlášena jako jediná chyba místo zprávy, bez ohledu na `--quiet` či `--json`.

---

## Správa repozitáře

---

### repo check

Příkaz `repo check` otestuje připojení k databázi a ověří instalaci a verzi repozitáře. Selže, pokud nakonfigurované schéma neexistuje, nebo pokud existuje, ale neobsahuje žádný repozitář ***digna***.

Hlášená verze je verze schématu repozitáře, které je verzováno odděleně od vydání ***digna***, jež vypisuje [`version`](#version).

#### Použití příkazu
```bash
digna repo check
```

#### Ukázkový výstup
```text
Repo version 3.0.0 installed
```

### repo install

Příkaz `repo install` nainstaluje nový repozitář ***digna*** do schématu nakonfigurovaného v `config.toml` a vytvoří všechny potřebné sekvence, tabulky, indexy, omezení a počáteční záznamy.

Samotné schéma tento příkaz **nevytváří** — musí existovat předem. Příkaz se rovněž odmítne spustit, pokud je v daném schématu repozitář již nainstalován, a odkáže na [`repo upgrade`](#repo-upgrade), je-li nainstalovaná verze starší.

#### Použití příkazu
```bash
digna repo install
```

#### Ukázkový výstup
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Příkaz `repo upgrade` aplikuje migrace databázového schématu, aby povýšil existující repozitář na verzi očekávanou nainstalovaným vydáním. Povýšení se aplikují po jednom verzním kroku podél pevně dané cesty a každý dokončený krok se zaznamenává do repozitáře.

Pokud je repozitář již na očekávané verzi, příkaz oznámí, že povýšení není potřeba, a neprovede žádné změny.

#### Použití příkazu
```bash
digna repo upgrade
```

#### Ukázkový výstup
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Správa šifrování

---

### crypt gen-key

Příkaz `crypt gen-key` vygeneruje nový šifrovací klíč AES-GCM určený k použití jako šifrovací klíč v `config.toml`. Načitatelný soubor `config.toml` už musí existovat, přestože na něm vygenerovaný klíč nezávisí.

#### Použití příkazu
```bash
digna crypt gen-key
```

#### Ukázkový výstup
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Příkaz `crypt encrypt` zašifruje řetězec (například heslo k databázi) pomocí klíče AES-GCM nakonfigurovaného v `config.toml` a vypíše šifrový text.

#### Použití příkazu
```bash
digna crypt encrypt <VALUE>
```

#### Argumenty
- **VALUE**: Otevřený text, který se má zašifrovat (povinné).

#### Příklad
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Příkaz `crypt decrypt` dešifruje řetězec zašifrovaný algoritmem AES-GCM pomocí klíče nakonfigurovaného v `config.toml` a vypíše otevřený text.

#### Použití příkazu
```bash
digna crypt decrypt <VALUE>
```

#### Argumenty
- **VALUE**: Zašifrovaný řetězec, který se má dešifrovat (povinné).

#### Příklad
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Správa uživatelů

---

### user add

Příkaz `user add` vytvoří v repozitáři ***digna*** nový uživatelský účet. Příkaz selže, pokud uživatel se zadanou e-mailovou adresou již existuje.

#### Použití příkazu
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenty
- **EMAIL**: E-mailová adresa uživatele (povinné).
- **PASSWORD**: Počáteční heslo uživatele (povinné).
- **DISPLAY_NAME**: Celé zobrazované jméno uživatele (povinné).

#### Volby
- `--admin`, `-a`: Vytvoří uživatele s právy administrátora (superuživatele).

#### Příklad
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Vytvoření účtu administrátora:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Ukázkový výstup
```text
User created with ID: 42
```

### user list

Příkaz `user list` vypíše všechny registrované uživatele v tabulkové podobě s ID, e-mailem, zobrazovaným jménem a příznakem administrátora.

#### Použití příkazu
```bash
digna user list
```

#### Ukázkový výstup
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Příkaz `user modify` aktualizuje zobrazované jméno a práva administrátora u existujícího uživatelského účtu určeného e-mailovou adresou.

Zobrazované jméno i příznak administrátora se zapisují vždy oba. `--admin` je přepínač, nikoli hodnota: **jeho vynechání administrátorská práva odebere**, uvádějte jej tedy vždy, když si má uživatel práva ponechat nebo je získat.

#### Použití příkazu
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenty
- **EMAIL**: E-mail uživatele, který se má změnit (povinné).
- **DISPLAY_NAME**: Aktualizované zobrazované jméno (povinné).

#### Volby
- `--admin`, `-a`: Udělí práva administrátora. Vynechejte pro jejich odebrání.
- `--valid-until`, `-v`: Přijímán kvůli kompatibilitě, ale **aktuálně se neuplatňuje**. Jeho předání vypíše varování a nic nezmění.

#### Příklad
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Ukázkový výstup
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Příkaz `user modify-pwd` aktualizuje heslo existujícího uživatelského účtu.

#### Použití příkazu
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumenty
- **EMAIL**: E-mail uživatele, jehož heslo se má aktualizovat (povinné).
- **PASSWORD**: Nové heslo (povinné).

#### Příklad
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Příkaz `user delete` odstraní uživatelský účet ze systému.

#### Použití příkazu
```bash
digna user delete <EMAIL>
```

#### Argumenty
- **EMAIL**: E-mail uživatele, který se má smazat (povinné).

#### Příklad
```bash
digna user delete jdoe@example.com
```

---

## Správa projektů a zdrojů dat

---

### project list

Příkaz `project list` vypíše všechny projekty dostupné v repozitáři a zobrazí jejich ID, název a popis.

#### Použití příkazu
```bash
digna project list
```

#### Ukázkový výstup
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Příkaz `project list-ds` vypíše všechny zdroje dat přiřazené danému projektu a zobrazí jejich ID, název, druh, schéma a název tabulky.

#### Použití příkazu
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, jehož zdroje dat se mají vypsat (povinné). Název musí přesně odpovídat.

#### Příklad
```bash
digna project list-ds ProjectA
```

#### Ukázkový výstup
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Příkaz `project export-ds` exportuje zdroje dat z projektu do dokumentu JSON.

Pokud není zadáno ani `--table-name`, ani `--table-id`, exportují se všechny zdroje dat projektu.

#### Použití příkazu
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, ze kterého se mají zdroje dat exportovat (povinné).

#### Volby
- `--table-name`, `-n`: Názvy zdrojů dat k exportu. Více názvů lze zadat oddělených mezerami.
- `--table-id`, `-i`: ID zdrojů dat k exportu. Více ID lze zadat oddělených mezerami.
- `--exportfile`, `-f`: Cesta pro uložení exportovaných zdrojů dat (výchozí: `data_sources_export.json`).

#### Příklad
Export všech zdrojů dat z projektu `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Export konkrétních tabulek:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Ukázkový výstup
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Příkaz `project import-ds` importuje zdroje dat z exportního souboru do cílového projektu a u každého objektu hlásí, co bylo vytvořeno, aktualizováno nebo přeskočeno.

#### Použití příkazu
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenty
- **PROJECT_NAME**: Název cílového projektu, do kterého se importuje (povinné).
- **EXPORT_FILE**: Cesta k exportnímu souboru JSON (povinné).

#### Volby
- `--output-file`, `-o`: Soubor, do kterého se zapíše zpráva o importu. Bez něj jde zpráva na stdout.
- `--output-format`, `-f`: Formát zprávy o importu — `table`, `json` nebo `csv` (výchozí: `table`).

#### Příklad
```bash
digna project import-ds ProjectB my_export.json
```

Získání strojově čitelné zprávy:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Zpráva pokrývá čtyři úrovně objektů — zdroj dat, definici datové sady, atribut a validační pravidlo — u každé s importní akcí, výsledkem, ID výsledného objektu a případnými doplňujícími informacemi.

### project plan-import-ds

Příkaz `project plan-import-ds` zobrazí náhled importu zdrojů dat do cílového projektu a ukáže, které objekty by byly vytvořeny, aktualizovány nebo přeskočeny, aniž by cokoli změnil. Přijímá stejný exportní soubor a stejné volby výstupu jako [`project import-ds`](#project-import-ds) a přidává číslo kroku ke každému plánovanému objektu.

#### Použití příkazu
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenty
- **PROJECT_NAME**: Název cílového projektu (povinné).
- **EXPORT_FILE**: Cesta k exportnímu souboru (povinné).

#### Volby
- `--output-file`, `-o`: Soubor, do kterého se zapíše plán importu. Bez něj jde plán na stdout.
- `--output-format`, `-f`: Formát plánu importu — `table`, `json` nebo `csv` (výchozí: `table`).

#### Příklad
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Správa inspekcí

---

### inspection run

Příkaz `inspection run` vytvoří požadavek na inspekci pro projekt a rozsah dat a poté — podle zadaných voleb — buď na něj čeká, ihned se vrátí, nebo jej provede přímo ve vlastním procesu.

Tři režimy provádění jsou:

- **Výchozí (bez přepínače)**: požadavek se zařadí do fronty pro backend a CLI jej každé dvě sekundy dotazuje a vypisuje průběh úloh, dokud inspekce nedosáhne konečného stavu. Je nutné běžící `digna serve`, jinak požadavek nikdo nepřevezme.
- **`--async-mode`**: požadavek se zařadí do fronty a jeho ID se ihned vypíše. Pro sledování použijte [`inspection status`](#inspection-status).
- **`--bypass-backend`**: inspekci provede samotný proces CLI a do fronty se nezařazuje, takže není potřeba běžící server.

Volby `--async-mode` a `--bypass-backend` se vzájemně vylučují.

Ve všech režimech končí příkaz nenulovým návratovým kódem, pokud inspekce neproběhla úspěšně.

#### Použití příkazu
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumenty
- **PROJECT_NAME**: Název cílového projektu (povinné). Název musí přesně odpovídat.
- **START_DATE**: Počáteční datum rozsahu ve formátu `YYYY-MM-DD` (povinné).
- **END_DATE**: Koncové datum rozsahu ve formátu `YYYY-MM-DD` (povinné).

#### Volby
- `--table-name`: Omezí inspekci na jediný zdroj dat projektu zadaný jeho názvem. Bez této volby se kontrolují všechny zdroje dat projektu.
- `--async-mode`: Zařadí inspekci do fronty a vypíše ID požadavku místo čekání na dokončení. Nelze kombinovat s `--bypass-backend`.
- `--bypass-backend`: Provede inspekci přímo v procesu CLI místo zařazení do fronty pro backend. Nelze kombinovat s `--async-mode`.

#### Příklad
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Odeslání asynchronní inspekce:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Kontrola jediného zdroje dat:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Ukázkový výstup
Výchozí režim:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asynchronní režim:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Příkaz `inspection status` zjišťuje stav a průběh úloh požadavku na inspekci podle jeho ID.

#### Použití příkazu
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumenty
- **INSPECTION_REQUEST_ID**: Číselné ID požadavku na inspekci (povinné).

#### Příklad
```bash
digna inspection status 1024
```

#### Ukázkový výstup
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Příkaz `inspection abort` požaduje zrušení běžících nebo čekajících požadavků na inspekci. Pro každý dotčený požadavek zaznamená událost zastavení; jedná na jejím základě backend, takže přerušení je žádostí o zastavení, nikoli okamžitým ukončením.

#### Použití příkazu
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumenty
- **INSPECTION_REQUEST_ID**: ID požadavku na inspekci, který se má přerušit. Povinné, pokud není zadáno `--killall`.

#### Volby
- `--killall`: Přeruší všechny aktuálně běžící a čekající požadavky na inspekci. Má přednost před ID požadavku zadaným zároveň s ním.

#### Příklad
Přerušení konkrétního požadavku:
```bash
digna inspection abort 1024
```

Přerušení všech aktivních a zařazených inspekcí:
```bash
digna inspection abort --killall
```

#### Ukázkový výstup
`--killall` hlásí, co provedl; přerušení jediného požadavku nevypíše nic a úspěch hlásí návratovým kódem.
```text
All running and pending inspections have been aborted.
```

---

## Správa licencí

---

### license check

Příkaz `license check` ověřuje soubor `license.toml`, kontroluje jeho podpis proti veřejnému klíči dodanému s instalací a ověřuje, že licence nevypršela. Nenačítá žádnou konfiguraci aplikace, takže funguje i dříve, než je `config.toml` nastaven.

#### Použití příkazu
```bash
digna license check
```

#### Ukázkový výstup
```text
License is valid
```

Neplatný podpis a vypršelá licence jsou hlášeny jako dvě odlišné chyby, obě s návratovým kódem 1.

---

## Server a služby na pozadí

---

### serve

Příkaz `serve` spustí server REST API ***digna*** spolu s plánovačem inspekcí na pozadí a správcem inspekcí. Při startu rovněž označí za neúspěšnou každou inspekci, kterou repozitář stále eviduje jako běžící, protože z dřívějšího procesu nemohlo nic přežít.

Příkaz běží v popředí, dokud není zastaven.

#### Použití příkazu
```bash
digna serve [OPTIONS]
```

#### Volby
- `--address`: Síťová adresa, na kterou se má server API navázat (výchozí: `127.0.0.1`).
- `--port`: Číslo portu, na kterém se naslouchá (výchozí: `8000`).

#### Příklad
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Ukázkový výstup
```text
Server running on http://0.0.0.0:8000
```