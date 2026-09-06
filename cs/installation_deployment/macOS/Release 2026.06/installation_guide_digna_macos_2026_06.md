# Průvodce instalací na macOS pro digna Release 2026.06

**Release:** 2026.06

**Poslední aktualizace:** 5. září 2026


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

- **dignabackend**: Jádro aplikace zodpovědné za zpracování dat a provádění kontrol kvality.
- **dignadashboard**: Webové rozhraní hostované na webovém serveru, poskytující uživatelsky přívětivé prostředí pro práci s platformou digna a vizualizaci metrik kvality dat.

### Co je nového ve verzi 2026.06

Tato verze přináší schopnosti datové observability přímo do vašeho kódu, což umožňuje vývojářům sledovat kvalitu dat u zdroje. Kompletní podrobnosti najdete v [release notes](http://docs.digna.ai/changelog/Release_202606/).

### Hledáte Windows nebo Linux?

Tento průvodce pokrývá macOS. Pro jiné platformy viz [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) nebo [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — konfigurační soubor
   - `license.toml` — licenční soubor (zkopírujte sem svůj)

Pro rozbalení z Terminálu:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
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

Tato sekce konfiguruje nastavení backendu digna:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Hodnota | Poznámky |
|---|---|---|
| `digna_APP_HOST` | `localhost` nebo IP adresa | Hostname nebo IP, kde běží dignabackend |
| `digna_APP_PORT` | `8082` (výchozí) | Port pro REST API endpointy |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontendu | Pokud je dashboard na jiném serveru, zahrňte jeho URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Vyžadováno pro CORS s credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Povolit všechny HTTP metody |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Povolit všechny hlavičky |

!!! note "Poznámka"

    Pokud servírujete dashboard z Homebrew nginx na jeho výchozím portu, origin, který je třeba povolit, je `http://localhost:8080`.

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

| Parameter | Hodnota | Poznámky |
|---|---|---|
| `digna_REPO_HOST` | `localhost` nebo IP | Hostname/IP PostgreSQL serveru |
| `digna_REPO_PORT` | `5432` (výchozí) | Port PostgreSQL |
| `digna_REPO_DB` | `postgres` | Název databáze |
| `digna_REPO_SCHEMA` | `dignarepo` | Dříve vytvořené schéma |
| `digna_REPO_USER` | `digna_user` | Uživatel vytvořený v PostgreSQL |
| `digna_REPO_PASSWORD` | Vaše heslo | Heslo nastavené při tvorbě uživatele |

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

| Parameter | Hodnota | Poznámky |
|---|---|---|
| `digna_FERNET_KEY` | Šifrovací klíč | Používá se k šifrování tokenů a cookies (je zde výchozí) |
| `digna_COOKIE_DOMAIN` | `localhost` | Odpovídá vaší doméně frontendu |
| `digna_COOKIE_SECURE` | `false` (lokálně) / `true` (produkce) | Použijte `true` pro HTTPS připojení |
| `digna_COOKIE_HTTPONLY` | `true` | Vždy povoleno pro bezpečnost |
| `digna_COOKIE_SAME_SITE` | `lax` | Pomáhá předcházet CSRF útokům |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 hodin) | Doba platnosti relace v sekundách |
| `digna_MAX_WORKERS` | Počet CPU jader - 1 | Počet paralelních inspekčních úloh |

!!! tip "Tip"

    Pro zjištění počtu CPU jader na vašem Macu spusťte `sysctl -n hw.ncpu`.

#### Sekce [logging]

Tato sekce konfiguruje chování logování:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Hodnota | Poznámky |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` nebo `DEBUG` | `INFO` pro produkci, `DEBUG` pro ladění |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Počet denních záloh logů, které se uchovávají |

---

### Krok 2: Inicializujte repozitář

1. Otevřete **Terminál**
2. Přejděte do instalačního adresáře digna (kde jsou `config.toml` a spustitelný soubor `digna`)
3. Spusťte test připojení:

```bash
cd /opt/digna
./digna repo check
```

Měli byste vidět potvrzení, že je připojení navázáno (samo repozitář ještě nebyl inicializován).

!!! note "Poznámka"

    Na macOS nejsou příkazy v aktuálním adresáři na PATH, takže spustitelný soubor voláte jako `./digna` místo `digna`. Chcete-li používat kratší zápis všude, přidejte instalační složku do PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
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

Parametry:
- `--address` — hostname/IP serveru
- `--port` — port serveru

Měli byste vidět zprávy o spuštění potvrzující běh serveru:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Tip"

    Při prvním spuštění vás macOS může požádat, zda chcete aplikaci povolit příchozí síťová připojení. Klikněte **Allow**, jinak dashboard nebude moci komunikovat s backendem.

### Krok 5: Vytvořte administrátorského uživatele

1. Otevřete nové okno Terminálu
2. Přejděte do instalačního adresáře digna
3. Spusťte následující příkaz pro vytvoření admin uživatele:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Příklad:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Tím se vytvoří uživatel s uživatelským jménem `admin` a plnými administrátorskými právy.

!!! tip "Tip"

    Zabalte heslo do jednoduchých uvozovek. `zsh` zachází se znaky jako `!`, `$` a `*` speciálně, a neuváděné heslo je s těmito znaky nebude správně předáno.

!!! tip "Doporučení"

    Používejte silné heslo kombinující velká a malá písmena, čísla a speciální znaky.

---

## Konfigurace dashboardu {: #dashboard-configuration }

### Krok 1: Nasazení dashboardu na webový server

Digna dashboard má svůj vlastní soubor `config.toml` umístěný ve složce `dashboard/`. Tato konfigurace je již dodána a během počátečního nastavení ji obvykle není potřeba měnit. Měníte ji pouze v případě, že potřebujete upravit připojení na backend nebo jiné pokročilé nastavení.

Pokud potřebujete dashboard nakonfigurovat (např. pro nasazení ve více instancích), přečtěte si dokumentaci dashboardu.

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

### Před upgradem

Vytvoření zálohy repozitáře digna je POVINNÉ

Před upgradem digna zálohujte svůj repozitář (PostgreSQL), abyste se chránili proti ztrátě dat.
Záloha vám umožní obnovit data v případě nečekaných problémů během upgradu.

Pro vytvoření zálohy z Terminálu:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Postup upgradu

#### Krok 1: Zastavte službu digna

Pokud digna běží jako služba na pozadí, nejprve ji zastavte:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Pokud běží v popředí, stiskněte v jeho Terminálu `Ctrl + C`.

#### Krok 2: Zálohujte aktuální backendovou instalaci

Ve vašem instalačním adresáři digna:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Krok 3: Rozbalte a nasazení nové verze

1. Rozbalte nový instalační ZIP soubor digna
2. Zkopírujte nový `digna` spustitelný soubor a složku `dashboard` do instalačního adresáře
3. Obnovte spustitelný bit a v případě potřeby odstraňte karanténní atribut:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Důležité"

    Soubor `config.toml` **nikdy** není součástí instalačního ZIP. Vaše stávající konfigurace zůstane zachována.

### Krok 4: Obnovte konfigurační soubory

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Krok 5: Upgradujte schéma repozitáře

Přejděte do instalačního adresáře digna a spusťte:

```bash
cd /opt/digna
./digna repo upgrade
```

Tím se aktualizuje PostgreSQL schéma na nejnovější verzi při zachování všech existujících dat.

### Krok 6: Restartujte služby

Pokud běží jako služba na pozadí:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Pokud běžíte ručně, restartujte server:

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

#### Krok 7: Ověřte upgrade

1. Přistupte k digna dashboardu
2. Ověřte, že se rozhraní načítá správně
3. Zkontrolujte serverové logy na případné chyby