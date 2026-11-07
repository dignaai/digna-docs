# Průvodce instalací na Linuxu pro digna Release 2026.11

**Release:** 2026.11

**Poslední aktualizace:** 7. listopadu 2026


---

## Obsah

1. [Úvod](#introduction)
2. [Systémové požadavky](#system-requirements)
3. [Předinstalační příprava](#pre-installation-setup)
4. [Nastavení PostgreSQL serveru](#postgresql-server-setup)
5. [Konfigurace webového serveru](#web-server-configuration)
6. [Počáteční instalace](#initial-installation)
7. [Konfigurace backendu](#backend-configuration)
8. [Konfigurace dashboardu](#dashboard-configuration)
9. [Spuštění digna jako systemd služby](#running-digna-as-a-systemd-service)
10. [Aktualizace na nové vydání](#upgrading-to-a-new-release)

---

## Úvod {: #introduction }

### O digna

digna je komplexní platforma řízená umělou inteligencí navržená pro optimalizaci správy kvality dat napříč různými datovými prostředími, jako jsou datové sklady, datová jezera a lakehousy. Je postavena tak, aby byla vysoce škálovatelná a přizpůsobitelná, a řeší moderní datové výzvy prostřednictvím automatizace, monitoringu v reálném čase a detekce anomálií.

digna se skládá ze dvou hlavních částí:

- **digna**: jádro aplikace, které zpracovává data a provádí kontroly kvality. Spojuje backend a rozhraní příkazového řádku do jediného spustitelného souboru a nahrazuje tak samostatné programy `dignabackend` a `dignacli` z předchozích verzí.
- **dignadashboard**: Webové rozhraní hostované na webovém serveru, které poskytuje uživatelsky přívětivé rozhraní pro práci s platformou digna a vizualizaci metrik kvality dat.

### Co je nového ve vydání 2026.11

Toto vydání přináší digna Data Reconciliation, digna Agentic s digna MCP Server a digna Engine, který umí profilovat data přímo v digna a kontrolovat referenční integritu mezi různými databázovými technologiemi. Kompletní podrobnosti naleznete v [poznámkách k vydání](../../../changelog/Release_202611.md).

Pro instalaci toto vydání přináší nový mechanismus migrací repozitáře, volitelnou sekci `[duckdb]` v souboru `config.toml` pro digna Engine a nový licenční soubor. Všem se věnuje [sekce o upgradu](#upgrading-to-a-new-release).

### Hledáte Windows nebo macOS?

Tento průvodce pokrývá Linux. Pro jiné platformy viz [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) nebo [macOS Installation Guide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Pro které distribuce je tento průvodce určen?

Instrukce jsou psány pro dva nejběžnější rodiny serverových distribucí. Kde se liší, jsou uvedeny oba příkazy:

- **Rodina Debian** — Debian, Ubuntu. Správce balíčků: `apt`.
- **Rodina RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Správce balíčků: `dnf`.

Jakákoli moderní distribuce s `systemd` bude fungovat; mění se pouze názvy balíčků a několik konfiguračních cest.

---

## Systémové požadavky {: #system-requirements }

Než začnete s instalací, ujistěte se, že váš systém splňuje následující minimální požadavky:

| Požadavek | Specifikace |
|---|---|
| **Operační systém** | Ubuntu 22.04 LTS nebo novější, Debian 12 nebo novější, RHEL 9 / Rocky 9 / AlmaLinux 9 nebo novější |
| **Architektura** | x86_64 (amd64) nebo arm64 |
| **Init systém** | systemd |
| **Paměť (minimální nasazení)** | 16 GB RAM |
| **Místo na disku** | 10 GB dostupného úložiště |
| **Databáze** | PostgreSQL Server 12 nebo vyšší |
| **Webový server** | nginx, Apache httpd nebo ekvivalent |

!!! info "digna Engine"

    Databázová připojení, která jako místo profilování používají digna Engine, se profilují přímo
    na hostiteli digna. Naplánujte pro ně dodatečnou paměť a místo na disku, viz
    [sekce \[duckdb\]](#duckdb-section).

### Možnosti instalace databáze

**Pokud je PostgreSQL již nainstalováno:**
Do stávajícího PostgreSQL serveru můžete přidat novou databázi pro digna.

**Pokud instalujete PostgreSQL na stejném stroji jako digna:**

!!! info "Doporučené specifikace"

    - **Paměť**: 32 GB RAM (namísto 16 GB)
    - **Místo na disku**: 50 GB dostupného úložiště (namísto 10 GB)

    Tyto vyšší specifikace jsou vhodné, pokud na stejném stroji běží současně digna a PostgreSQL databáze.

### Kontrola distribuce a architektury

Některé příkazy v tomto průvodci se liší mezi rodinami Debian a RHEL. Pro kontrolu spusťte:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` nebo `ID=debian` — použijte příkazy `apt`.
- `ID=rhel`, `rocky`, `almalinux` nebo `fedora` — použijte příkazy `dnf`.
- `x86_64` nebo `aarch64` — architektura instalačního balíčku, který potřebujete.

---

## Předinstalační příprava {: #pre-installation-setup }

Před instalací digna se ujistěte, že jsou splněny dvě klíčové předpoklady:

1. **PostgreSQL Server** – pro ukládání vypočtených metrik a výkonových dat
2. **Webový server** – pro hostování digna Dashboardu

Pokud tyto komponenty ještě nejsou nastaveny, postupujte podle níže uvedených sekcí pro jejich instalaci a konfiguraci.

### Aktualizace indexu balíčků

Aktualizujte seznamy balíčků před instalací:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Poznámka"

    V celém tomto průvodci je první příkaz v páru určen pro **rodinu Debian** a druhý pro **rodinu RHEL**. Spusťte pouze ten, který odpovídá vašemu systému.

---

## Nastavení PostgreSQL serveru {: #postgresql-server-setup }

### Pokud PostgreSQL již máte

Pokud je PostgreSQL již nainstalované a běží na místním stroji nebo používáte spravovaný vzdálený PostgreSQL server, můžete přejít na [další sekci](#web-server-configuration).

### Instalace PostgreSQL

#### Krok 1: Nainstalujte balíček serveru

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Tip"

    Balíčky v distribucích mohou zaostávat za aktuálním vydáním PostgreSQL. Pokud potřebujete konkrétní novější verzi, použijte oficiální [PostgreSQL apt nebo yum repo](https://www.postgresql.org/download/linux/).

#### Krok 2: Inicializujte databázový cluster

U **rodiny Debian** balíček vytvoří a spustí cluster automaticky — pokračujte dalším krokem.

U **rodiny RHEL** je třeba cluster vytvořit explicitně:

```bash
sudo postgresql-setup --initdb
```

#### Krok 3: Spusťte a povolte službu

```bash
sudo systemctl enable --now postgresql
```

Tím spustíte PostgreSQL okamžitě a nakonfigurujete automatické spuštění při startu systému.

#### Krok 4: Ověřte instalaci

```bash
psql --version
sudo systemctl status postgresql
```

Měli byste vidět verzi PostgreSQL a službu s označením `active (running)`.

#### Krok 5: Připojte se na server

Balíček PostgreSQL na Linuxu vytvoří systémový účet `postgres`, který vlastní cluster. Připojte se přes něj:

```bash
sudo -u postgres psql
```

!!! note "Poznámka — na Linuxu se to liší oproti Windows"

    Windows instalátor vás během nastavení vyzve k zadání hesla pro superuživatele `postgres`. Linuxové balíčky to neprovádějí. Místní připojení jsou autentizována pomocí **peer authentication**: uživatel operačního systému `postgres` se může připojit jako databázový uživatel `postgres` bez hesla.

    Proto příkaz výše používá `sudo -u postgres`. digna backend se připojuje přes TCP s uživatelským jménem a heslem, takže si vytvoříte explicitního uživatele digna v části [Počáteční instalace](#initial-installation).

#### Krok 6: Potvrďte port

Výchozí port PostgreSQL je `5432`. Pro potvrzení portu, na kterém server naslouchá:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Poznamenejte si hodnotu — budete ji potřebovat při konfiguraci digna backendu.

#### Krok 7: Povolení autentizace heslem pro uživatele digna

digna se k PostgreSQL připojuje přes TCP jako `digna_user`, což vyžaduje autentizaci heslem místo peer autentizace. Zkontrolujte, že váš `pg_hba.conf` to umožňuje.

Najděte soubor:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Otevřete ho v editoru a potvrďte, že řádky pro lokální TCP používají `scram-sha-256` (nebo `md5` na starších serverech) místo `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Po jakékoliv změně PostgreSQL znovu načtěte:

```bash
sudo systemctl reload postgresql
```

!!! warning "Důležité"

    Pokud digna nahlásí `FATAL: Ident authentication failed for user "digna_user"`, je to způsobeno tímto nastavením.

#### Krok 8: Pokud PostgreSQL běží na jiném stroji

Aby server akceptoval připojení z jiného hostitele, nastavte `listen_addresses` v `postgresql.conf` a přidejte odpovídající `host` řádek pro vaši síť v `pg_hba.conf`:

```
listen_addresses = '*'
```

Pak otevřete port ve firewallu a restartujte službu:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Konfigurace webového serveru {: #web-server-configuration }

digna potřebuje webový server pro hostování dashboardu. Vyberte jednu z následujících možností:

- [nginx](#nginx-setup) — lehký a doporučený
- [Apache httpd](#apache-setup) — široce rozšířená alternativa

Instalovat a konfigurovat potřebujete jen **jeden** z těchto serverů.

Obě sekce konfigurují dvě věci, na kterých dashboard závisí:

- **Fallback pro single-page aplikaci**, aby obnovení stránky dashboardu nevracelo 404
- **MIME typ `.md`**, aby se Markdown soubory správně servírovaly

### Nastavení nginx {: #nginx-setup }

#### Přehled

nginx je lehký, vysoce výkonný webový server vhodný pro servírování statického digna dashboardu.

#### Instalace

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Spuštění nginx

```bash
sudo systemctl enable --now nginx
```

#### Ověření instalace

1. Otevřete prohlížeč
2. Přejděte na `http://localhost`
3. Měli byste vidět uvítací stránku nginx

#### Otevření firewallu

Pokud bude server přístupný z jiných strojů, povolte HTTP provoz:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Konfigurace webu pro dashboard

nginx načítá všechny soubory v adresáři `conf.d` u obou rodin distribucí. Vytvořte tam dedikovaný konfigurační soubor pro digna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Vložte následující a nahraďte `/opt/digna/dashboard` reálnou cestou k rozbalené složce `dashboard`:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

    Bez direktivy `try_files` obnovení jakékoli stránky dashboardu kromě kořenové URL vrátí 404. To je ekvivalent modulu URL Rewrite v IIS na Windows.

#### Deaktivace výchozího webu

Pouze jeden serverový blok může být `default_server` pro port. U **rodiny Debian** odstraňte balíčkovaný výchozí site, aby nedošlo ke konfliktu:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

U **rodiny RHEL** zakomentujte nebo smažte blok `server { ... }` uvnitř `/etc/nginx/nginx.conf`.

#### Aplikujte konfiguraci

Ověřte konfiguraci na syntaktické chyby a pak nginx znovu načtěte:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Nastavení Apache httpd {: #apache-setup }

#### Přehled

Apache httpd je k dispozici v základních repozitářích všech podporovaných distribucí. Balíček se jmenuje `apache2` u rodiny Debian a `httpd` u rodiny RHEL.

#### Instalace

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Spuštění Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Ověření instalace

1. Otevřete prohlížeč
2. Přejděte na `http://localhost`
3. Měli byste vidět výchozí stránku Apache distribuce

#### Požadováno: povolit mod_rewrite

Dashboard vyžaduje přepis URL.

U **rodiny Debian** modul povolte a restartujte:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

U **rodiny RHEL** je `mod_rewrite` načteno ve výchozím nastavení. Potvrďte to:

```bash
httpd -M | grep rewrite
```

#### Požadováno: povolení .htaccess přepisů

Otevřete konfigurační soubor pro váš dokumentový kořen:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Najděte `<Directory>` blok pokrývající váš dokumentový kořen (`/var/www/html` u obou rodin) a změňte:

```apache
AllowOverride None
```

na:

```apache
AllowOverride All
```

#### Požadováno: MIME typ pro Markdown soubory

Do stejného souboru přidejte následující řádek, aby se Markdown soubory správně servírovaly:

```apache
AddType text/markdown .md
```

!!! warning "Důležité"

    Bez tohoto nastavení nemusí být `.md` soubory servírovány správně.

#### Aplikujte konfiguraci

Zkontrolujte konfiguraci na syntaktické chyby a pak Apache restartujte:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Počáteční instalace {: #initial-installation }

### Krok 1: Nastavte repozitář digna

Repozitář digna ukládá všechny metriky vypočítané dignou. Působí jako centrální databáze pro analytická a výkonová data.

#### Vytvoření schématu a uživatele repozitáře

Otevřete svůj PostgreSQL klient (psql, pgAdmin nebo podobně) a proveďte následující SQL příkazy:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Nahraďte následující zástupné hodnoty:**

- `<digna_repo_schema>` — požadovaný název schématu (např. `dignarepo`)
- `<digna_repo_user>` — požadované uživatelské jméno (např. `digna_user`)
- `<digna_repo_password>` — bezpečné heslo pro tohoto uživatele

**Příklad:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Pro spuštění těchto příkazů z shellu v jednom kroku:

```bash
sudo -u postgres psql
```

Pak vložte příkazy na výzvu `postgres=#` a pro ukončení napište `\q`.

!!! tip "Doporučené"

    Používejte silná, komplexní hesla pro databázové uživatele. Vyhněte se snadno uhodnutelným přihlašovacím údajům.

---

### Krok 2: Rozbalte instalační balík digna

1. Najděte ZIP soubor s instalací digna, který vám byl poskytnut
2. Rozbalte ho do požadované instalační složky — například `/opt/digna`
3. Po rozbalení byste měli vidět následující položky:
   - `dashboard/` — webové rozhraní dashboardu
   - `digna` — hlavní spustitelný soubor (backend + CLI dohromady)

!!! info "Konfigurační a licenční soubory nejsou součástí balíku"

    Soubory `config.toml` ani `dashboard/dashboard_config.toml` nejsou součástí instalace — oba
    si vytvoříte sami, v částech [Konfigurace backendu](#backend-configuration) a
    [Konfigurace dashboardu](#dashboard-configuration). Ani `license.toml` není součástí
    balíku; digna jej dodává samostatně, jak popisuje krok 3.

Pro rozbalení ze shellu:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Poznámka"

    Pokud není nainstalován `unzip`, přidejte ho příkazem `sudo apt install -y unzip` nebo `sudo dnf install -y unzip`.

#### Umožněte spuštění souboru

V závislosti na způsobu přenosu archivu se mohla ztratit příznak spustitelnosti. Nastavte ho explicitně:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Vytvořte servisní účet

Pro provoz backendu je doporučeno použít dedikovaného neprivilegovaného uživatele pro produkční nasazení:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Poznámka"

    U rodiny RHEL je ekvivalentní cesta shellu `/sbin/nologin`.

### Krok 3: Nainstalujte licenční soubor

!!! warning "Důležité"

    Licenční soubor **není** součástí instalačního balíčku a bude vám poskytnut samostatně společností digna.

1. Najděte `license.toml` soubor, který vám byl poskytnut
2. Zkopírujte jej do kořenového instalačního adresáře digna (tam, kde jsou `config.toml` a spustitelný soubor `digna`)

**Proč je to důležité:**
Licenční soubor obsahuje informace o zákazníkovi, datum vypršení licence a digitální podpis. **Neměňte tento soubor** — jakákoliv úprava jej zneplatní.

**Struktura adresářů po nastavení:**

```
/opt/digna/
├── config.toml         (konfigurační soubor)
├── license.toml        (VAŠE LICENCE - zkopírujte sem)
├── digna               (hlavní spustitelný soubor)
├── bin/                (skripty pro správu služby)
└── dashboard/          (webové rozhraní)
    └── (soubory dashboardu)
```

---

## Konfigurace backendu {: #backend-configuration }

### Krok 1: Vytvořte a upravte konfigurační soubor

Soubor `config_template.toml` je součástí vaší instalační složky digna. Stačí jej přejmenovat na `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
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

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URL dashboardu | URL, ze kterých je dashboard servírován. Požadavky prohlížeče z jakéhokoli jiného původu jsou odmítnuty |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Povinné, aby prohlížeč s každým požadavkem odesílal cookie relace |

!!! note "Poznámka"

    Pokud servírujete dashboard z nginx nebo Apache na výchozím HTTP portu, původ, který povolit, je `http://localhost` — nebo veřejné URL serveru, pokud je dashboard dostupný z jiných strojů.

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
| `DIGNA_REPO_HOST` | `localhost` nebo IP | Hostitel/IP PostgreSQL serveru |
| `DIGNA_REPO_PORT` | `5432` (výchozí) | PostgreSQL port |
| `DIGNA_REPO_DB` | `postgres` | Název databáze |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Dříve vytvořené schéma |
| `DIGNA_REPO_USER` | `digna_user` | Uživatelské jméno vytvořené v PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Vaše heslo | Heslo nastavené při vytváření uživatele |
| `DIGNA_REPO_SSLMODE` | `prefer` (výchozí) | Volitelné. Režim SSL pro PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` nebo `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (výchozí) | Volitelné. Počet připojení, která digna udržuje otevřená k repozitáři |

!!! tip "Doporučené"

    `config.toml` obsahuje heslo k databázi v prostém textu. Omezte jeho oprávnění tak, aby soubor mohl číst pouze servisní účet:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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
| `DIGNA_MAX_WORKERS` | Počet CPU jader - 1 | Počet inspekcí, které mohou běžet současně |
| `DIGNA_FRONTEND_BASEURL` | URL dashboardu | Povinné. Používá se pro odkazy ve zprávách s upozorněními, proto musí jít o URL, kterou příjemci dokážou otevřít |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (výchozí) | Volitelné. Počet sekund, po které smí běžet jeden dotaz na zdrojovou databázi, než je přerušen; `0` časový limit vypíná |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (výchozí) | Volitelné. Počet sekund čekání na připojení ke zdrojové databázi; `0` čeká neomezeně dlouho |

!!! tip "Tip"

    Pro zjištění počtu CPU jader na serveru spusťte `nproc`.

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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Výchozí: dočasný adresář systému (`$TMPDIR`, nebo `/tmp`, pokud není nastaven) | Adresář pro dočasné soubory, když se data nevejdou do paměti |

!!! tip "Dimenzování digna Engine"

    Počítejte na hostiteli digna s až `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` paměti
    navíc k tomu, co spotřebuje samotná digna, a s dostatkem volného místa na disku v dočasném
    adresáři, aby se do něj vešlo největší inspektované datum zdrojů dat, které používají digna Engine.
    Nasměrujte `DIGNA_DUCKDB_TEMP_DIRECTORY` na disk s takovým místem, do kterého smí zapisovat účet,
    pod kterým digna běží:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
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

1. Otevřete terminál
2. Přejděte do instalační složky digna (tam, kde jsou `config.toml` a spustitelný soubor `digna`)
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

    Na Linuxu aktuální adresář není ve vaší PATH, takže spustitelný soubor se volá jako `./digna` místo `digna`. Pokud chcete používat kratší tvar všude, vytvořte symbolický odkaz:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
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

1. Otevřete **nové** okno terminálu
2. Přejděte do instalační složky digna
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

    Heslo uzavřete do jednoduchých uvozovek. `bash` a `zsh` zacházejí se znaky jako `!`, `$` a `*` speciálně, a nepřeořádované heslo je nemusí předat tak, jak bylo napsáno.

!!! tip "Doporučené"

    Používejte silné heslo kombinující velká a malá písmena, čísla a speciální znaky.

---

### Krok 6: Spusťte digna server

V instalačním adresáři digna spusťte server:

```bash
./digna serve --address <host> --port <port>
```

**Parametry:**
- `--address` — hostname/IP serveru (výchozí `127.0.0.1`)
- `--port` — port serveru (výchozí `8000`)

Jakmile server běží, vypíše adresu, na které naslouchá:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tip"

    Pokud je dashboard servírován z jiného stroje než backend, otevřete také API port ve firewallu:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Server drží terminál"

    `serve` běží na popředí a pokračuje, dokud jej nezastavíte pomocí ++ctrl+c++. Nechte jej běžet, než dokončíte nastavení; pokud jej chcete místo toho spouštět automaticky při startu, viz [Spuštění digna jako služby systemd](#running-digna-as-a-systemd-service).

## Konfigurace dashboardu {: #dashboard-configuration }

### Krok 1: Nasazení dashboardu na webový server

Dashboard digna načítá svou vlastní konfiguraci ze souboru `dashboard/dashboard_config.toml`. Tento soubor není součástí instalace — vytvoříte jej ve složce `dashboard/` vedle souborů dashboardu.

Jeho obsah je popsán v části [Jednotné přihlášení (SSO)](../../../sso/overview.md), kde je soubor také potřeba: obsahuje možnosti přihlášení, které dashboard nabízí, a u nasazení s více instancemi také připojení k backendu.

Vyberte webový server a postupujte podle příslušných kroků nasazení.

#### Nasazení na nginx

Pokud jste postupovali podle sekce [nginx Setup](#nginx-setup), serverový blok již ukazuje na složku `dashboard` a není třeba nic kopírovat.

1. **Potvrďte cestu**
   - Otevřete `/etc/nginx/conf.d/digna.conf`
   - Ověřte, že `root` ukazuje na vaši rozbalenou složku `dashboard`

2. **Zajistěte, aby složka byla čitelná**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Načtěte znovu nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Ověřte instalaci**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost` (nebo vaši nakonfigurovanou URL)
   - Měli byste vidět přihlašovací stránku digna dashboardu

#### Nasazení na Apache httpd

1. **Zkopírujte dashboard do dokumentového kořene**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Přidejte pravidla pro přepis**

   Vytvořte soubor `.htaccess` v nasazené složce, aby trasy dashboardu přežily obnovení stránky prohlížečem:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Přístup k dashboardu**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost/digna`
   - Měli byste vidět přihlašovací stránku digna dashboardu

### Krok 2: SELinux (pouze rodina RHEL)

Na RHEL, Rocky, AlmaLinux a Fedora je SELinux ve výchozím nastavení v režimu enforcing a zablokuje webový server v čtení souborů mimo očekávané lokace. Zkontrolujte, zda je aktivní:

```bash
getenforce
```

Pokud je výsledek `Enforcing` a servírujete dashboard z `/opt/digna/dashboard`, označte adresář tak, aby webový server k němu mohl číst:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Poznámka"

    Pokud příkaz `semanage` nenajdete, nainstalujte ho příkazem `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Důležité"

    Pokud dashboard na čerstvě nakonfigurovaném RHEL serveru vrací **403 Forbidden**, je to téměř vždy problém s označením SELinuxu, nikoliv s oprávněními souborů. Potvrďte pomocí `sudo ausearch -m avc -ts recent`.

---

## Spuštění digna jako systemd služby {: #running-digna-as-a-systemd-service }

### Proč spouštět digna jako službu?

Provoz digna backendu jako systemd služby zajistí, že:

- se automaticky spustí při startu stroje
- poběží na pozadí bez otevřeného terminálu
- se automaticky restartuje v případě pádu
- je možné jej spravovat přes `systemctl`, standardní správce služeb na Linuxu

### Soubory pro správu služby

Všechny potřebné soubory jsou umístěny v instalačním adresáři digna pod: `bin/`

Následující shell skripty jsou dostupné:

- `install_service.sh` — zaregistruje digna u systemd
- `uninstall_service.sh` — odregistruje službu
- `start_service.sh` — spustí registrovanou službu
- `stop_service.sh` — zastaví běžící službu

!!! warning "Je potřeba root oprávnění"

    Všechny skripty musíte spustit pomocí `sudo`, protože registrace služby, která se spouští při startu, zapisuje jednotkový soubor do `/etc/systemd/system`.

### Nastavení spustitelnosti skriptů

Při extrakci se mohl ztratit příznak spustitelnosti. Před prvním použitím:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Instalace služby

1. **Otevřete terminál**

2. **Přejděte do složky bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Spusťte instalační skript**
   ```bash
   sudo ./install_service.sh
   ```

Digna server je nyní zaregistrován u systemd s povoleným **automatickým spuštěním**. Služba se sama nespustí okamžitě — viz další sekce pro její spuštění.

### Spuštění a zastavení služby

#### Pro spuštění služby

1. Otevřete terminál
2. Přejděte do `/opt/digna/bin`
3. Spusťte:
   ```bash
   sudo ./start_service.sh
   ```

#### Pro zastavení služby

1. Otevřete terminál
2. Přejděte do `/opt/digna/bin`
3. Spusťte:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tip"

    Vždy službu zastavte před aktualizací souborů aplikace.

### Správa služby pomocí systemctl

Po registraci lze službu také ovládat standardními příkazy systemd z libovolného adresáře:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Ověření služby

Pro potvrzení, že je služba zaregistrována a běží:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` znamená, že se služba spouští při startu; `active` znamená, že právě běží.

### Zobrazení logů služby

systemd zachycuje všechno, co backend vypisuje na konzoli. Pro čtení:

```bash
sudo journalctl -u digna -n 100
```

Pro sledování logu živě během reprodukce problému:

```bash
sudo journalctl -u digna -f
```

!!! tip "Tip"

    Toto je nejrychlejší způsob, jak diagnostikovat službu, která se spustí a okamžitě zastaví. Selhání připojení k repozitáři nebo chybějící `license.toml` se zde zobrazí.

### Přesun služby do nového adresáře

Jednotkový soubor ukládá absolutní cestu ke spustitelnému souboru, takže přesunutí instalace vyžaduje opětovnou registraci služby:

1. **Odinstalujte stávající službu**
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

### Odinstalace služby

1. **Zastavte běžící službu**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Odinstalujte službu**
   ```bash
   sudo ./uninstall_service.sh
   ```

Digna server je nyní odregistrován z systemd.

---

## Aktualizace na nové vydání {: #upgrading-to-a-new-release }

Tato sekce popisuje upgrade instalace Release 2026.06 na Release 2026.11. Pokud je vaše
instalace starší, přečtěte si nejprve [Upgrade z verze starší než 2026.06](#upgrading-from-a-release-before-2026-06).

### Před aktualizací

**Vytvoření zálohy repozitáře digna je povinné**

Před upgradem digna zálohujte svůj repozitář (PostgreSQL), abyste se ochránili proti ztrátě dat.
Záloha vám umožní obnovit data, pokud by během upgradu nastaly neočekávané problémy.

Pro vytvoření zálohy ze shellu:

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

### Postup aktualizace

#### Krok 1: Zastavte službu digna {: #step-1-stop-the-digna-service }

Pokud digna běží jako systemd služba, nejprve ji zastavte:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Pokud digna běží v popředí, stiskněte v jejím terminálovém okně ++ctrl+c++.

#### Krok 2: Zálohujte stávající instalaci {: #step-2-backup-current-installation }

V instalačním adresáři digna přejmenujte spustitelný soubor a složku dashboardu stávající
instalace, aby vedle nich bylo možné nasadit nové vydání:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Soubor `digna_old` si ponechte, dokud upgrade neověříte, a složku `dashboard_old`, dokud z ní
neobnovíte své konfigurační soubory (viz krok 4). Poté můžete obojí smazat.

!!! info "Upgrade z verze starší než 2026.06"

    Místo spustitelného souboru přejmenujte složky `dignabackend` a `dignacli`:
    `sudo mv dignabackend dignabackend_old` a `sudo mv dignacli dignacli_old`. Release 2026.11 nepoužívá žádnou z nich.

#### Krok 3: Rozbalte a nasaďte novou verzi {: #step-3-extract-and-deploy-new-version }

1. Rozbalte nový ZIP soubor s instalací digna
2. Zkopírujte nový spustitelný soubor `digna` a složku `dashboard` do instalačního adresáře
3. Obnovte příznak spustitelnosti a vlastníka servisního účtu:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Důležité"

    Soubory `config.toml` ani `dashboard/dashboard_config.toml` nejsou nikdy součástí
    instalačního ZIP — tým digna žádný z nich nedodává. Vaše stávající konfigurace proto
    zůstane upgradem nedotčena a kopie v přejmenovaných složkách `*_old` jsou jediné,
    které máte.

#### Krok 4: Obnovte konfigurační soubory {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Nenechávejte si předchozí licenci"

    S předchozí licencí se digna sice spustí, ale digna Data Reconciliation a digna MCP Server
    zůstanou vypnuté. Každý příkaz, který licenci kontroluje — `user`, `inspection`, `repo` — se
    při neúspěšné kontrole ukončí dříve, než se repozitáře dotkne. Než budete pokračovat, ověřte
    novou licenci:

    ```bash
    ./digna license check
    ```

#### Krok 8: Aktualizujte schéma repozitáře {: #step-8-upgrade-the-repository-schema }

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

Pokud digna běží jako systemd služba:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Pokud digna spouštíte ručně, restartujte server:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Pokud používáte nginx nebo Apache, znovu načtěte příslušný webový server:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

U rodiny RHEL znovu aplikujte SELinux označení, pokud byla složka `dashboard` nahrazena:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Krok 10: Ověřte aktualizaci {: #step-10-verify-the-upgrade }

1. Ověřte vydání nového spustitelného souboru:

    ```bash
    ./digna version
    ```

    První řádek musí znít `Release: 2026.11`.

2. Otevřete dashboard digna a ověřte, že se rozhraní načítá správně.
3. Zkontrolujte logy serveru, zda neobsahují chyby:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Otestujte databázová připojení — viz
   [Testování připojení](../../../databases/overview.md#testing-a-connection). Po upgradu
   z verze starší než 2026.06 nejprve převeďte na ODBC každé připojení, které ODBC dosud
   nepoužívalo.

Jak začít s novými moduly, popisují stránky [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Připojení AI agenta](../../../platform/agentic/connect_ai_agent.md) pro digna MCP Server a
[Místo profilování](../../../platform/profiling/profiling_location.md) pro digna Engine.