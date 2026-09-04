---
title: Průvodce instalací na Windows – digna Release 2026.06 | digna Documentation
description: Krok za krokem průvodce instalací digna Release 2026.06 na Windows — systémové požadavky, nastavení PostgreSQL, konfigurace webového serveru, konfigurace backendu a dashboardu, spuštění digna jako služby Windows a upgrade na novou verzi.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Průvodce instalací na Windows pro digna Release 2026.06

**Release:** 2026.06

**Naposledy aktualizováno:** 30. srpna 2026


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
10. [Upgrade na novou verzi](#upgrading-to-a-new-release)

---

## Úvod {: #introduction }

### O digna

digna je komplexní platforma poháněná umělou inteligencí navržená pro optimalizaci správy kvality dat napříč různými datovými prostředími, jako jsou datové sklady, datová jezera a lakehouse řešení. Je navržena tak, aby byla vysoce škálovatelná a přizpůsobitelná, přičemž řeší moderní datové výzvy prostřednictvím automatizace, monitoringu v reálném čase a detekce anomálií.

digna se skládá ze dvou hlavních komponent:

- **dignabackend**: Jádro aplikace, odpovědné za zpracování dat a provádění kontrol kvality.
- **dignadashboard**: Webové rozhraní hostované na webovém serveru, poskytující uživatelsky přívětivý způsob interakce s platformou digna a vizualizaci metrik kvality dat.

### Co je nového v Release 2026.06

Tato verze přináší možnosti data observability přímo do vašeho kódu, což umožňuje vývojářům sledovat kvalitu dat přímo u zdroje. Kompletní podrobnosti najdete v [release notes](http://docs.digna.ai/changelog/Release_202606/).

---

## Systémové požadavky {: #system-requirements }

Než začnete instalaci, ujistěte se, že váš systém splňuje následující minimální požadavky:

| Požadavek | Specifikace |
|---|---|
| **Operační systém** | Windows Server nebo Windows 10/11 |
| **Paměť (minimální instalace)** | 16 GB RAM |
| **Volné místo na disku** | 10 GB dostupného úložiště |
| **Databáze** | PostgreSQL Server 12 nebo novější |
| **Webový server** | IIS, Apache Tomcat nebo ekvivalent |

### Možnosti instalace databáze

**Pokud je PostgreSQL již nainstalován:**
Můžete přidat novou databázi pro digna na váš existující PostgreSQL server.

**Pokud instalujete PostgreSQL na stejný stroj jako digna:**

> **Doporučené specifikace**
>
> - **Paměť**: 32 GB RAM (místo 16 GB)
> - **Volné místo na disku**: 50 GB dostupného úložiště (místo 10 GB)
>
> Tyto vyšší specifikace zohledňují běh jak digna, tak PostgreSQL současně.

---

## Předinstalační nastavení {: #pre-installation-setup }

Než nainstalujete digna, ujistěte se, že jsou splněny dva klíčové předpoklady:

1. **PostgreSQL Server** – pro ukládání vypočítaných metrik a výkonových dat
2. **Webový server** – pro hostování digna Dashboardu

Pokud tyto komponenty ještě nejsou nastaveny, postupujte podle níže uvedených sekcí k jejich instalaci a konfiguraci.

---

## Nastavení PostgreSQL serveru {: #postgresql-server-setup }

### Pokud již máte PostgreSQL

Pokud je PostgreSQL již nainstalovaný a běží na vašem lokálním stroji nebo používáte spravovaný vzdálený PostgreSQL server, můžete přejít k [další sekci](#web-server-configuration).

### Instalace PostgreSQL

Postupujte podle těchto kroků pro instalaci PostgreSQL na Windows:

#### Krok 1: Stáhněte PostgreSQL

1. Navštivte stránku [PostgreSQL Downloads](https://www.postgresql.org/download/)
2. Zvolte **Windows**
3. Stáhněte nejnovější instalační program

#### Krok 2: Spusťte instalační program

1. Dvojklikem otevřete stažený instalační soubor
2. Postupujte podle pokynů průvodce instalací

#### Krok 3: Zvolte instalační adresář

Vyberte adresář, kam bude PostgreSQL nainstalován. Výchozí umístění je obvykle vhodné.

#### Krok 4: Vyberte komponenty

Pro standardní instalaci ponechte výchozí volby komponent.

#### Krok 5: Nastavte heslo superuživatele PostgreSQL

Zadejte a potvrďte heslo pro superuživatele PostgreSQL (`postgres`). **Uložte toto heslo bezpečně** — později ho budete potřebovat.

#### Krok 6: Nakonfigurujte číslo portu

Výchozí port PostgreSQL je `5432`. Můžete použít výchozí nebo specifikovat jiný port podle potřeby.

> **Tip**
>
> Pokud je port 5432 již obsazen, zvolte alternativní port a poznamenejte si ho pro pozdější konfiguraci.

#### Krok 7: Vyberte locale

Zvolte locale pro vaši databázi. Výchozí hodnota je obvykle vhodná pro většinu instalací.

#### Krok 8: Dokončete instalaci

Klikněte na **Next** v zbývajících krocích a poté na **Finish**.

#### Krok 9: Ověřte instalaci

Otevřete Příkazový řádek a ověřte, že je PostgreSQL nainstalován:

```bash
psql --version
```

Pokud byla instalace úspěšná, zobrazí se verze PostgreSQL.

---

## Konfigurace webového serveru {: #web-server-configuration }

digna vyžaduje webový server pro hostování dashboardu. Vyberte jednu z následujících možností:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Je potřeba nainstalovat a nakonfigurovat pouze **jeden** z těchto serverů.

### Nastavení IIS {: #iis-setup }

#### Přehled

Internet Information Services (IIS) je webový server od Microsoftu pro hostování webových stránek a webových aplikací.

#### Povolení IIS

1. **Otevřete Ovládací panely**
   - Stiskněte `Win + R`
   - Zadejte `control` a stiskněte Enter

2. **Přejděte na Windows Features**
   - Klikněte na **Programs**
   - Vyberte **Turn Windows features on or off**

3. **Povolte Internet Information Services**
   - Najděte **Internet Information Services (IIS)**
   - Zaškrtněte políčko pro jeho povolení
   - Klikněte na **+**, rozbalte a ověřte, že jsou vybrány tyto podkomponenty:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klikněte na OK** pro aplikaci změn

5. **Ověřte instalaci IIS**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost`
   - Měli byste vidět IIS Welcome stránku

#### Povinné: URL Rewrite Module

IIS vyžaduje komponentu URL Rewrite. Stáhněte a nainstalujte ji z [oficiální stránky Microsoftu](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Povinné: MIME typ pro Markdown soubory

Aby byly Markdown soubory (`.md`) správně obsluhovány IIS:

1. Otevřete **IIS Manager** (stiskněte `Win + R`, zadejte `inetmgr`, stiskněte Enter)
2. Přejděte na **Your Site > MIME Types**
3. Klikněte **Add...**
4. Nakonfigurujte:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

> **Důležité**
>
> Bez tohoto nastavení nemusí být `.md` soubory správně obsluhovány.

---

### Nastavení Apache Tomcat {: #apache-tomcat-setup }

#### Přehled

Apache Tomcat je open-source kontejner pro Java servlety a webový server.

#### Instalace

1. **Stáhněte Apache Tomcat**
   - Navštivte [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Stáhněte Windows ZIP distribuci

2. **Rozbalte archiv**
   - Rozbalte ZIP soubor do adresáře na vašem systému
   - Příklad: `C:\Program Files\Apache Tomcat`

3. **Ověřte, že Tomcat běží**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost:8080`
   - Měli byste vidět uvítací stránku Apache Tomcat

> **Tip**
>
> Apache Tomcat se obvykle spustí automaticky po instalaci. Pokud se nespustí, přejděte do složky `bin` a spusťte `startup.bat`.

---

## Počáteční instalace {: #initial-installation }

### Krok 1: Nastavení digna repository

Repository digna ukládá všechny metriky vypočítané digna. Slouží jako centrální databáze pro analytická a výkonová data.

#### Vytvoření schématu a uživatele repository

Otevřete váš PostgreSQL klient (pgAdmin, psql nebo podobný) a spusťte následující SQL příkazy:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Nahraďte následující zástupné hodnoty:**

- `<digna_repo_schema>` — Vámi zvolené jméno schématu (např. `dignarepo`)
- `<digna_repo_user>` — Vámi zvolené uživatelské jméno (např. `digna_user`)
- `<digna_repo_password>` — Silné heslo pro tohoto uživatele

**Příklad:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **Nejlepší postup**
>
> Používejte silná, komplexní hesla pro databázové uživatele. Vyvarujte se snadno uhodnutelných přihlašovacích údajů.

---

### Krok 2: Rozbalení instalačního balíku digna

1. Najděte ZIP soubor s instalací digna, který vám byl poskytnut
2. Rozbalte ho do požadovaného instalačního umístění
3. Po rozbalení byste měli vidět následující položky:
   - `dashboard/` — Webové rozhraní dashboardu
   - `digna` — Hlavní spustitelný soubor (backend + CLI v jednom)
   - `config.toml` — Konfigurační soubor
   - `license.toml` — Licenční soubor (sem zkopírujte svůj)

### Krok 3: Instalace licenčního souboru

> **Důležité**
>
> Licenční soubor **není** součástí instalačního balíku a bude vám poskytnut samostatně společností digna.

1. Najděte poskytnutý soubor `license.toml`
2. Zkopírujte jej do kořenového adresáře instalace digna (tam, kde se nachází `config.toml` a spustitelný soubor `digna`)

**Proč je to důležité:**
Licenční soubor obsahuje informace o zákazníkovi, datum vypršení licence a digitální podpis. **Neměňte tento soubor** — jakékoliv úpravy ho zneplatní.

**Struktura adresářů po nastavení:**

```
digna_installation/
├── config.toml         (konfigurační soubor)
├── license.toml        (VÁŠ LICENČNÍ SOUBOR - sem ho zkopírujte)
├── digna               (hlavní spustitelný soubor)
└── dashboard/          (webové rozhraní)
    └── (soubory dashboardu)
```

---

## Konfigurace backendu {: #backend-configuration }

### Krok 1: Vytvoření a úprava konfiguračního souboru

Soubor `config_template.toml` je dodán ve vaší instalační složce digna. Stačí jej přejmenovat na `config.toml`.

**Umístění:** `digna_installation/config.toml`

Otevřete `config.toml` v textovém editoru a nakonfigurujte každou z níže uvedených sekcí.

#### Sekce [app]

Tato sekce konfiguruje nastavení backend aplikace digna:

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
| `digna_APP_HOST` | `localhost` nebo IP adresa | Hostname nebo IP, kde je hostován dignabackend |
| `digna_APP_PORT` | `8082` (výchozí) | Port pro REST API koncové body |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontendu | Pokud je dashboard na jiném serveru, přidejte jeho URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Požadováno pro CORS s přihlašovacími údaji |
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
| `digna_REPO_HOST` | `localhost` nebo IP | Host PostgreSQL serveru / IP |
| `digna_REPO_PORT` | `5432` (výchozí) | Port PostgreSQL |
| `digna_REPO_DB` | `postgres` | Jméno databáze |
| `digna_REPO_SCHEMA` | `dignarepo` | Dříve vytvořené schéma |
| `digna_REPO_USER` | `digna_user` | Uživatel vytvořený v PostgreSQL |
| `digna_REPO_PASSWORD` | Vaše heslo | Heslo nastavené při vytváření uživatele |

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
| `digna_FERNET_KEY` | Šifrovací klíč | Používá se k šifrování tokenů a cookies (výchozí je poskytnut) |
| `digna_COOKIE_DOMAIN` | `localhost` | Odpovídejte doméně vašeho frontendu |
| `digna_COOKIE_SECURE` | `false` (lokálně) / `true` (produkce) | Použijte `true` pro HTTPS připojení |
| `digna_COOKIE_HTTPONLY` | `true` | Vždy povoleno z bezpečnostních důvodů |
| `digna_COOKIE_SAME_SITE` | `lax` | Zabraňuje CSRF útokům |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 hodin) | Vypršení relace v sekundách |
| `digna_MAX_WORKERS` | Počet CPU jader - 1 | Počet paralelních inspekčních úloh |

#### Sekce [logging]

Tato sekce konfiguruje chování logování:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametr | Hodnota | Poznámky |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` nebo `DEBUG` | `INFO` pro produkci, `DEBUG` pro řešení problémů |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Počet denních záloh logů, které se uchovávají |

---

### Krok 3: Inicializace repository

1. Otevřete Příkazový řádek
2. Přejděte do instalačního adresáře digna (kam jste umístili `config.toml` a spustitelný soubor `digna`)
3. Spusťte test připojení:

```bash
digna repo check
```

Měli byste vidět potvrzení, že je připojení navázáno (samotné repository ještě nebylo inicializováno).

### Krok 4: Instalace schématu repository

Ve stejném adresáři spusťte:

```bash
digna repo install
```

Tento příkaz nainstaluje potřebné tabulky a schéma ve vaší PostgreSQL databázi.

### Krok 5: Spuštění digna serveru

V instalačním adresáři digna spusťte server:

```bash
digna serve --address <host> --port <port>
```

**Parametry:**
- `--address` — Hostname/IP serveru
- `--port` — Port serveru 

Měli byste vidět startovací hlášky potvrzující, že server běží:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Krok 6: Vytvoření administrátorského uživatele

1. Otevřete **nové** okno Příkazového řádku
2. Přejděte do instalačního adresáře digna
3. Spusťte následující příkaz pro vytvoření administrátorského uživatele:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Příklad:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Tím se vytvoří uživatel s plnými administrátorskými právy.

> **Nejlepší postup**
>
> Používejte silné heslo obsahující kombinaci velkých a malých písmen, čísel a speciálních znaků.

---

## Konfigurace dashboardu {: #dashboard-configuration }

### Krok 1: Nasazení dashboardu na webový server

Dashboard digna má vlastní samostatný soubor `config.toml` uložený v adresáři `dashboard/`. Tato konfigurace je již dodána a obvykle nevyžaduje změny při počátečním nastavení. Je třeba ji upravovat pouze tehdy, pokud potřebujete přizpůsobit připojení na backend (např. při nasazení více instancí).

Pokud potřebujete upravit konfiguraci dashboardu, nahlédněte do dokumentace dashboardu.

Vyberte webový server a postupujte podle příslušných kroků pro nasazení.

#### Nasazení do IIS

1. **Otevřete IIS Manager**
   - Stiskněte `Win + R`, zadejte `inetmgr`, stiskněte Enter

2. **Vytvořte novou webovou stránku**
   - V levém panelu klikněte pravým tlačítkem na **Sites**
   - Zvolte **Add Website...**

3. **Nakonfigurujte web**
   - **Site Name**: Zadejte název (např. "dignaDashboard")
   - **Physical Path**: Klikněte na Browse a vyberte složku `dashboard`
   - **Binding**: Nastavte IP adresu a port (výchozí port 80 pro HTTP, 443 pro HTTPS)

4. **Spusťte web**
   - Klikněte **OK** pro vytvoření webu
   - Klikněte pravým tlačítkem na nově vytvořený web a vyberte **Start**

5. **Ověřte instalaci**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost` (nebo vaši nakonfigurovanou URL)
   - Měli byste vidět přihlašovací stránku dashboardu digna

#### Nasazení do Apache Tomcat

1. **Zkopírujte dashboard do Tomcat**
   - Zkopírujte složku `dashboard` do adresáře `webapps` Tomcatu
   - Přejmenujte ji podle potřeby (např. na `digna`)
   - Příklad: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Ověřte nasazení**
   - Obnovte nebo znovu načtěte Tomcat management stránku (http://localhost:8080)
   - Měli byste vidět "digna" (nebo zvolené jméno) v seznamu nasazených aplikací

3. **Přístup k dashboardu**
   - Otevřete prohlížeč
   - Přejděte na `http://localhost:8080/digna`
   - Měli byste vidět přihlašovací stránku dashboardu digna

---

## Spuštění digna jako služby Windows {: #running-digna-as-a-windows-service }

### Proč používat službu Windows?

Spuštění backendu digna jako Windows služby zajistí, že:
- se spustí automaticky při startu serveru
- běží na pozadí bez otevřeného Příkazového řádku
- se automaticky restartuje v případě pádu
- je možné ji spravovat přes Windows Services

### Soubory pro správu služby

Všechny potřebné soubory jsou umístěny v instalačním adresáři digna pod: `bin/`

K dispozici jsou tyto dávkové soubory:
- `install_service.bat` — Zaregistruje digna jako Windows službu
- `uninstall_service.bat` — Odstraní registraci služby
- `start_service.bat` — Spustí registrovanou službu
- `stop_service.bat` — Zastaví běžící službu

> **Vyžadováno oprávnění správce**
>
> Všechny dávkové soubory musí být spuštěny s oprávněními Administrátora.

### Instalace služby

1. **Otevřete Příkazový řádek jako Administrátor**
   - Klikněte pravým tlačítkem na Příkazový řádek
   - Vyberte "Run as Administrator"

2. **Přejděte do složky bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Spusťte instalační skript**
   ```bash
   install_service.bat
   ```

digna server je nyní zaregistrován jako Windows služba s povoleným automatickým spuštěním. Služba se však nespustí okamžitě — viz následující sekci pro její spuštění.

### Spuštění a zastavení služby

#### Pro spuštění služby

1. Otevřete Příkazový řádek jako Administrátor
2. Přejděte do `digna\bin`
3. Spusťte:
   ```bash
   start_service.bat
   ```

#### Pro zastavení služby

1. Otevřete Příkazový řádek jako Administrátor
2. Přejděte do `digna\bin`
3. Spusťte:
   ```bash
   stop_service.bat
   ```

> **Tip**
>
> Vždy službu zastavte před aktualizací souborů aplikace.

### Přesunutí služby do nového adresáře

Pokud potřebujete přesunout instalaci digna:

1. **Odinstalujte současnou službu**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Přesuňte soubory aplikace**
   - Přesuňte celou instalační složku digna na nové místo

3. **Znovu nainstalujte službu**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Spusťte službu**
   ```bash
   start_service.bat
   ```

### Odinstalování služby

1. **Zastavte běžící službu**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Odinstalujte službu**
   ```bash
   uninstall_service.bat
   ```

digna server je nyní zrušen jako Windows služba.

---

## Upgrade na novou verzi {: #upgrading-to-a-new-release }

### Před upgradem

**Vytvoření zálohy digna repository je POVINNÉ**

Před upgradem digna zálohujte svoje repository (PostgreSQL), abyste předešli ztrátě dat.
Záloha zajistí možnost obnovy, pokud by během upgradu nastaly neočekávané problémy.

### Proces upgradu

#### Krok 1: Zastavte službu digna

Pokud běží digna jako Windows služba, nejprve ji zastavte:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Krok 2: Zálohujte aktuální backend instalaci

Ve vašem instalačním adresáři digna:

```bash
# Přejmenujte složku obsahující dignabackend
ren dignabackend dignabackend_old
```
```bash
# Přejmenujte dashboard
ren dashboard dashboard_old
```

#### Krok 3: Rozbalte a nasadte novou verzi

1. Rozbalte nový instalační ZIP soubor digna
2. Zkopírujte nový spustitelný soubor `digna` a složku `dashboard` do instalačního adresáře


> **Důležité**
>
> Soubor `config.toml` **nikdy** není součástí instalačního ZIP. Vaše existující konfigurace zůstane zachována.

### Krok 4: Obnovte konfigurační soubory

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Krok 5: Upgradujte schéma repository

Přejděte do instalačního adresáře digna a spusťte:

```bash
digna repo upgrade
```

Tento příkaz aktualizuje PostgreSQL schéma na nejnovější verzi při zachování veškerých existujících dat.

### Krok 6: Restartujte služby

Pokud běží jako Windows služba:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Pokud běžíte ručně, restartujte server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Pokud používáte IIS nebo Tomcat, restartujte příslušný webový server.

#### Krok 7: Ověřte upgrade

1. Přistupte k digna dashboardu
2. Ověřte, že se rozhraní načítá správně
3. Zkontrolujte serverové logy na případné chyby
