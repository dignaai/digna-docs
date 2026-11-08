# Průvodce instalací pro Windows pro digna Release 2026.11

**Verze:** 2026.11

**Poslední aktualizace:** 7. listopadu 2026


---

## Obsah

1. [Úvod](#introduction)
2. [Systémové požadavky](#system-requirements)
3. [Předinstalační nastavení](#pre-installation-setup)
4. [Nastavení PostgreSQL serveru](#postgresql-server-setup)
5. [Konfigurace webového serveru](#web-server-configuration)
6. [Počáteční instalace](#initial-installation)
7. [Konfigurace backendu](#backend-configuration)
8. [Konfigurace dashboardu](#dashboard-configuration)
9. [Spuštění digna jako služby Windows](#running-digna-as-a-windows-service)
10. [Upgrade na nové vydání](#upgrading-to-a-new-release)

---

## Úvod {: #introduction }

### O digna

digna je komplexní platforma řízená umělou inteligencí navržená pro optimalizaci správy kvality dat napříč různými datovými prostředími, jako jsou datové sklady, datová jezera a lakehousy. Je navržena tak, aby byla vysoce škálovatelná a přizpůsobitelná, a řeší moderní datové výzvy pomocí automatizace, monitoringu v reálném čase a detekce anomálií.

digna se skládá ze dvou hlavních komponent:

- **digna**: jádro aplikace, které zpracovává data a provádí kontroly kvality. Spojuje backend a rozhraní příkazového řádku do jediného spustitelného souboru a nahrazuje tak samostatné programy `dignabackend` a `dignacli` z předchozích verzí.
- **dignadashboard**: Webové rozhraní hostované na webovém serveru, které poskytuje uživatelsky přívětivý způsob interakce s platformou digna a vizualizace metrik kvality dat.

### Co je nového ve vydání 2026.11

Toto vydání přináší digna Data Reconciliation, digna Agentic s digna MCP Server a digna Engine, který umí profilovat data přímo v digna a kontrolovat referenční integritu mezi různými databázovými technologiemi. Kompletní podrobnosti naleznete v [poznámkách k vydání](../../../changelog/Release_202611.md).

Pro instalaci toto vydání přináší nový mechanismus migrací repozitáře, volitelnou sekci `[duckdb]` v souboru `config.toml` pro digna Engine a nový licenční soubor. Všem se věnuje [sekce o upgradu](#upgrading-to-a-new-release).

### Hledáte macOS nebo Linux?

Tento průvodce pokrývá Windows. Pro jiné platformy viz [macOS Installation Guide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) nebo [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Systémové požadavky {: #system-requirements }

Než začnete instalaci, ujistěte se, že váš systém splňuje následující minimální požadavky:

| Požadavek | Specifikace |
|---|---|
| **Operační systém** | Windows Server nebo Windows 10/11 |
| **Paměť (minimální konfigurace)** | 16 GB RAM |
| **Volné místo na disku** | 10 GB dostupného úložiště |
| **Databáze** | PostgreSQL Server 12 nebo vyšší |
| **Webový server** | IIS, Apache Tomcat nebo ekvivalent |

!!! info "digna Engine"

    Databázová připojení, která jako místo profilování používají digna Engine, se profilují přímo
    na hostiteli digna. Naplánujte pro ně dodatečnou paměť a místo na disku, viz
    [sekce \[duckdb\]](#duckdb-section).

### Možnosti instalace databáze

**Pokud je PostgreSQL již nainstalován:**
Můžete do stávajícího PostgreSQL serveru přidat novou databázi pro digna.

**Pokud instalujete PostgreSQL na stejný stroj jako digna:**

!!! info "Doporučené specifikace"

    - **Paměť**: 32 GB RAM (namísto 16 GB)
    - **Volné místo na disku**: 50 GB dostupného úložiště (namísto 10 GB)

    Tyto vyšší specifikace umožní současný provoz digna a PostgreSQL databáze.

---

## Předinstalační nastavení {: #pre-installation-setup }

Než nainstalujete digna, ujistěte se, že máte připraveny dvě klíčové předpoklady:

1. **PostgreSQL Server** – pro ukládání vypočtených metrik a výkonových dat
2. **Webový server** – pro hostování digna Dashboardu

Pokud tyto komponenty nejsou nastaveny, následujte níže uvedené sekce pro jejich instalaci a konfiguraci.

---

## Nastavení PostgreSQL serveru {: #postgresql-server-setup }

### Pokud už máte PostgreSQL

Pokud je PostgreSQL nainstalovaný a spuštěný na vašem lokálním stroji nebo pokud používáte spravovaný vzdálený PostgreSQL server, můžete přeskočit do [následující sekce](#web-server-configuration).

### Instalace PostgreSQL

Postupujte podle těchto kroků pro instalaci PostgreSQL na Windows:

#### Krok 1: Stažení PostgreSQL

1. Navštivte [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Vyberte **Windows**
3. Stáhněte si nejnovější instalační program

#### Krok 2: Spuštění instalátoru

1. Dvakrát klikněte na stažený instalační soubor
2. Postupujte podle pokynů v průvodci instalací

#### Krok 3: Volba instalačního adresáře

Zvolte adresář, kam bude PostgreSQL nainstalován. Výchozí umístění je obvykle vhodné.

#### Krok 4: Výběr komponent

Pro standardní instalaci ponechte výchozí volby komponent.

#### Krok 5: Nastavení hesla superuživatele PostgreSQL

Zadejte a potvrďte heslo pro superuživatele PostgreSQL (`postgres`). **Uložte toto heslo bezpečně** — budete ho později potřebovat.

#### Krok 6: Konfigurace portu

Výchozí port PostgreSQL je `5432`. Můžete použít výchozí nebo specifikovat jiný port podle potřeby.

!!! tip "Tip"

    Pokud je port 5432 již obsazen, zvolte alternativní port a poznamenejte si ho pro pozdější konfiguraci.

#### Krok 7: Volba locale

Vyberte locale pro vaši databázi. Výchozí nastavení je obvykle vhodné pro většinu instalací.

#### Krok 8: Dokončení instalace

Klikněte na **Next** v posledních krocích, poté klikněte na **Finish**.

#### Krok 9: Ověření instalace

Otevřete Příkazový řádek a ověřte, že je PostgreSQL nainstalován:

```bash
psql --version
```

Měli byste vidět verzi PostgreSQL, pokud byla instalace úspěšná.

---

## Konfigurace webového serveru {: #web-server-configuration }

digna vyžaduje webový server pro hostování dashboardu. Zvolte jednu z následujících možností:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Stačí nainstalovat a nakonfigurovat **jeden** z těchto serverů.

### Nastavení IIS {: #iis-setup }

#### Přehled

Internet Information Services (IIS) je Microsoftův webový server pro hostování webových stránek a webových aplikací.

#### Povolení IIS

1. **Otevřete Ovládací panely**
   - Stiskněte `Win + R`
   - Napište `control` a stiskněte Enter

2. **Přejděte na Windows Features**
   - Klikněte na **Programs**
   - Vyberte **Turn Windows features on or off**

3. **Povolte Internet Information Services**
   - Sjeďte dolů a najděte **Internet Information Services (IIS)**
   - Zaškrtněte políčko pro jeho povolení
   - Klikněte na **+** pro rozbalení a ověřte, že jsou vybrány tyto podkomponenty:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klikněte OK** pro použití změn

5. **Ověřte instalaci IIS**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost`
   - Měli byste vidět uvítací stránku IIS

#### Požadováno: URL Rewrite Module

IIS vyžaduje komponentu URL Rewrite. Stáhněte a nainstalujte ji z [oficiální Microsoft stránky](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Požadováno: MIME typ pro Markdown soubory

Aby byly Markdown soubory (`.md`) správně servírovány IIS:

1. Otevřete **IIS Manager** (stiskněte `Win + R`, napište `inetmgr`, stiskněte Enter)
2. Přejděte na **Your Site > MIME Types**
3. Klikněte **Add...**
4. Nakonfigurujte:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Důležité"

    Bez tohoto nastavení nemusí být soubory `.md` správně servírovány.

---

### Nastavení Apache Tomcat {: #apache-tomcat-setup }

#### Přehled

Apache Tomcat je open-source kontejner pro Java servlet a webový server.

#### Instalace

1. **Stáhněte Apache Tomcat**
   - Navštivte [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Stáhněte Windows ZIP distribuci

2. **Rozbalte archiv**
   - Rozbalte ZIP soubor do adresáře ve vašem systému
   - Příklad: `C:\Program Files\Apache Tomcat`

3. **Ověřte, že Tomcat běží**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost:8080`
   - Měli byste vidět uvítací stránku Apache Tomcat

!!! tip "Tip"

    Apache Tomcat se obvykle po instalaci spustí automaticky. Pokud ne, přejděte do složky `bin` a spusťte `startup.bat`.

---

## Počáteční instalace {: #initial-installation }

### Krok 1: Nastavení repozitáře digna

Repozitář digna ukládá všechny metriky vypočtené dignou. Funguje jako centrální databáze pro analytická a výkonová data.

#### Vytvoření schématu repozitáře a uživatele

Otevřete svůj PostgreSQL klient (pgAdmin, psql nebo podobně) a spusťte následující SQL příkazy:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Nahraďte následující zástupné hodnoty:**

- `<digna_repo_schema>` — Název schématu podle vašeho výběru (např. `dignarepo`)
- `<digna_repo_user>` — Uživatelské jméno podle vašeho výběru (např. `digna_user`)
- `<digna_repo_password>` — Silné heslo pro tohoto uživatele

**Příklad:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Doporučené postupy"

    Používejte silná, komplexní hesla pro databázové uživatele. Vyhněte se snadno uhodnutelným přihlašovacím údajům.

---

### Krok 2: Rozbalení instalačního balíčku digna

1. Najděte ZIP soubor s instalací digna, který vám byl poskytnut
2. Rozbalte ho do požadovaného instalačního umístění
3. Po rozbalení byste měli vidět následující položky:
   - `dashboard/` — Webové rozhraní dashboardu
   - `digna` — Hlavní spustitelný soubor (backend + CLI dohromady)

!!! info "Konfigurační a licenční soubory nejsou součástí balíčku"

    Soubory `config.toml` ani `dashboard/dashboard_config.toml` nejsou součástí instalace — oba
    si vytvoříte sami, v částech [Konfigurace backendu](#backend-configuration) a
    [Konfigurace dashboardu](#dashboard-configuration). Ani `license.toml` není součástí
    balíčku; digna jej dodává samostatně, jak popisuje krok 3.

### Krok 3: Instalace licenčního souboru

!!! warning "Důležité"

    Licenční soubor **není** součástí instalačního balíčku a bude vám dodán samostatně společností digna.

1. Najděte soubor `license.toml`, který vám byl poskytnut
2. Zkopírujte ho do kořenového instalačního adresáře digna (tam, kde jsou `config.toml` a spustitelný soubor `digna`)

**Proč je to důležité:**
Licenční soubor obsahuje informace o zákazníkovi, datum vypršení licence a digitální podpis. **Neměňte tento soubor** — jakákoli úprava ho zneplatní.

**Struktura adresářů po nastavení:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Konfigurace backendu {: #backend-configuration }

### Krok 1: Vytvoření a úprava konfiguračního souboru

Soubor `config_template.toml` je součástí instalačního adresáře digna. Stačí jej přejmenovat na `config.toml`.

**Umístění:** `digna_installation/config.toml`

Otevřete `config.toml` v textovém editoru a nakonfigurujte jednotlivé sekce níže.

#### Sekce [app]

Tato sekce konfiguruje sdílení prostředků mezi různými původy (CORS) mezi dashboardem a backendem:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URL dashboardu | URL, ze kterých je dashboard servírován. Požadavky prohlížeče z jakéhokoli jiného původu jsou odmítnuty |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Povinné, aby prohlížeč s každým požadavkem odesílal cookie relace |

!!! info "Sekce [app] je volitelná"

    Od Release 2026.11 lze oba klíče i celou sekci `[app]` vynechat. To je správné nastavení,
    když reverzní proxy servíruje dashboard i backend pod jedním původem: prohlížeč pak neposílá
    žádné požadavky mezi různými původy a ve výchozím stavu není žádný takový požadavek povolen.

#### Sekce [repo]

Tato sekce konfiguruje připojení k PostgreSQL databázi:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` nebo IP | Hostname/IP PostgreSQL serveru |
| `DIGNA_REPO_PORT` | `5432` (výchozí) | Port PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Název databáze |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Dříve vytvořené schéma |
| `DIGNA_REPO_USER` | `digna_user` | Uživatel vytvořený v PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Vaše heslo | Heslo nastavené při vytváření uživatele |
| `DIGNA_REPO_SSLMODE` | `prefer` (výchozí) | Volitelné. Režim SSL pro PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` nebo `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (výchozí) | Volitelné. Počet připojení, která digna udržuje otevřená k repozitáři |

#### Sekce [base]

Tato sekce obsahuje nastavení zabezpečení, cookie a inspekcí:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_FERNET_KEY` | Hodnota uvedená výše | Klíč šifrování, které používaly dřívější verze. Musí být uveden; ponechte uvedenou hodnotu |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Hostitel, pod kterým je dashboard dostupný. `""` nenastavuje žádnou doménu, což je správné za proxy, která servíruje dashboard i backend pod jedním původem |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Musí být `true`, kdykoli je digna servírována přes HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Chrání cookie relace před přístupem skriptů |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 hodin) | Vypršení relace v sekundách |
| `DIGNA_MAX_WORKERS` | Počet jader CPU - 1 | Počet inspekcí, které mohou běžet současně |
| `DIGNA_FRONTEND_BASEURL` | URL dashboardu | Povinné. Používá se pro odkazy ve zprávách s upozorněními, proto musí jít o URL, kterou příjemci dokážou otevřít |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (výchozí) | Volitelné. Počet sekund, po které smí běžet jeden dotaz na zdrojovou databázi, než je přerušen; `0` časový limit vypíná |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (výchozí) | Volitelné. Počet sekund čekání na připojení ke zdrojové databázi; `0` čeká neomezeně dlouho |

#### Sekce [encryption]

Tato sekce obsahuje klíč, kterým se šifrují citlivé hodnoty uložené v repozitáři. Je **povinná** — `config check` hlásí sekci `[encryption]` jako FAILED, pokud klíč chybí.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Klíč kódovaný v Base64 | Šifruje citlivé hodnoty uložené v repozitáři digna |

!!! warning "Chraňte soubor config.toml"

    Tento klíč je pevná hodnota, shodná ve všech instalacích digna, a právě on dešifruje citlivé hodnoty ve vašem repozitáři. Omezte přístup k `config.toml` na účet, pod kterým digna běží, držte soubor mimo správu verzí a sdílené disky a vynechte jej z každé zálohy uchovávané méně bezpečně než samotný repozitář.

#### Sekce [logging]

Tato sekce konfiguruje chování logování:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` nebo `DEBUG` | `INFO` pro produkci, `DEBUG` pro ladění. Přijímány jsou také `TRACE`, `WARN` a `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (výchozí) | Volitelné. Adresář pro rotované soubory logů, relativně k pracovnímu adresáři |
| `DIGNA_LOGGING_MAX_FILES` | `30` (výchozí) | Volitelné. Počet rotovaných souborů logů, které se uchovávají |

!!! warning "Při běhu jako služba ponechte adresář logů"

    Služba Windows nemá konzoli, takže soubory logů jsou jediným záznamem o tom, co služba dělá.
    Nenastavujte `DIGNA_LOGGING_DIR` na prázdný řetězec, který soubory logů vypíná.

#### Sekce [duckdb] (volitelná) {: #duckdb-section }

Novinka v Release 2026.11. Tato sekce nastavuje prostředky pro **digna Engine**, který profiluje
data přímo v digna u databázových připojení, jejichž místem profilování je **digna Engine**, a
spouští kontroly referenční integrity mezi zdroji dat na různých databázových připojeních. Viz
[Místo profilování](../../../platform/profiling/profiling_location.md).

Sekce je volitelná. Bez ní platí níže uvedené výchozí hodnoty.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (výchozí) | Paměť v MB, kterou smí použít jeden běh digna Engine. Současně může být aktivních až `DIGNA_MAX_WORKERS` běhů |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Výchozí: dočasný adresář účtu, pod kterým digna běží (`%TEMP%`) | Adresář pro dočasné soubory, když se data nevejdou do paměti |

!!! tip "Dimenzování digna Engine"

    Počítejte na hostiteli digna s až `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` paměti
    navíc k tomu, co spotřebuje samotná digna, a s dostatkem volného místa na disku v dočasném
    adresáři, aby se do něj vešlo největší inspektované datum zdrojů dat, které používají digna Engine.
    Nasměrujte `DIGNA_DUCKDB_TEMP_DIRECTORY` na disk s takovým místem, do kterého smí zapisovat účet,
    pod kterým digna běží:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Tuto sekci potřebujete jen tehdy, když alespoň jedno databázové připojení používá digna Engine
    nebo když kontrola referenční integrity porovnává zdroje dat na různých připojeních.

---

### Krok 2: Ověřte konfiguraci

Před inicializací repozitáře ověřte, že je `config.toml` úplný a správně sestavený. V instalačním adresáři digna spusťte:

```bash
digna config check
```

Každá sekce se ověřuje samostatně, takže jediná chyba nezakryje stav ostatních:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Opravte vše, co je hlášeno jako FAILED, a před pokračováním příkaz spusťte znovu. WARNING v části **Unknown keys** uvádí klíče v `config.toml`, které digna nečte; nemají žádný účinek, proto je odstraňte nebo opravte jejich zápis. Úplný seznam voleb najdete v [referenci CLI](../../../cli/Command_Line_Interface_202611.md).

### Krok 3: Inicializace repozitáře

1. Otevřete Příkazový řádek
2. Přejděte do instalačního adresáře digna (tam, kde jsou `config.toml` a spustitelný soubor `digna`)
3. Spusťte test připojení:

```bash
digna repo check
```

Na novém schématu se příkaz připojí a poté oznámí, že repozitář zatím není nainstalován:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

V tuto chvíli je to očekávaný výsledek: potvrzuje, že se digna dostane k PostgreSQL i ke schématu. Chyba připojení nebo ověření naopak ukazuje na sekci `[repo]` nebo na nastavení PostgreSQL.

### Krok 4: Instalace schématu repozitáře

Ve stejném adresáři spusťte:

```bash
digna repo upgrade
```

Tento příkaz nainstaluje potřebné tabulky do schématu repozitáře a skončí hlášením:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instaluje i upgraduje"

    Od Release 2026.11 příkaz `repo upgrade` nainstaluje nový repozitář a upgraduje stávající.
    `repo install` dál funguje jako jiný název téhož příkazu.

### Krok 5: Vytvoření administrátorského uživatele

1. Otevřete **nové** okno Příkazového řádku
2. Přejděte do instalačního adresáře digna
3. Spusťte následující příkaz pro vytvoření admin uživatele:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Příklad:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Tím vytvoříte uživatele s plnými administrátorskými právy.

!!! tip "Doporučené postupy"

    Používejte silné heslo kombinující velká a malá písmena, číslice a speciální znaky.

---

### Krok 6: Spuštění serveru digna

V instalačním adresáři digna spusťte server pomocí:

```bash
digna serve --address <host> --port <port>
```

**Parametry:**
- `--address` — Hostname/IP serveru (výchozí `127.0.0.1`)
- `--port` — Port serveru (výchozí `8000`)

Jakmile server běží, vypíše adresu, na které naslouchá:

```text
Server running on http://127.0.0.1:8082
```

!!! note "Server drží terminál"

    `serve` běží na popředí a pokračuje, dokud jej nezastavíte pomocí ++ctrl+c++. Nechte jej běžet, než dokončíte nastavení; pokud jej chcete místo toho spouštět automaticky při startu, viz [Spuštění digna jako služby Windows](#running-digna-as-a-windows-service).

## Konfigurace dashboardu {: #dashboard-configuration }

### Krok 1: Nasazení dashboardu na webový server

Dashboard digna načítá svou vlastní konfiguraci ze souboru `dashboard/dashboard_config.toml`. Tento soubor není součástí instalace — vytvoříte jej ve složce `dashboard/` vedle souborů dashboardu.

Jeho obsah je popsán v části [Jednotné přihlášení (SSO)](../../../sso/overview.md), kde je soubor také potřeba: obsahuje možnosti přihlášení, které dashboard nabízí, a u nasazení s více instancemi také připojení k backendu.

Zvolte svůj webový server a postupujte podle odpovídajících kroků nasazení.

#### Nasazení do IIS

1. **Otevřete IIS Manager**
   - Stiskněte `Win + R`, napište `inetmgr`, stiskněte Enter

2. **Vytvořte nový web**
   - V levém panelu klikněte pravým tlačítkem na **Sites**
   - Vyberte **Add Website...**

3. **Konfigurujte web**
   - **Site Name**: Zadejte název (např. "dignaDashboard")
   - **Physical Path**: Klikněte na Browse a vyberte složku `dashboard`
   - **Binding**: Nastavte IP adresu a port (výchozí port 80 pro HTTP, 443 pro HTTPS)

4. **Spusťte web**
   - Klikněte **OK** pro vytvoření webu
   - Klikněte pravým tlačítkem na nový web a vyberte **Start**

5. **Otestujte instalaci**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost` (nebo na vámi nakonfigurovanou URL)
   - Měli byste vidět přihlašovací stránku dashboardu digna

#### Nasazení do Apache Tomcat

1. **Zkopírujte dashboard do Tomcatu**
   - Zkopírujte složku `dashboard` do adresáře `webapps` ve vašem Tomcatu
   - Přejmenujte ji podle potřeby (např. na `digna`)
   - Příklad: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Ověřte nasazení**
   - Obnovte nebo znovu načtěte stránku správy Tomcatu (http://localhost:8080)
   - Měli byste vidět "digna" (nebo zvolené jméno) v seznamu nasazených aplikací

3. **Přístup k dashboardu**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost:8080/digna`
   - Měli byste vidět přihlašovací stránku dashboardu digna

---

## Spuštění digna jako služby Windows {: #running-digna-as-a-windows-service }

### Proč používat službu Windows?

Spuštění backendu digna jako služby Windows zajistí, že:
- se automaticky spustí při startu serveru
- poběží na pozadí bez otevřeného okna Příkazového řádku
- se automaticky restartuje v případě selhání
- lze ji spravovat přes správu služeb Windows

### Příkazy `windows`

Službu spravuje přímo spustitelný soubor `digna` prostřednictvím podpříkazů `digna windows`.
Nespouštějí se žádné batch soubory.

| Příkaz | Účel |
|---|---|
| `digna windows install` | Registruje digna jako službu Windows |
| `digna windows start` | Spustí registrovanou službu |
| `digna windows stop` | Zastaví běžící službu |
| `digna windows uninstall` | Odregistruje službu |

!!! warning "Vyžadováno oprávnění správce"

    Všechny čtyři příkazy musí být spuštěny z Příkazového řádku otevřeného jako správce.

Každý příkaz přijímá `--name` pro práci se službou registrovanou pod jiným než výchozím názvem.
Úplný seznam voleb je v [referenční příručce CLI](../../../cli/Command_Line_Interface_202611.md).

### Instalace služby

1. **Otevřete Příkazový řádek jako administrátor**
   - Klikněte pravým tlačítkem na Příkazový řádek
   - Vyberte "Spustit jako správce"

2. **Přejděte do instalačního adresáře digna**
   ```bash
   cd C:\path\to\digna
   ```

3. **Zaregistrujte službu**
   ```bash
   digna windows install
   ```

!!! important "Zadejte adresu a port, pokud vám nevyhovují výchozí hodnoty"

    `install` zaznamená adresu a port do registrace služby a služba se naváže přesně na to, co
    bylo zaznamenáno. Výchozí hodnoty jsou `127.0.0.1` a `8000`, které přijímají připojení
    pouze z tohoto počítače. Dashboard na jiném hostiteli se k nim nepřipojí, proto zadejte
    adresu, na které má backend naslouchat:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Tyto hodnoty se nenačítají z `config.toml`. Chcete-li je později změnit, službu
    odinstalujte a nainstalujte znovu s novými hodnotami.

Služba je registrována s **automatickým spuštěním**, takže se spustí spolu s Windows. Okamžitě
se však nespustí — viz následující sekci.

#### Volby instalace

| Volba | Výchozí hodnota | Účel |
|---|---|---|
| `--name` | `digna` | Název, pod kterým se služba registruje |
| `--display-name` | `digna` | Název zobrazený v services.msc |
| `--description` | `digna data quality backend` | Popis zobrazený v services.msc |
| `--address` | `127.0.0.1` | Adresa, na kterou služba naváže své API |
| `--port` | `8000` | Port, na který služba naváže své API |
| `--working-dir` | adresář spustitelného souboru `digna` | Adresář obsahující `config.toml` a `license.toml`, který služba použije jako svůj pracovní adresář |
| `--start-type` | `auto` | `auto` se spouští s Windows, `manual` se spouští jen na vyžádání, `disabled` službu zaregistruje, ale odmítne ji spustit |
| `--account` | `LocalSystem` | Účet, pod kterým služba běží, např. `DOMAIN\user` nebo `.\user` |
| `--password` | | Heslo účtu `--account` |

!!! tip "Spuštění pod doménovým účtem"

    `LocalSystem` nemá žádnou síťovou identitu, takže ověřování Windows vůči SQL Serveru
    i jakýkoli přístup ke sdílené síťové složce selže. Pokud služba potřebuje přistupovat
    k prostředkům jako konkrétní uživatel, nainstalujte ji s `--account` a `--password`.

### Spuštění a zastavení služby

#### Pro spuštění služby

```bash
digna windows start
```

#### Pro zastavení služby

```bash
digna windows stop
```

!!! tip "Tip"

    Před aktualizací souborů aplikace vždy službu zastavte.

### Přesunutí služby do nového adresáře

Pokud je potřeba přesunout instalaci digna:

1. **Zastavte a odregistrujte současnou službu**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Přesuňte soubory aplikace**
   - Přesuňte celý instalační adresář digna na nové místo

3. **Zaregistrujte službu znovu z nového umístění**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Zopakujte všechny hodnoty `--address`, `--port` nebo `--account`, které jste použili
   poprvé — předchozí registrace již neexistuje.

4. **Spusťte službu**
   ```bash
   digna windows start
   ```

### Odinštalování služby

1. **Zastavte běžící službu**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Odregistrujte službu**
   ```bash
   digna windows uninstall
   ```

Server digna je nyní odregistrován jako služba Windows.

---

## Upgrade na nové vydání {: #upgrading-to-a-new-release }

Tato část popisuje upgrade instalace z Release 2026.06 na Release 2026.11.

!!! warning "Upgrade z verze starší než 2026.06"

    Nejprve proveďte kroky upgradu na Release 2026.06: [Upgrade na nové vydání](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). Poté pokračujte následujícími kroky.

### Před upgradem

**Vytvoření zálohy repozitáře digna je povinné**

Před upgradem digna zálohujte svůj repozitář (PostgreSQL), abyste se ochránili proti ztrátě dat.
Záloha vám umožní obnovit data, pokud by během upgradu nastaly neočekávané problémy.

**Vyžádání licenčního souboru pro Release 2026.11**

Release 2026.11 vyžaduje nový soubor `license.toml`. Vyžádejte si jej od týmu digna ještě před
zahájením a mějte jej připravený pro [krok 7](#step-7-replace-the-license-file).

### Proces upgradu

#### Krok 1: Zastavte službu digna {: #step-1-stop-the-digna-service }

Otevřete Příkazový řádek jako správce a zastavte službu pomocí spustitelného souboru `digna`
vaší stávající instalace:

```bash
cd C:\path\to\digna
digna windows stop
```

Služba zůstane zaregistrovaná. Nový spustitelný soubor nahradí ten starý ve stejném adresáři,
takže registrace bude dál odkazovat na správný soubor.

Pokud digna běží v popředí, stiskněte v jejím okně Příkazového řádku ++ctrl+c++.

#### Krok 2: Zálohujte stávající instalaci {: #step-2-backup-current-installation }

V instalačním adresáři digna přejmenujte spustitelný soubor a složku dashboardu stávající
instalace, aby vedle nich bylo možné nasadit nové vydání:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Soubor `digna_old.exe` si ponechte, dokud upgrade neověříte, a složku `dashboard_old`, dokud z ní
neobnovíte své konfigurační soubory (viz krok 4). Poté můžete obojí smazat.

#### Krok 3: Rozbalte a nasaďte novou verzi {: #step-3-extract-and-deploy-new-version }

1. Rozbalte nový ZIP soubor s instalací digna
2. Zkopírujte nový spustitelný soubor `digna` a složku `dashboard` do instalačního adresáře

!!! warning "Důležité"

    Soubory `config.toml` ani `dashboard/dashboard_config.toml` nejsou nikdy součástí
    instalačního ZIP — tým digna žádný z nich nedodává. Vaše stávající konfigurace proto
    zůstane upgradem nedotčena a kopie v přejmenovaných složkách `*_old` jsou jediné,
    které máte.

#### Krok 4: Obnovte konfigurační soubory {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

Release 2026.11 nevyžaduje žádnou změnu v `config.toml`: soubor, který funguje s Release 2026.06,
funguje i nadále. Dvě změny jsou volitelné:

- Přidejte [sekci `[duckdb]`](#duckdb-section), pokud mají databázová připojení používat digna Engine
  a jeho výchozí hodnoty vašemu hostiteli nevyhovují.
- Vynechte sekci `[app]`, pokud reverzní proxy servíruje dashboard i backend pod jedním
  původem.

!!! warning "Nastavení, která digna nečte"

    Dřívější verze tohoto průvodce uváděly některá nastavení, která digna nečte. Nemají žádný
    účinek a `config check` je v kroku 6 vypisuje v části **Unknown keys**. Odstraňte je nebo
    je opravte:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` a
      `digna_LOGGING_BACKUP_COUNT` neexistují. Odstraňte je.
    - V názvech nastavení se rozlišují velká a malá písmena. digna čte `DIGNA_REPO_HOST`, nikoli
      `digna_REPO_HOST`. Pište všechny názvy velkými písmeny, jako v části
      [Konfigurace backendu](#backend-configuration).

!!! warning "Jednotné přihlášení: ponechte [[oidc_clients]]"

    digna čte poskytovatele jednotného přihlášení jako seznam položek `[[oidc_clients]]`, z nichž
    každá má vlastní `DIGNA_OIDC_KEY`. Pokud jste své poskytovatele změnili na sekce
    `[oidc_clients.<key>]`, jak uváděla dřívější verze tohoto průvodce, vraťte je zpět.
    `config check` hlásí `OIDC config(s)` jako FAILED, dokud je tato podoba použita:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Položku zopakujte pro každého poskytovatele a každý `DIGNA_OIDC_KEY` udržujte shodný s `key`
    v souboru `dashboard_config.toml`. Týká se to pouze instalací, které používají jednotné
    přihlášení.

#### Krok 5: Znovu načtěte webový server {: #step-5-reload-the-web-server }

Dashboard je sada statických souborů, takže váš webový server — i prohlížeč — může stále
servírovat předchozí verzi. Znovu načtěte nebo restartujte webový server, který hostuje složku
`dashboard`, a poté stránku znovu načtěte s vynuceným obnovením (++ctrl+f5++).

#### Krok 6: Ověřte konfiguraci {: #step-6-validate-the-configuration }

Než sáhnete na repozitář, ověřte, že je `config.toml` úplný:

```bash
digna config check
```

Každá sekce musí hlásit OK. Opravte vše, co je hlášeno jako FAILED, odstraňte klíče uvedené
v části **Unknown keys** a před pokračováním příkaz spusťte znovu.

#### Krok 7: Nahraďte licenční soubor {: #step-7-replace-the-license-file }

Licenční soubor vydaný pro dřívější vydání s Release 2026.11 nefunguje. Zkopírujte soubor
`license.toml`, který vám tým digna poskytl pro Release 2026.11, do instalačního adresáře a nahraďte
jím ten starý:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Nenechávejte si předchozí licenci"

    S předchozí licencí selže každý příkaz, který licenci kontroluje — `serve`, `user`,
    `inspection`, `repo` —, takže se digna nespustí a repozitář nelze upgradovat. Než budete
    pokračovat, ověřte novou licenci:

    ```bash
    digna license check
    ```

#### Krok 8: Upgradujte schéma repozitáře {: #step-8-upgrade-the-repository-schema }

V instalačním adresáři digna spusťte:

```bash
digna repo upgrade
```

Release 2026.11 spravuje schéma repozitáře pomocí verzovaných migrací. První upgrade z dřívější
verze převede schéma na poslední verzi předchozího mechanismu, zaznamená ji jako svůj výchozí
bod a poté použije migrace Release 2026.11. Skončí hlášením:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Všechna existující data zůstanou zachována. Stav repozitáře můžete kdykoli zjistit příkazem
`digna repo check`: vypíše poslední použitou migraci a všechny čekající.

!!! warning "digna se nespustí na zastaralém repozitáři"

    Od Release 2026.11 server odmítne start, dokud repozitář potřebuje upgrade, a oznámí to,
    například:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Spusťte `repo upgrade` dříve, než spustíte server nebo službu.

#### Krok 9: Restartujte služby {: #step-9-restart-services }

Pokud digna běží jako služba Windows, znovu ji spusťte:

```bash
cd C:\path\to\digna
digna windows start
```

Pokud digna spouštíte ručně, restartujte server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Pokud používáte IIS nebo Tomcat, restartujte příslušný webový server.

#### Krok 10: Ověřte upgrade {: #step-10-verify-the-upgrade }

1. Ověřte vydání nového spustitelného souboru:

    ```bash
    digna version
    ```

    První řádek musí znít `Release: 2026.11`.

2. Otevřete dashboard digna a ověřte, že se rozhraní načítá správně.
3. Zkontrolujte soubory v adresáři `logs` instalace, zda neobsahují chyby.
4. Otestujte databázová připojení — viz
   [Testování připojení](../../../databases/overview.md#testing-a-connection).

Jak začít s novými moduly, popisují stránky [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Připojení AI agenta](../../../platform/agentic/connect_ai_agent.md) pro digna MCP Server a
[Místo profilování](../../../platform/profiling/profiling_location.md) pro digna Engine.