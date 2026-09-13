---
title: Průvodce instalací pro Windows – digna Release 2026.06 | digna Dokumentace
description: Krok za krokem průvodce instalací digna Release 2026.06 na Windows — systémové požadavky, nastavení PostgreSQL, konfigurace webového serveru, konfigurace backendu a dashboardu, spuštění digna jako služby Windows a upgrade na nové vydání.
keywords: digna instalace windows, průvodce nasazením digna, nastavení digna backendu, instalace digna dashboardu, nastavení postgresql, digna služba windows, průvodce upgrade digna
image: /assets/logo_square.png
---

# Průvodce instalací pro Windows pro digna Release 2026.06

**Verze:** 2026.06

**Poslední aktualizace:** 30. srpna 2026


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

### Co je nového ve vydání 2026.06

Toto vydání přináší možnosti pozorovatelnosti dat přímo do vašeho kódu, což umožňuje vývojářům sledovat kvalitu dat u zdroje. Kompletní podrobnosti najdete v [release notes](http://docs.digna.ai/changelog/Release_202606/).

### Hledáte macOS nebo Linux?

Tento průvodce pokrývá Windows. Pro jiné platformy viz [macOS Installation Guide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) nebo [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — Konfigurační soubor
   - `license.toml` — Licenční soubor (sem zkopírujte váš soubor)

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

Tato sekce konfiguruje nastavení aplikačního backendu digna:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `digna_APP_HOST` | `localhost` nebo IP adresa | Hostname nebo IP, kde je nasazen dignabackend |
| `digna_APP_PORT` | `8082` (výchozí) | Port pro REST API endpointy |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontend | Pokud je dashboard na jiném serveru, přidejte jeho URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Požadováno pro CORS s credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Povolit všechny HTTP metody |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Povolit všechny hlavičky |

#### Sekce [repo]

Tato sekce konfiguruje připojení k PostgreSQL databázi:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `digna_REPO_HOST` | `localhost` nebo IP | Hostname/IP PostgreSQL serveru |
| `digna_REPO_PORT` | `5432` (výchozí) | Port PostgreSQL |
| `digna_REPO_DB` | `postgres` | Název databáze |
| `digna_REPO_SCHEMA` | `dignarepo` | Dříve vytvořené schéma |
| `digna_REPO_USER` | `digna_user` | Uživatel vytvořený v PostgreSQL |
| `digna_REPO_PASSWORD` | Vaše heslo | Heslo nastavené při vytváření uživatele |

#### Sekce [base]

Tato sekce obsahuje bezpečnostní a cookie nastavení:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Musí odpovídat doméně frontendu |
| `digna_COOKIE_SECURE` | `false` (lokálně) / `true` (produkce) | Pro HTTPS použijte `true` |
| `digna_COOKIE_HTTPONLY` | `true` | Vždy povoleno z bezpečnostních důvodů |
| `digna_COOKIE_SAME_SITE` | `lax` | Zabraňuje CSRF útokům |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 hodin) | Vypršení relace v sekundách |
| `digna_MAX_WORKERS` | Počet jader CPU - 1 | Počet paralelních inspekčních úloh |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Maximální zpoždění v sekundách, které může plánovač přidat před spuštěním splatné úlohy |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Denní čas (24hodinový formát `HH:MM`), kdy začíná denní úklid |

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` nebo `DEBUG` | `INFO` pro produkci, `DEBUG` pro ladění |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Počet denních záloh logů, které se uchovávají |

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

Overall: OK
```

Opravte vše, co je hlášeno jako FAILED, a před pokračováním příkaz spusťte znovu. Úplný seznam voleb najdete v [referenci CLI](../../../cli/Command_Line_Interface_202606.md).

### Krok 3: Inicializace repozitáře

1. Otevřete Příkazový řádek
2. Přejděte do instalačního adresáře digna (tam, kde jsou `config.toml` a spustitelný soubor `digna`)
3. Spusťte test připojení:

```bash
digna repo check
```

Měli byste obdržet potvrzení, že připojení bylo navázáno (repozitář samotný zatím nebyl inicializován).

### Krok 4: Instalace schématu repozitáře

Ve stejném adresáři spusťte:

```bash
digna repo install
```

Tento příkaz nainstaluje potřebné tabulky a schéma ve vaší PostgreSQL databázi.

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
- `--address` — Hostname/IP serveru
- `--port` — Port serveru 

Měli byste vidět úvodní zprávy potvrzující, že server běží:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "Server drží terminál"

    `serve` běží na popředí a pokračuje, dokud jej nezastavíte pomocí ++ctrl+c++. Nechte jej běžet, než dokončíte nastavení; pokud jej chcete místo toho spouštět automaticky při startu, viz [Spuštění digna jako služby Windows](#running-digna-as-a-windows-service).

## Konfigurace dashboardu {: #dashboard-configuration }

### Krok 1: Nasazení dashboardu na webový server

Dashboard digna má vlastní konfigurační soubor `config.toml` umístěný ve složce `dashboard/`. Tento konfigurační soubor je již poskytnut a během počátečního nastavení obvykle není nutné jej měnit. Pokud potřebujete přizpůsobit připojení na backend, upravte jej podle potřeby.

Pokud potřebujete upravit konfiguraci dashboardu (např. pro nasazení více instancí), nahlédněte do dokumentace dashboardu.

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

### Soubory pro správu služby

Všechny potřebné soubory se nacházejí v instalačním adresáři digna ve složce: `bin/`

Následující batch soubory jsou k dispozici:
- `install_service.bat` — Registruje digna jako službu Windows
- `uninstall_service.bat` — Odregistrovává službu
- `start_service.bat` — Spustí běžící službu
- `stop_service.bat` — Zastaví běžící službu

!!! warning "Vyžadováno oprávnění správce"

    Všechny batch soubory musí být spuštěny s oprávněními administrátora.

### Instalace služby

1. **Otevřete Příkazový řádek jako administrátor**
   - Klikněte pravým tlačítkem na Příkazový řádek
   - Vyberte "Spustit jako správce"

2. **Přejděte do složky bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Spusťte instalační skript**
   ```bash
   install_service.bat
   ```

Server digna je nyní registrován jako služba Windows s povoleným **automatickým spuštěním**. Služba se však nespustí okamžitě — viz následující sekci pro spuštění.

### Spuštění a zastavení služby

#### Pro spuštění služby

1. Otevřete Příkazový řádek jako administrátor
2. Přejděte do `digna\bin`
3. Spusťte:
   ```bash
   start_service.bat
   ```

#### Pro zastavení služby

1. Otevřete Příkazový řádek jako administrátor
2. Přejděte do `digna\bin`
3. Spusťte:
   ```bash
   stop_service.bat
   ```

!!! tip "Tip"

    Před aktualizací souborů aplikace vždy službu zastavte.

### Přesunutí služby do nového adresáře

Pokud je potřeba přesunout instalaci digna:

1. **Odinštalujte současnou službu**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Přesuňte soubory aplikace**
   - Přesuňte celý instalační adresář digna na nové místo

3. **Znovu nainstalujte službu**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Spusťte službu**
   ```bash
   start_service.bat
   ```

### Odinštalování služby

1. **Zastavte běžící službu**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Odinštalujte službu**
   ```bash
   uninstall_service.bat
   ```

Server digna je nyní odregistrován jako služba Windows.

---

## Upgrade na nové vydání {: #upgrading-to-a-new-release }

### Před upgradem

**Nejprve ověřte všechna databázová připojení**

Od verze 2026.06 přistupuje digna ke každé zdrojové technologii přes **ODBC**. Dřívější verze nabízely volbu mezi ovladačem specifickým pro danou technologii a ODBC, vybíranou přepínačem **Use ODBC**. Tým digna se rozhodl stavět výhradně na ODBC, protože jediné standardní rozhraní přináší více než sada ovladačů šitých na míru:

- **Ověřování** — ověřování je součástí ODBC, takže připojení může použít vše, co jeho ovladač podporuje: hesla, tokeny a PAT, Kerberos a Active Directory, MFA a jednotné přihlášení přes prohlížeč, cloudové identity, klientské certifikáty a TLS. Nové metody přicházejí s aktualizací ovladače, místo čekání na vydání digna.
- **Ovladače udržované výrobci databází** — vlastní ovladač výrobce sleduje nové verze serveru i bezpečnostní opravy a můžete jej aktualizovat podle svého harmonogramu, nezávisle na digna.
- **Jediný způsob konfigurace všeho** — každá technologie je seznam vlastností klíč/hodnota se stejným rozhraním, stejným šifrováním citlivých hodnot a stejným řešením potíží, místo odlišné sady polí pro každý zdroj.
- **Ladění a dosah** — volby ovladače jako časové limity, nastavení TLS, proxy a velikosti načítání jsou dostupné pro každý zdroj a připojit lze jakoukoli technologii s odpovídajícím ovladačem ODBC, včetně těch, pro které digna nevydává samostatnou příručku.

V praxi to znamená, že přepínač **Use ODBC** ani samostatná pole hostitele, portu, databáze, uživatele a hesla už neexistují. **Každé připojení, které ODBC dosud nepoužívá, musí být převedeno na ODBC** — automatický převod neexistuje, naplánujte si to tedy před upgradem:

1. Projděte každé databázové připojení definované ve vaší instalaci a poznamenejte si ta, která ODBC dosud nepoužívají — každé z nich bude třeba nakonfigurovat znovu.
2. Nainstalujte odpovídající ovladač ODBC na hostitele digna — připojení se otevírají ze serveru, na kterém běží backend digna, nikoli z prohlížeče. Viz [Instalace ovladače ODBC na hostitele digna](../../../databases/overview.md#install-the-driver).
3. Mějte připravené vlastnosti ODBC pro každé dotčené připojení. [Příručky k jednotlivým technologiím](../../../databases/overview.md#technology-guides) uvádějí pro každý zdroj ověřenou sadu vlastností.

Po upgradu převeďte každé dotčené připojení na ODBC a otestujte je z dashboardu — viz [Vytvoření databázového připojení](../../../databases/overview.md#create-a-database-connection) a [Testování připojení](../../../databases/overview.md#testing-a-connection).

!!! warning "Připojení Databricks Legacy"

    Konektor Databricks Legacy byl v této verzi odstraněn. Převeďte tato připojení na konektor [Databricks](../../../databases/databricks_connector_guide.md).

**Vytvoření zálohy repozitáře digna je povinné**

Před upgradem digna zálohujte svůj repozitář (PostgreSQL), abyste se ochránili před ztrátou dat.
Záloha zaručí, že v případě neočekávaných problémů s upgradem můžete obnovit data.

### Proces upgradu

#### Krok 1: Zastavte službu digna

Pokud běží digna jako služba Windows, nejprve ji zastavte:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Krok 2: Zálohujte stávající instalaci

V instalačním adresáři digna přejmenujte složky stávající instalace, aby vedle nich bylo možné nasadit novou verzi:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend a dignacli se již nepoužívají"

    Od verze 2026.06 jsou `dignabackend` a `dignacli` nahrazeny jediným spustitelným souborem `digna`, který spojuje backend a CLI. Složky `dignabackend_old` a `dignacli_old` si ponechte jen do doby, než upgrade ověříte — poté je můžete obě smazat. Složku `dashboard_old` si ponechte, dokud z ní neobnovíte své konfigurační soubory (viz krok 4).

#### Krok 3: Rozbalte a nasadte novou verzi

1. Rozbalte nový ZIP soubor s instalací digna
2. Zkopírujte nový spustitelný soubor `digna` a složku `dashboard` do vašeho instalačního adresáře


!!! warning "Důležité"

    Soubor `config.toml` **nikdy** není součástí instalačního ZIP. Vaše stávající konfigurace zůstane nedotčena.

#### Krok 4: Obnovení konfiguračních souborů

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "Verze 2026.06 mění soubor config.toml"

    Tři nastavení jsou nová a povinná, jedno se již nepoužívá. `config.toml` převzatý z dřívější verze nová nastavení neobsahuje a digna se nespustí, dokud budou chybět. Do stávajícího `config.toml` doplňte následující:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Přidejte dva klíče `[base]` do své stávající sekce `[base]` a přidejte `[encryption]` jako novou sekci. Poté z `[base]` **odstraňte `digna_FERNET_KEY`** — již se nepoužívá.

    Význam jednotlivých nastavení je popsán v části [Konfigurace backendu](#backend-configuration).

!!! warning "Jednotné přihlášení: formát [oidc_clients] se změnil"

    Verze 2026.06 nahrazuje pole tabulek jednou tabulkou pro každého poskytovatele, pojmenovanou podle klíče poskytovatele. `DIGNA_OIDC_KEY` mizí — klíč je nyní součástí záhlaví sekce.

    Před:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Po:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Sekci zopakujte pro každého poskytovatele a každý klíč udržujte shodný s `key` v souboru `dashboard_config.toml`. `digna config check` hlásí `oidc_clients` jako FAILED, dokud stará podoba zůstává. Týká se to pouze instalací, které používají jednotné přihlášení.

#### Krok 5: Ověřte konfiguraci

Než sáhnete na repozitář, ověřte, že je aktualizovaný `config.toml` úplný:

```bash
digna config check
```

Každá sekce musí hlásit OK. Opravte vše, co je hlášeno jako FAILED, a před pokračováním příkaz spusťte znovu.

#### Krok 6: Upgrade schématu repozitáře

Přejděte do instalačního adresáře digna a spusťte:

```bash
digna repo upgrade
```

Tím se aktualizuje PostgreSQL schéma na nejnovější verzi při zachování všech existujících dat.

#### Krok 7: Restart služeb

Pokud běží jako služba Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Pokud běží ručně, restartujte server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Pokud používáte IIS nebo Tomcat, restartujte příslušný webový server.

#### Krok 8: Ověření upgradu

1. Přistupte k dashboardu digna
2. Ověřte, že se rozhraní načítá správně
3. Zkontrolujte logy serveru, zda se nezobrazují chyby
4. Převeďte na ODBC každé připojení, které jej dosud nepoužívalo, a poté otestujte všechna připojení — viz [Testování připojení](../../../databases/overview.md#testing-a-connection)