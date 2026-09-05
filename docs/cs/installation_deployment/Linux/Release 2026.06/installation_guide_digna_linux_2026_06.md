---
title: Průvodce instalací na Linuxu – digna Release 2026.06 | digna Dokumentace
description: Krok za krokem průvodce instalací digna Release 2026.06 na Linuxu — systémové požadavky, nastavení PostgreSQL, konfigurace nginx nebo Apache, konfigurace backendu a dashboardu, spuštění digna jako systemd služby a aktualizace na nové vydání.
keywords: digna instalace linux, digna průvodce nasazením, nastavení digna backendu, instalace digna dashboardu, postgresql linux, nginx linux, digna systemd služba, digna průvodce aktualizací
image: /assets/logo_square.png
---

# Průvodce instalací na Linuxu pro digna Release 2026.06

**Release:** 2026.06

**Poslední aktualizace:** 5. září 2026


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

- **dignabackend**: Jádro aplikace, které zpracovává data a provádí kontroly kvality.
- **dignadashboard**: Webové rozhraní hostované na webovém serveru, které poskytuje uživatelsky přívětivé rozhraní pro práci s platformou digna a vizualizaci metrik kvality dat.

### Co je nového ve vydání 2026.06

Toto vydání přináší schopnosti datové observability přímo do vašeho kódu, což umožňuje vývojářům monitorovat kvalitu dat u zdroje. Kompletní podrobnosti naleznete v [poznámkách k vydání](http://docs.digna.ai/changelog/Release_202606/).

### Hledáte Windows nebo macOS?

Tento průvodce pokrývá Linux. Pro jiné platformy viz [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) nebo [macOS Installation Guide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

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
   - `config.toml` — konfigurační soubor
   - `license.toml` — licenční soubor (zkopírujte sem svůj)

Pro rozbalení ze shellu:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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

Tato sekce konfiguruje nastavení aplikace digna backend:

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
| `digna_APP_HOST` | `localhost` nebo IP adresa | Hostitel nebo IP, kde běží dignabackend |
| `digna_APP_PORT` | `8082` (výchozí) | Port pro REST API koncové body |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontendu | Pokud běží dashboard na jiném serveru, přidejte jeho URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Požadováno pro CORS s pověřeními |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Povolit všechny HTTP metody |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Povolit všechny hlavičky |

!!! note "Poznámka"

    Pokud servírujete dashboard z nginx nebo Apache na výchozím HTTP portu, původ, který povolit, je `http://localhost` — nebo veřejné URL serveru, pokud je dashboard dostupný z jiných strojů.

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
| `digna_REPO_HOST` | `localhost` nebo IP | Hostitel/IP PostgreSQL serveru |
| `digna_REPO_PORT` | `5432` (výchozí) | PostgreSQL port |
| `digna_REPO_DB` | `postgres` | Název databáze |
| `digna_REPO_SCHEMA` | `dignarepo` | Dříve vytvořené schéma |
| `digna_REPO_USER` | `digna_user` | Uživatelské jméno vytvořené v PostgreSQL |
| `digna_REPO_PASSWORD` | Vaše heslo | Heslo nastavené při vytváření uživatele |

!!! tip "Doporučené"

    `config.toml` obsahuje heslo k databázi v prostém textu. Omezte jeho oprávnění tak, aby soubor mohl číst pouze servisní účet:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### Sekce [base]

Tato sekce obsahuje bezpečnostní a cookie nastavení:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `digna_FERNET_KEY` | Šifrovací klíč | Používá se k šifrování tokenů a cookie (je poskytnut výchozí) |
| `digna_COOKIE_DOMAIN` | `localhost` | Odpovídejte doméně frontendu |
| `digna_COOKIE_SECURE` | `false` (lokálně) / `true` (produkce) | Použijte `true` pro HTTPS připojení |
| `digna_COOKIE_HTTPONLY` | `true` | Vždy povolit z bezpečnostních důvodů |
| `digna_COOKIE_SAME_SITE` | `lax` | Zabrání CSRF útokům |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 hodin) | Vypršení relace v sekundách |
| `digna_MAX_WORKERS` | Počet CPU jader - 1 | Počet paralelních inspekčních úloh |

!!! tip "Tip"

    Pro zjištění počtu CPU jader na serveru spusťte `nproc`.

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

### Krok 2: Inicializujte repozitář

1. Otevřete terminál
2. Přejděte do instalační složky digna (tam, kde jsou `config.toml` a spustitelný soubor `digna`)
3. Spusťte test připojení:

```bash
cd /opt/digna
./digna repo check
```

Měli byste vidět potvrzení, že připojení bylo navázáno (samo repozitář ještě nebyl inicializován).

!!! note "Poznámka"

    Na Linuxu aktuální adresář není ve vaší PATH, takže spustitelný soubor se volá jako `./digna` místo `digna`. Pokud chcete používat kratší tvar všude, vytvořte symbolický odkaz:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Krok 3: Nainstalujte schéma repozitáře

Ve stejném adresáři spusťte:

```bash
./digna repo install
```

Tento příkaz nainstaluje potřebné tabulky a schéma ve vaší PostgreSQL databázi.

### Krok 4: Spusťte digna server

V instalačním adresáři digna spusťte server:

```bash
./digna serve --address <host> --port <port>
```

**Parametry:**
- `--address` — hostname/IP serveru
- `--port` — port serveru

Měli byste vidět spouštěcí zprávy potvrzující, že server běží:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Tip"

    Pokud je dashboard servírován z jiného stroje než backend, otevřete také API port ve firewallu:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Krok 5: Vytvořte administrátorského uživatele

1. Otevřete **nové** okno terminálu
2. Přejděte do instalační složky digna
3. Spusťte následující příkaz pro vytvoření admin uživatele:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Příklad:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Tím vytvoříte uživatele s uživatelským jménem `admin` a plnými administrátorskými právy.

!!! tip "Tip"

    Heslo uzavřete do jednoduchých uvozovek. `bash` a `zsh` zacházejí se znaky jako `!`, `$` a `*` speciálně, a nepřeořádované heslo je nemusí předat tak, jak bylo napsáno.

!!! tip "Doporučené"

    Používejte silné heslo kombinující velká a malá písmena, čísla a speciální znaky.

---

## Konfigurace dashboardu {: #dashboard-configuration }

### Krok 1: Nasazení dashboardu na webový server

Dashboard digna má svůj vlastní samostatný soubor `config.toml` umístěný v adresáři `dashboard/`. Tato konfigurace je již poskytnuta a během počátečního nastavení obvykle není nutné ji měnit. Upravte ji pouze, pokud potřebujete přizpůsobit připojení na backend.

Pokud potřebujete změnit konfiguraci dashboardu (např. pro nasazení více instancí), odkažte se na dokumentaci dashboardu.

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

### Před aktualizací

**Vytvoření zálohy repozitáře digna je povinné**

Před aktualizací digna zálohujte svůj repozitář (PostgreSQL), abyste se ochránili proti ztrátě dat.
Záloha vám umožní obnovit data, pokud by během aktualizace nastaly neočekávané problémy.

Pro vytvoření zálohy ze shellu:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Postup aktualizace

#### Krok 1: Zastavte službu digna

Pokud běží digna jako systemd služba, nejprve ji zastavte:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Pokud běží v popředí, stiskněte v jeho terminálovém okně `Ctrl + C`.

#### Krok 2: Zálohujte aktuální backend instalaci

Ve své instalační složce digna:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Krok 3: Rozbalte a nasaďte novou verzi

1. Rozbalte nový ZIP soubor s instalací digna
2. Zkopírujte nový spustitelný soubor `digna` a složku `dashboard` do instalační složky
3. Obnovte příznak spustitelnosti a vlastníka servisního účtu:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Důležité"

    Soubor `config.toml` **nikdy** není součástí instalačního ZIP. Vaše stávající konfigurace zůstane nedotčena.

### Krok 4: Obnovte konfigurační soubory

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Krok 5: Aktualizujte schéma repozitáře

Přejděte do instalační složky digna a spusťte:

```bash
cd /opt/digna
./digna repo upgrade
```

Tím se aktualizuje PostgreSQL schéma na nejnovější verzi při zachování všech existujících dat.

### Krok 6: Restartujte služby

Pokud běží jako systemd služba:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Pokud běžíte ručně, znovu spusťte server:

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

#### Krok 7: Ověřte aktualizaci

1. Přistupte k digna dashboardu
2. Ověřte, že se rozhraní načítá správně
3. Zkontrolujte logy serveru pro případné chyby:

```bash
sudo journalctl -u digna -n 100
```