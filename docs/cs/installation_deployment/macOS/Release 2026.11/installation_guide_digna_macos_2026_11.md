---
title: Průvodce instalací na macOS – digna Release 2026.11 | digna Dokumentace
description: Krok za krokem průvodce instalací digna Release 2026.11 na macOS — systémové požadavky, nastavení Homebrew a PostgreSQL, konfigurace nginx nebo Apache, konfigurace backendu a dashboardu, spuštění digna jako služby na pozadí a upgrade z Release 2026.06.
keywords: digna macos instalace, digna nasazení mac, nastavení digna backendu, instalace digna dashboardu, postgresql homebrew, nginx macos, digna launchd služba, digna průvodce upgradem
image: /assets/logo_square.png
---

# Průvodce instalací na macOS pro digna Release 2026.11

**Release:** 2026.11

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
9. [Spuštění digna jako služby na pozadí](#running-digna-as-a-background-service)
10. [Upgrade na novou verzi](#upgrading-to-a-new-release)

---

## Úvod {: #introduction }

### O digna

digna je komplexní platforma poháněná AI navržená k optimalizaci řízení kvality dat v různých datových prostředích jako datové sklady, datová jezera a lakehouse. Je navržena pro vysokou škálovatelnost a přizpůsobivost a řeší moderní problémy s daty pomocí automatizace, monitorování v reálném čase a detekce anomálií.

digna se skládá ze dvou hlavních komponent:

- **digna**: jádro aplikace, které zpracovává data a provádí kontroly kvality. Spojuje backend a rozhraní příkazového řádku do jediného spustitelného souboru a nahrazuje tak samostatné programy `dignabackend` a `dignacli` z předchozích verzí.
- **dignadashboard**: Webové rozhraní hostované na webovém serveru, poskytující uživatelsky přívětivé prostředí pro práci s platformou digna a vizualizaci metrik kvality dat.

### Co je nového ve verzi 2026.11

Toto vydání přináší digna Data Reconciliation, digna Agentic s digna MCP Server a digna Engine, který umí profilovat data přímo v digna a kontrolovat referenční integritu mezi různými databázovými technologiemi. Kompletní podrobnosti naleznete v [poznámkách k vydání](../../../changelog/Release_202611.md).

Pro instalaci toto vydání přináší nový mechanismus migrací repozitáře, volitelnou sekci `[duckdb]` v souboru `config.toml` pro digna Engine a nový licenční soubor. Všem se věnuje [sekce o upgradu](#upgrading-to-a-new-release).

### Hledáte Windows nebo Linux?

Tento průvodce pokrývá macOS. Pro jiné platformy viz [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) nebo [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Systémové požadavky {: #system-requirements }

Než začnete s instalací, ověřte, že váš systém splňuje následující minimální požadavky:

| Požadavek | Specifikace |
|---|---|
| **Operační systém** | macOS 13 (Ventura) nebo novější |
| **Architektura** | Apple Silicon (arm64) nebo Intel (x86_64) |
| **Paměť (minimální nasazení)** | 16 GB RAM |
| **Místo na disku** | 10 GB volného místa |
| **Databáze** | PostgreSQL Server 12 nebo vyšší |
| **Webový server** | nginx, Apache httpd nebo ekvivalent |
| **Nástroje příkazové řádky** | Xcode Command Line Tools (vyžadováno pro Homebrew) |

!!! info "digna Engine"

    Databázová připojení, která jako místo profilování používají digna Engine, se profilují přímo
    na hostiteli digna. Naplánujte pro ně dodatečnou paměť a místo na disku, viz
    [sekce \[duckdb\]](#duckdb-section).

### Možnosti instalace databáze

**Pokud je PostgreSQL již nainstalovaný:**
Můžete do existujícího PostgreSQL serveru přidat novou databázi pro digna.

**Pokud instalujete PostgreSQL na stejný stroj jako digna:**

!!! info "Doporučené specifikace"

    - **Paměť**: 32 GB RAM (místo 16 GB)
    - **Místo na disku**: 50 GB volného místa (místo 10 GB)

    Tyto vyšší specifikace umožňují současný provoz digna i PostgreSQL databáze.

### Kontrola architektury

Několik cest v tomto návodu se liší mezi Apple Silicon a Intel Macy. Pro zjištění spusťte v **Terminálu**:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew instaluje do `/opt/homebrew`.
- `x86_64` — Intel. Homebrew instaluje do `/usr/local`.

!!! tip "Tip"

    Místo tvrdého kódování jedné z cest tento průvodce používá `$(brew --prefix)`, který se rozbalí na správné umístění pro obě architektury. Můžete příkazy zkopírovat přesně tak, jak jsou.

---

## Předinstalační nastavení {: #pre-installation-setup }

Před instalací digna se ujistěte, že jsou splněny tři klíčové předpoklady:

1. **Homebrew** – správce balíčků používaný k instalaci komponent níže
2. **PostgreSQL Server** – pro ukládání vypočítaných metrik a výkonových dat
3. **Webový server** – pro hostování digna Dashboardu

Pokud tyto komponenty ještě nejsou nastaveny, postupujte podle níže uvedených sekcí pro jejich instalaci a konfiguraci.

### Instalace Homebrew

Homebrew je standardní správce balíčků pro macOS a je používán v celém tomto průvodci k instalaci PostgreSQL a nginx.

#### Krok 1: Zkontrolujte, zda je Homebrew již nainstalovaný

Otevřete **Terminál** (stiskněte `Cmd + Space`, napište `Terminal`, stiskněte Enter) a spusťte:

```bash
brew --version
```

Pokud se objeví číslo verze, přeskočte na sekci [Nastavení PostgreSQL serveru](#postgresql-server-setup).

#### Krok 2: Nainstalujte Homebrew

Pokud příkaz nebyl nalezen, nainstalujte Homebrew podle pokynů na [oficiálních stránkách Homebrew](https://brew.sh). Instalátor také nainstaluje Xcode Command Line Tools, pokud již nejsou přítomny.

#### Krok 3: Přidejte Homebrew do PATH

Na Apple Silicon vypíše instalátor dva příkazy pro přidání Homebrew do vašeho shellového prostředí. Spusťte je podle pokynů a pak ověřte:

```bash
brew --prefix
```

To by mělo vypsat `/opt/homebrew` na Apple Silicon nebo `/usr/local` na Intel.

---

## Nastavení PostgreSQL serveru {: #postgresql-server-setup }

### Pokud již máte PostgreSQL

Pokud je PostgreSQL již nainstalovaný a běžící na lokálním stroji nebo používáte spravovaný vzdálený PostgreSQL server, můžete přejít na [další sekci](#web-server-configuration).

### Možnosti instalace

macOS nabízí dvě jednoduché možnosti instalace PostgreSQL. Vyberte **jednu**:

- [Homebrew](#postgresql-homebrew) — instalace z příkazové řádky, doporučeno pro servery
- [Postgres.app](#postgresql-app) — grafická instalace, pohodlné pro lokální vyhodnocení

### Instalace PostgreSQL přes Homebrew {: #postgresql-homebrew }

#### Krok 1: Nainstalujte verzi PostgreSQL

```bash
brew install postgresql@16
```

#### Krok 2: Přidejte PostgreSQL do PATH

Verzované formule PostgreSQL jsou *keg-only*, což znamená, že Homebrew automaticky nelinkuje jejich příkazy do PATH. Přidejte je sami:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Poznámka"

    Toto předpokládá výchozí shell `zsh` používaný v macOS. Pokud používáte `bash`, přidejte stejný řádek do `~/.bash_profile`.

#### Krok 3: Spusťte službu PostgreSQL

```bash
brew services start postgresql@16
```

Tím se PostgreSQL spustí ihned a zároveň se nastaví, aby se spouštěl automaticky při přihlášení.

#### Krok 4: Ověřte instalaci

```bash
psql --version
```

Měli byste vidět verzi PostgreSQL, pokud byla instalace úspěšná.

#### Krok 5: Připojte se k serveru

```bash
psql postgres
```

!!! warning "Důležité — macOS se tady liší od Windows"

    Windows instalátor vás vyzve k vytvoření superuživatele `postgres` a k zadání hesla. Homebrew to nedělá. Místo toho vytvoří superuživatele pojmenovaného podle vašeho **macOS účtu**, bez hesla, přístupného pouze z lokálního stroje.

    To znamená, že na čerstvé Homebrew instalaci neexistuje role `postgres`. Při potřebě superuživatele použijte své vlastní jméno macOS účtu a vytvořte explicitního uživatele digna, jak je popsáno v sekci [Počáteční instalace](#initial-installation).

#### Krok 6: Potvrďte port

Výchozí port PostgreSQL je `5432`. Pro potvrzení, na jakém portu server naslouchá:

```bash
psql postgres -c "SHOW port;"
```

Zapamatujte si hodnotu — budete ji potřebovat při konfiguraci digna backendu.

### Instalace PostgreSQL pomocí Postgres.app {: #postgresql-app }

Pokud preferujete grafickou instalaci:

1. Stáhněte [Postgres.app](https://postgresapp.com) a přetáhněte jej do složky **Applications**
2. Otevřete aplikaci a klikněte na **Initialize** pro vytvoření nového serveru
3. Postupujte podle pokynů aplikace pro přidání jejích příkazových nástrojů do PATH
4. Ověřte instalaci:

```bash
psql --version
```

Postgres.app také vytvoří superuživatele pojmenovaného podle vašeho macOS účtu.

---

## Konfigurace webového serveru {: #web-server-configuration }

digna vyžaduje webový server pro hostování dashboardu. Vyberte jednu z následujících možností:

- [nginx](#nginx-setup) — instalovaný přes Homebrew, doporučeno
- [Apache httpd](#apache-setup) — součást macOS

Stačí nainstalovat a konfigurovat **jeden** z těchto serverů.

Obě sekce nastavují dvě věci, na kterých dashboard závisí:

- **Fallback pro single-page aplikaci**, aby obnovení URL dashboardu v prohlížeči nevracelo 404
- **MIME typ pro `.md`**, aby byly Markdown soubory servírovány správně

### Nastavení nginx {: #nginx-setup }

#### Přehled

nginx je lehký, výkonný webový server vhodný pro servírování statického digna dashboardu.

#### Instalace

```bash
brew install nginx
```

#### Spuštění nginx

```bash
brew services start nginx
```

#### Ověření instalace

1. Otevřete prohlížeč
2. Přejděte na `http://localhost:8080`
3. Měli byste vidět uvítací stránku nginx

!!! note "Poznámka — výchozí port je 8080, nikoli 80"

    Homebrew konfiguruje nginx tak, aby naslouchal na portu `8080`, aby mohl běžet bez oprávnění administrátora. Na macOS vyžaduje vázání na port `80` nebo jiný port pod 1024 práva root.

    Chcete-li servírovat dashboard na portu 80, změňte `listen 8080;` na `listen 80;` v níže uvedené konfiguraci a spusťte nginx pomocí `sudo brew services start nginx`.

#### Konfigurace webu pro dashboard

Konfigurace Homebrew nginx zahrnuje všechny soubory ve složce `servers`. Vytvořte věnovaný konfigurační soubor pro digna tam:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Vložte následující, nahraďte `/path/to/digna/dashboard` skutečnou cestou k rozbalené složce `dashboard`:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Důležité"

    Bez direktivy `try_files` při obnově jakékoli stránky dashboardu kromě kořenové URL dojde k 404. Toto je ekvivalent URL Rewrite modulu v IIS na Windows.

#### Aplikujte konfiguraci

Otestujte syntaxi konfigurace, pak reloadujte nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Nastavení Apache httpd {: #apache-setup }

#### Přehled

macOS obsahuje Apache httpd, takže instalace není nutná. Ve výchozím stavu je vypnutý.

#### Spuštění Apache

```bash
sudo apachectl start
```

#### Ověření instalace

1. Otevřete prohlížeč
2. Přejděte na `http://localhost`
3. Měli byste vidět hlášku "It works!"

#### Povinné: povolit mod_rewrite

Dashboard vyžaduje přepisování URL. Otevřete Apache konfiguraci:

```bash
sudo nano /etc/apache2/httpd.conf
```

Najděte následující řádek a odstraňte počáteční `#`, aby byl odkomentován:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Povinné: povolit .htaccess Overrides

Ve stejném souboru najděte blok `<Directory "/Library/WebServer/Documents">` a změňte:

```apache
AllowOverride None
```

na:

```apache
AllowOverride All
```

#### Povinné: MIME typ pro Markdown soubory

Stále v `httpd.conf` přidejte následující řádek, aby byly Markdown soubory servírovány správně:

```apache
AddType text/markdown .md
```

!!! warning "Důležité"

    Bez tohoto nastavení nemusí být `.md` soubory servírovány správně.

#### Aplikujte konfiguraci

Zkontrolujte konfiguraci na syntaktické chyby a restartujte Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Počáteční instalace {: #initial-installation }

### Krok 1: Nastavte repozitář digna

Repozitář digna uchovává všechny metriky vypočtené digna. Slouží jako centrální databáze pro analytická a výkonová data.

#### Vytvoření schématu a uživatele repozitáře

Otevřete svůj PostgreSQL klient (psql, pgAdmin nebo podobně) a spusťte následující SQL příkazy:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Nahraďte následující zástupné hodnoty:**

- `<digna_repo_schema>` — Vámi zvolené jméno schématu (např. `dignarepo`)
- `<digna_repo_user>` — Vámi zvolené uživatelské jméno (např. `digna_user`)
- `<digna_repo_password>` — Bezpečné heslo pro tohoto uživatele

**Příklad:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Pro spuštění z Terminálu v jednom kroku:

```bash
psql postgres
```

Poté vložte příkazy na promptu `postgres=#` a zadejte `\q` pro ukončení.

!!! tip "Doporučení"

    Používejte silná, složitá hesla pro databázové uživatele. Vyhněte se snadno odhadnutelným přihlašovacím údajům.

---

### Krok 2: Rozbalte instalační balík digna

1. Najděte ZIP soubor instalačního balíku digna, který jste obdrželi
2. Rozbalte jej do vámi zvoleného instalačního umístění — například `/opt/digna` nebo `~/digna`
3. Po rozbalení byste měli vidět následující položky:
   - `dashboard/` — webové rozhraní dashboardu
   - `digna` — hlavní spustitelný soubor (backend + CLI v jednom)

!!! info "Konfigurační a licenční soubory nejsou součástí balíku"

    Soubory `config.toml` ani `dashboard/dashboard_config.toml` nejsou součástí instalace — oba
    si vytvoříte sami, v částech [Konfigurace backendu](#backend-configuration) a
    [Konfigurace dashboardu](#dashboard-configuration). Ani `license.toml` není součástí
    balíku; digna jej dodává samostatně, jak popisuje krok 3.

Pro rozbalení z Terminálu:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Nastavte spustitelné oprávnění

V závislosti na způsobu přenosu může spustitelný bit po rozbalení chybět. Nastavte jej explicitně:

```bash
cd /opt/digna
chmod +x digna
```

#### Pokud macOS blokuje aplikaci

Soubory stažené přes prohlížeč nebo e-mailový klient jsou označeny karanténním atributem. Pokud macOS ohlásí, že aplikaci *"nelze otevřít, protože vývojáře nelze ověřit"*, odstraňte atribut z instalační složky:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativně otevřete **System Settings → Privacy & Security**, najděte zablokovanou položku u spodní části stránky a klikněte **Open Anyway**.

!!! note "Poznámka"

    Tento krok je nutný pouze pokud macOS skutečně zablokuje spustitelný soubor. Balíčky přenesené přes SSH nebo z interních sdílených úložišť obvykle nejsou v karanténě.

### Krok 3: Nainstalujte licenční soubor

!!! warning "Důležité"

    Licenční soubor není součástí instalačního balíku a bude vám poskytnut zvlášť společností digna.

1. Najděte soubor `license.toml`, který jste obdrželi
2. Zkopírujte jej do kořenového instalačního adresáře digna (tam, kde jsou `config.toml` a spustitelný soubor `digna`)

**Proč je to důležité:**
Licenční soubor obsahuje informace o zákazníkovi, datum vypršení licence a digitální podpis. **Neměňte tento soubor** — jakákoli úprava jej zneplatní.

**Struktura adresářů po nastavení:**

```
/opt/digna/
├── config.toml         (konfigurační soubor)
├── license.toml        (VÁŠ LICENČNÍ SOUBOR - zkopírujte sem)
├── digna               (hlavní spustitelný soubor)
├── bin/                (skripty pro správu služby)
└── dashboard/          (webové rozhraní)
    └── (soubory dashboardu)
```

---

## Konfigurace backendu {: #backend-configuration }

### Krok 1: Vytvořte a upravte konfigurační soubor

Soubor `config_template.toml` je dodán ve vaší instalační složce digna. Stačí jej přejmenovat na `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Umístění:** `/opt/digna/config.toml`

Otevřete `config.toml` v textovém editoru a nakonfigurujte každou sekci níže.

#### Sekce [app]

Tato sekce konfiguruje sdílení prostředků mezi různými původy (CORS) mezi dashboardem a backendem:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URL dashboardu | URL, ze kterých je dashboard servírován. Požadavky prohlížeče z jakéhokoli jiného původu jsou odmítnuty |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Povinné, aby prohlížeč s každým požadavkem odesílal cookie relace |

!!! note "Poznámka"

    Pokud servírujete dashboard z Homebrew nginx na jeho výchozím portu, origin, který je třeba povolit, je `http://localhost:8080`.

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

| Parameter | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` nebo IP | Hostname/IP PostgreSQL serveru |
| `DIGNA_REPO_PORT` | `5432` (výchozí) | Port PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Název databáze |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Dříve vytvořené schéma |
| `DIGNA_REPO_USER` | `digna_user` | Uživatel vytvořený v PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Vaše heslo | Heslo nastavené při tvorbě uživatele |
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

| Parameter | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_FERNET_KEY` | Hodnota uvedená výše | Klíč šifrování, které používaly dřívější verze. Musí být uveden; ponechte uvedenou hodnotu |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Hostitel, pod kterým je dashboard dostupný. `""` nenastavuje žádnou doménu, což je správné za proxy, která servíruje dashboard i backend pod jedním původem |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Musí být `true`, kdykoli je digna servírována přes HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Chrání cookie relace před přístupem skriptů |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 hodin) | Doba platnosti relace v sekundách |
| `DIGNA_MAX_WORKERS` | Počet CPU jader - 1 | Počet inspekcí, které mohou běžet současně |
| `DIGNA_FRONTEND_BASEURL` | URL dashboardu | Povinné. Používá se pro odkazy ve zprávách s upozorněními, proto musí jít o URL, kterou příjemci dokážou otevřít |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (výchozí) | Volitelné. Počet sekund, po které smí běžet jeden dotaz na zdrojovou databázi, než je přerušen; `0` časový limit vypíná |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (výchozí) | Volitelné. Počet sekund čekání na připojení ke zdrojové databázi; `0` čeká neomezeně dlouho |

!!! tip "Tip"

    Pro zjištění počtu CPU jader na vašem Macu spusťte `sysctl -n hw.ncpu`.

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

| Parameter | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` nebo `DEBUG` | `INFO` pro produkci, `DEBUG` pro ladění. Přijímány jsou také `TRACE`, `WARN` a `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (výchozí) | Volitelné. Adresář pro rotované soubory logů, relativně k pracovnímu adresáři |
| `DIGNA_LOGGING_MAX_FILES` | `30` (výchozí) | Volitelné. Počet rotovaných souborů logů, které se uchovávají |

#### Sekce [duckdb] (volitelná) {: #duckdb-section }

Novinka v Release 2026.11. Tato sekce nastavuje prostředky pro **digna Engine**, který profiluje
data přímo v digna u databázových připojení, jejichž místem profilování je **digna Engine**, a
spouští kontroly referenční integrity mezi zdroji dat na různých databázových připojeních. Viz
[Místo profilování](../../../platform/profiling/profiling_location.md).

Sekce je volitelná. Bez ní platí níže uvedené výchozí hodnoty.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (výchozí) | Paměť v MB, kterou smí použít jeden běh digna Engine. Současně může být aktivních až `DIGNA_MAX_WORKERS` běhů |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Výchozí: dočasný adresář systému (`$TMPDIR` účtu, pod kterým digna běží) | Adresář pro dočasné soubory, když se data nevejdou do paměti |

!!! tip "Dimenzování digna Engine"

    Počítejte na hostiteli digna s až `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` paměti
    navíc k tomu, co spotřebuje samotná digna, a s dostatkem volného místa na disku v dočasném
    adresáři, aby se do něj vešlo největší inspektované datum zdrojů dat, které používají digna Engine.
    Nasměrujte `DIGNA_DUCKDB_TEMP_DIRECTORY` na disk s takovým místem, do kterého smí zapisovat účet,
    pod kterým digna běží:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Tuto sekci potřebujete jen tehdy, když alespoň jedno databázové připojení používá digna Engine
    nebo když kontrola referenční integrity porovnává zdroje dat na různých připojeních.

---

### Krok 2: Ověřte konfiguraci

Před inicializací repozitáře ověřte, že je `config.toml` úplný a správně sestavený. V instalačním adresáři digna spusťte:

```bash
./digna config check
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

### Krok 3: Inicializujte repozitář

1. Otevřete **Terminál**
2. Přejděte do instalačního adresáře digna (kde jsou `config.toml` a spustitelný soubor `digna`)
3. Spusťte test připojení:

```bash
cd /opt/digna
./digna repo check
```

Na novém schématu se příkaz připojí a poté oznámí, že repozitář zatím není nainstalován:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

V tuto chvíli je to očekávaný výsledek: potvrzuje, že se digna dostane k PostgreSQL i ke schématu. Chyba připojení nebo ověření naopak ukazuje na sekci `[repo]` nebo na nastavení PostgreSQL.

!!! note "Poznámka"

    Na macOS nejsou příkazy v aktuálním adresáři na PATH, takže spustitelný soubor voláte jako `./digna` místo `digna`. Chcete-li používat kratší zápis všude, přidejte instalační složku do PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Krok 4: Nainstalujte schéma repozitáře

Ve stejném adresáři spusťte:

```bash
./digna repo upgrade
```

Tento příkaz nainstaluje potřebné tabulky do schématu repozitáře a skončí hlášením:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instaluje i upgraduje"

    Od Release 2026.11 příkaz `repo upgrade` nainstaluje nový repozitář a upgraduje stávající.
    `repo install` dál funguje jako jiný název téhož příkazu.

### Krok 5: Vytvořte administrátorského uživatele

1. Otevřete nové okno Terminálu
2. Přejděte do instalačního adresáře digna
3. Spusťte následující příkaz pro vytvoření admin uživatele:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Příklad:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Tím se vytvoří uživatel s e-mailovou adresou `admin@example.com` a plnými administrátorskými oprávněními.

!!! tip "Tip"

    Zabalte heslo do jednoduchých uvozovek. `zsh` zachází se znaky jako `!`, `$` a `*` speciálně, a neuváděné heslo je s těmito znaky nebude správně předáno.

!!! tip "Doporučení"

    Používejte silné heslo kombinující velká a malá písmena, čísla a speciální znaky.

---

### Krok 6: Spusťte digna server

V instalačním adresáři digna spusťte server:

```bash
./digna serve --address <host> --port <port>
```

Parametry:
- `--address` — hostname/IP serveru (výchozí `127.0.0.1`)
- `--port` — port serveru (výchozí `8000`)

Jakmile server běží, vypíše adresu, na které naslouchá:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tip"

    Při prvním spuštění vás macOS může požádat, zda chcete aplikaci povolit příchozí síťová připojení. Klikněte **Allow**, jinak dashboard nebude moci komunikovat s backendem.

!!! note "Server drží terminál"

    `serve` běží na popředí a pokračuje, dokud jej nezastavíte pomocí ++ctrl+c++. Nechte jej běžet, než dokončíte nastavení; pokud jej chcete místo toho spouštět automaticky při startu, viz [Spuštění digna jako služby na pozadí](#running-digna-as-a-background-service).

## Konfigurace dashboardu {: #dashboard-configuration }

### Krok 1: Nasazení dashboardu na webový server

Dashboard digna načítá svou vlastní konfiguraci ze souboru `dashboard/dashboard_config.toml`. Tento soubor není součástí instalace — vytvoříte jej ve složce `dashboard/` vedle souborů dashboardu.

Jeho obsah je popsán v části [Jednotné přihlášení (SSO)](../../../sso/overview.md), kde je soubor také potřeba: obsahuje možnosti přihlášení, které dashboard nabízí, a u nasazení s více instancemi také připojení k backendu.

Vyberte svůj webový server a postupujte podle odpovídajících kroků.

#### Nasazení na nginx

Pokud jste postupovali podle sekce [nginx Setup](#nginx-setup), server block již směřuje na vaši složku `dashboard` a žádné kopírování není potřeba.

1. **Potvrďte cestu**
   - Otevřete `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Ověřte, že `root` ukazuje na rozbalenou složku `dashboard`

2. **Ujistěte se, že složka je čitelná**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Reload nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Ověřte instalaci**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost:8080` (nebo na vaši nakonfigurovanou URL)
   - Měli byste vidět přihlašovací stránku digna dashboardu

#### Nasazení na Apache httpd

1. **Zkopírujte dashboard do document root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Přidejte Rewrite pravidla**

   Vytvořte soubor `.htaccess` ve deployed složce, aby se při obnovení v prohlížeči nezobrazovala 404:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Vložte následující:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Restartujte Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Přístup k dashboardu**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost/digna`
   - Měli byste vidět přihlašovací stránku digna dashboardu

---

## Spuštění digna jako služby na pozadí {: #running-digna-as-a-background-service }

### Proč spouštět digna jako službu?

Spuštění backendu digna jako služby na pozadí zajistí, že:

- Se automaticky spustí při startu stroje
- Běží na pozadí bez otevřeného okna Terminálu
- Automaticky se restartuje při pádu
- Lze jej spravovat přes `launchctl`, správce služeb macOS

### Soubory pro správu služby

Všechny potřebné soubory jsou umístěny v instalačním adresáři digna pod: `bin/`

Následující shell skripty jsou k dispozici:

- `install_service.sh` — zaregistruje digna v launchd
- `uninstall_service.sh` — odregistruje službu
- `start_service.sh` — spustí registrovanou službu
- `stop_service.sh` — zastaví běžící službu

!!! warning "Vyžadována práva administrátora"

    Všechny skripty musí být spuštěny s `sudo`, protože registrace služby, která se spouští při startu, zapisuje do `/Library/LaunchDaemons`.

### Nastavení spustitelnosti skriptů

Při rozbalení se spustitelný bit nemusí zachovat. Před prvním použitím:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Instalace služby

1. **Otevřete Terminál**

2. **Přejděte do složky bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Spusťte instalační skript**
   ```bash
   sudo ./install_service.sh
   ```

Digna server je nyní zaregistrován v launchd s povoleným **automatickým spuštěním**. Služba se tímto nezapne okamžitě — viz další sekci pro její spuštění.

### Spuštění a zastavení služby

#### Chcete-li službu spustit

1. Otevřete Terminál
2. Přejděte do `/opt/digna/bin`
3. Spusťte:
   ```bash
   sudo ./start_service.sh
   ```

#### Chcete-li službu zastavit

1. Otevřete Terminál
2. Přejděte do `/opt/digna/bin`
3. Spusťte:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tip"

    Vždy před aktualizací souborů aplikace službu zastavte.

### Ověření služby

Pro potvrzení, že je služba zaregistrovaná a běží:

```bash
sudo launchctl list | grep digna
```

Řádek začínající PIDem značí, že služba běží. `-` v prvním sloupci znamená, že je zaregistrovaná, ale zastavená.

### Přesunutí služby do nového adresáře

launchd ukládá absolutní cestu ke spustitelnému souboru, takže při přesunu instalace je nutné službu znovu zaregistrovat:

1. **Odinstalujte aktuální službu**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Přesuňte soubory aplikace**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Znovu nainstalujte službu**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Spusťte službu**
   ```bash
   sudo ./start_service.sh
   ```

### Odinstalování služby

1. **Zastavte běžící službu**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Odinstalujte službu**
   ```bash
   sudo ./uninstall_service.sh
   ```

Digna server je nyní odregistrován z launchd.

---

## Upgrade na novou verzi {: #upgrading-to-a-new-release }

Tato sekce popisuje upgrade instalace Release 2026.06 na Release 2026.11. Pokud je vaše
instalace starší, přečtěte si nejprve [Upgrade z verze starší než 2026.06](#upgrading-from-a-release-before-2026-06).

### Před upgradem

**Vytvoření zálohy repozitáře digna je povinné**

Před upgradem digna zálohujte svůj repozitář (PostgreSQL), abyste se ochránili proti ztrátě dat.
Záloha vám umožní obnovit data, pokud by během upgradu nastaly neočekávané problémy.

Pro vytvoření zálohy z Terminálu:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Vyžádání licenčního souboru pro Release 2026.11**

Release 2026.11 vyžaduje nový soubor `license.toml`. Vyžádejte si jej od týmu digna ještě před
zahájením a mějte jej připravený pro [krok 7](#step-7-replace-the-license-file).

### Upgrade z verze starší než 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 přinesl tři změny, které platí i tehdy, když starší instalaci upgradujete
přímo na 2026.11:

- **Pouze ODBC.** digna přistupuje ke každé zdrojové technologii přes ODBC. Každé databázové
  připojení, které ODBC dosud nepoužívá, musí být po upgradu převedeno na ODBC; automatický
  převod neexistuje. Předem nainstalujte ovladače ODBC na hostitele digna, viz
  [Instalace ovladače ODBC na hostitele digna](../../../databases/overview.md#install-the-driver),
  a mějte připravené vlastnosti každého připojení z
  [příruček k jednotlivým technologiím](../../../databases/overview.md#technology-guides). Konektor
  Databricks Legacy už neexistuje; převeďte tato připojení na konektor
  [Databricks](../../../databases/databricks_connector_guide.md).
- **Jeden spustitelný soubor.** `dignabackend` a `dignacli` jsou nahrazeny jediným spustitelným
  souborem `digna`, který spojuje backend a CLI.
- **config.toml.** Sekce `[encryption]` je povinná a `DIGNA_APP_HOST` a `DIGNA_APP_PORT` se již
  nenačítají: server si adresu a port bere z `digna serve`. Porovnejte svůj soubor s částí
  [Konfigurace backendu](#backend-configuration).

Následující kroky upozorňují na místa, kde starší instalace vyžaduje jiný postup. Upgrade
repozitáře v kroku 8 převede repozitář jakékoli dřívější verze přímo na 2026.11.

### Postup upgradu

#### Krok 1: Zastavte službu digna {: #step-1-stop-the-digna-service }

Pokud digna běží jako služba na pozadí, nejprve ji zastavte:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Pokud digna běží v popředí, stiskněte v jejím okně Terminálu ++ctrl+c++.

#### Krok 2: Zálohujte stávající instalaci {: #step-2-backup-current-installation }

V instalačním adresáři digna přejmenujte spustitelný soubor a složku dashboardu stávající
instalace, aby vedle nich bylo možné nasadit nové vydání:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Soubor `digna_old` si ponechte, dokud upgrade neověříte, a složku `dashboard_old`, dokud z ní
neobnovíte své konfigurační soubory (viz krok 4). Poté můžete obojí smazat.

!!! info "Upgrade z verze starší než 2026.06"

    Místo spustitelného souboru přejmenujte složky `dignabackend` a `dignacli`:
    `mv dignabackend dignabackend_old` a `mv dignacli dignacli_old`. Release 2026.11 nepoužívá žádnou z nich.

#### Krok 3: Rozbalte a nasaďte novou verzi {: #step-3-extract-and-deploy-new-version }

1. Rozbalte nový ZIP soubor s instalací digna
2. Zkopírujte nový spustitelný soubor `digna` a složku `dashboard` do instalačního adresáře
3. Obnovte příznak spustitelnosti a v případě potřeby odstraňte atribut karantény:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Důležité"

    Soubory `config.toml` ani `dashboard/dashboard_config.toml` nejsou nikdy součástí
    instalačního ZIP — tým digna žádný z nich nedodává. Vaše stávající konfigurace proto
    zůstane upgradem nedotčena a kopie v přejmenovaných složkách `*_old` jsou jediné,
    které máte.

#### Krok 4: Obnovte konfigurační soubory {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
`dashboard`, a poté stránku znovu načtěte s vynuceným obnovením (++cmd+shift+r++).

#### Krok 6: Ověřte konfiguraci {: #step-6-validate-the-configuration }

Než sáhnete na repozitář, ověřte, že je `config.toml` úplný:

```bash
./digna config check
```

Každá sekce musí hlásit OK. Opravte vše, co je hlášeno jako FAILED, odstraňte klíče uvedené
v části **Unknown keys** a před pokračováním příkaz spusťte znovu.

#### Krok 7: Nahraďte licenční soubor {: #step-7-replace-the-license-file }

Licenční soubor se obvykle přenáší z jednoho vydání do dalšího. Release 2026.11 je výjimkou:
přidává dva licencované moduly, digna Data Reconciliation a digna Agentic, a licence vydaná před
2026.11 je neobsahuje. Zkopírujte soubor `license.toml`, který vám tým digna poskytl pro
Release 2026.11, do instalačního adresáře a nahraďte jím ten starý:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Nenechávejte si předchozí licenci"

    S předchozí licencí se digna sice spustí, ale digna Data Reconciliation a digna MCP Server
    zůstanou vypnuté. Každý příkaz, který licenci kontroluje — `user`, `inspection`, `repo` — se
    při neúspěšné kontrole ukončí dříve, než se repozitáře dotkne. Než budete pokračovat, ověřte
    novou licenci:

    ```bash
    ./digna license check
    ```

#### Krok 8: Upgradujte schéma repozitáře {: #step-8-upgrade-the-repository-schema }

V instalačním adresáři digna spusťte:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 spravuje schéma repozitáře pomocí verzovaných migrací. První upgrade z dřívější
verze převede schéma na poslední verzi předchozího mechanismu, zaznamená ji jako svůj výchozí
bod a poté použije migrace Release 2026.11. Skončí hlášením:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Všechna existující data zůstanou zachována. Stav repozitáře můžete kdykoli zjistit příkazem
`./digna repo check`: vypíše poslední použitou migraci a všechny čekající.

!!! warning "digna se nespustí na zastaralém repozitáři"

    Od Release 2026.11 server odmítne start, dokud repozitář potřebuje upgrade, a oznámí to,
    například:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Spusťte `repo upgrade` dříve, než spustíte server nebo službu.

#### Krok 9: Restartujte služby {: #step-9-restart-services }

Pokud digna běží jako služba na pozadí:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Pokud digna spouštíte ručně, restartujte server:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Pokud používáte nginx nebo Apache, restartujte příslušný webový server:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Krok 10: Ověřte upgrade {: #step-10-verify-the-upgrade }

1. Ověřte vydání nového spustitelného souboru:

    ```bash
    ./digna version
    ```

    První řádek musí znít `Release: 2026.11`.

2. Otevřete dashboard digna a ověřte, že se rozhraní načítá správně.
3. Zkontrolujte výstup serveru a soubory v adresáři `logs`, zda neobsahují chyby.
4. Otestujte databázová připojení — viz
   [Testování připojení](../../../databases/overview.md#testing-a-connection). Po upgradu
   z verze starší než 2026.06 nejprve převeďte na ODBC každé připojení, které ODBC dosud
   nepoužívalo.

Jak začít s novými moduly, popisují stránky [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Připojení AI agenta](../../../platform/agentic/connect_ai_agent.md) pro digna MCP Server a
[Místo profilování](../../../platform/profiling/profiling_location.md) pro digna Engine.
