# Ghid de instalare pe Windows pentru digna Release 2026.06

**Release:** 2026.06

**Ultima actualizare:** 30 august 2026


---

## Cuprins

1. [Introducere](#introduction)
2. [Cerințe de sistem](#system-requirements)
3. [Pregătirea înainte de instalare](#pre-installation-setup)
4. [Configurarea serverului PostgreSQL](#postgresql-server-setup)
5. [Configurarea web serverului](#web-server-configuration)
6. [Instalarea inițială](#initial-installation)
7. [Configurarea backend-ului](#backend-configuration)
8. [Configurarea dashboard-ului](#dashboard-configuration)
9. [Rularea digna ca serviciu Windows](#running-digna-as-a-windows-service)
10. [Actualizarea la o versiune nouă](#upgrading-to-a-new-release)

---

## Introducere {: #introduction }

### Despre digna

digna este o platformă completă, bazată pe AI, concepută pentru a optimiza gestionarea calității datelor în diverse medii de date, cum ar fi data warehouses, data lakes și lakehouses. Construită pentru scalabilitate și adaptabilitate ridicate, digna abordează provocările moderne ale datelor prin automatizare, monitorizare în timp real și detectarea anomaliilor.

digna este alcătuită din două componente principale:

- **digna**: nucleul aplicației, responsabil de prelucrarea datelor și de efectuarea verificărilor de calitate. Reunește backend-ul și interfața în linie de comandă într-un singur executabil, înlocuind programele separate `dignabackend` și `dignacli` din versiunile anterioare.
- **dignadashboard**: o interfață web găzduită pe un web server, care oferă o modalitate prietenoasă de a interacționa cu platforma digna și de a vizualiza metricile de calitate a datelor.

### Noutăți în Release 2026.06

Această versiune aduce capabilitățile de observabilitate a datelor direct în codul dumneavoastră, permițând dezvoltatorilor să monitorizeze calitatea datelor la sursă. Consultați [notele de lansare](http://docs.digna.ai/changelog/Release_202606/) pentru detalii complete.

### Căutați macOS sau Linux?

Acest ghid acoperă Windows. Pentru alte platforme, consultați [Ghidul de instalare macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) sau [Ghidul de instalare Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Cerințe de sistem {: #system-requirements }

Înainte de a începe instalarea, asigurați-vă că sistemul dumneavoastră îndeplinește următoarele cerințe minime:

| Cerință | Specificație |
|---|---|
| **Sistem de operare** | Windows Server sau Windows 10/11 |
| **Memorie (configurație minimă)** | 16 GB RAM |
| **Spațiu pe disc** | 10 GB spațiu de stocare disponibil |
| **Bază de date** | PostgreSQL Server 12 sau o versiune superioară |
| **Web server** | IIS, Apache Tomcat sau echivalent |

### Opțiuni de instalare a bazei de date

**Dacă PostgreSQL este deja instalat:**
Puteți adăuga o bază de date nouă pentru digna pe serverul PostgreSQL existent.

**Dacă instalați PostgreSQL pe aceeași mașină cu digna:**

!!! info "Specificații recomandate"

    - **Memorie**: 32 GB RAM (în loc de 16 GB)
    - **Spațiu pe disc**: 50 GB spațiu de stocare disponibil (în loc de 10 GB)

    Aceste specificații mai mari permit rularea simultană a digna și a bazei de date PostgreSQL.

---

## Pregătirea înainte de instalare {: #pre-installation-setup }

Înainte de a instala digna, asigurați-vă că sunt pregătite două cerințe preliminare esențiale:

1. **Serverul PostgreSQL** – pentru stocarea metricilor calculate și a datelor de performanță
2. **Web serverul** – pentru găzduirea digna Dashboard

Dacă aceste componente nu sunt deja configurate, urmați secțiunile de mai jos pentru a le instala și configura.

---

## Configurarea serverului PostgreSQL {: #postgresql-server-setup }

### Dacă aveți deja PostgreSQL

Dacă PostgreSQL este deja instalat și rulează pe mașina locală sau dacă folosiți un server PostgreSQL gestionat, la distanță, puteți trece direct la [secțiunea următoare](#web-server-configuration).

### Instalarea PostgreSQL

Urmați pașii de mai jos pentru a instala PostgreSQL pe Windows:

#### Pasul 1: Descărcați PostgreSQL

1. Accesați [pagina de descărcări PostgreSQL](https://www.postgresql.org/download/)
2. Selectați **Windows**
3. Descărcați cel mai recent program de instalare

#### Pasul 2: Rulați programul de instalare

1. Faceți dublu clic pe fișierul de instalare descărcat
2. Urmați instrucțiunile din asistentul de instalare

#### Pasul 3: Alegeți directorul de instalare

Selectați directorul în care va fi instalat PostgreSQL. Locația implicită este de obicei potrivită.

#### Pasul 4: Selectați componentele

Pentru o configurație standard, păstrați selectate opțiunile implicite ale componentelor.

#### Pasul 5: Setați parola superutilizatorului PostgreSQL

Introduceți și confirmați o parolă pentru superutilizatorul PostgreSQL (`postgres`). **Păstrați această parolă în siguranță** — veți avea nevoie de ea mai târziu.

#### Pasul 6: Configurați numărul portului

Portul implicit PostgreSQL este `5432`. Puteți folosi valoarea implicită sau puteți specifica un alt port, dacă este necesar.

!!! tip "Sfat"

    Dacă portul 5432 este deja utilizat, alegeți un port alternativ și notați-l pentru configurarea ulterioară.

#### Pasul 7: Alegeți setările regionale

Selectați setările regionale (locale) pentru baza de date. Valoarea implicită este de obicei potrivită pentru majoritatea instalărilor.

#### Pasul 8: Finalizați instalarea

Faceți clic pe **Next** în pașii rămași, apoi pe **Finish**.

#### Pasul 9: Verificați instalarea

Deschideți Command Prompt și verificați că PostgreSQL este instalat:

```bash
psql --version
```

Dacă instalarea a reușit, ar trebui să vedeți versiunea PostgreSQL.

---

## Configurarea web serverului {: #web-server-configuration }

digna necesită un web server pentru a găzdui dashboard-ul. Alegeți una dintre următoarele opțiuni:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Trebuie să instalați și să configurați **doar unul** dintre aceste servere.

### Configurarea IIS {: #iis-setup }

#### Prezentare generală

Internet Information Services (IIS) este web serverul Microsoft pentru găzduirea site-urilor și a aplicațiilor web.

#### Activarea IIS

1. **Deschideți Control Panel**
   - Apăsați `Win + R`
   - Tastați `control` și apăsați Enter

2. **Accesați Windows Features**
   - Faceți clic pe **Programs**
   - Selectați **Turn Windows features on or off**

3. **Activați Internet Information Services**
   - Derulați în jos și găsiți **Internet Information Services (IIS)**
   - Bifați caseta pentru a-l activa
   - Faceți clic pe **+** pentru a extinde lista și verificați că sunt selectate următoarele subcomponente:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Faceți clic pe OK** pentru a aplica modificările

5. **Verificați instalarea IIS**
   - Deschideți browserul
   - Accesați `http://localhost`
   - Ar trebui să vedeți pagina de bun venit IIS

#### Obligatoriu: modulul URL Rewrite

IIS necesită componenta URL Rewrite. Descărcați-o și instalați-o de pe [pagina oficială Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Obligatoriu: tipul MIME pentru fișierele Markdown

Pentru ca fișierele Markdown (`.md`) să fie servite corect de IIS:

1. Deschideți **IIS Manager** (apăsați `Win + R`, tastați `inetmgr`, apăsați Enter)
2. Accesați **Your Site > MIME Types**
3. Faceți clic pe **Add...**
4. Configurați:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Important"

    Fără această setare, fișierele `.md` s-ar putea să nu fie servite corect.

---

### Configurarea Apache Tomcat {: #apache-tomcat-setup }

#### Prezentare generală

Apache Tomcat este un container de servleturi Java și un web server open-source.

#### Instalare

1. **Descărcați Apache Tomcat**
   - Accesați [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Descărcați distribuția ZIP pentru Windows

2. **Extrageți arhiva**
   - Extrageți fișierul ZIP într-un director de pe sistemul dumneavoastră
   - Exemplu: `C:\Program Files\Apache Tomcat`

3. **Verificați că Tomcat rulează**
   - Deschideți browserul
   - Accesați `http://localhost:8080`
   - Ar trebui să vedeți pagina de bun venit Apache Tomcat

!!! tip "Sfat"

    Apache Tomcat pornește de obicei automat după instalare. Dacă nu pornește, accesați folderul `bin` și rulați `startup.bat`.

---

## Instalarea inițială {: #initial-installation }

### Pasul 1: Configurați repository-ul digna

Repository-ul digna stochează toate metricile calculate de digna. Acesta funcționează ca bază de date centrală pentru datele analitice și de performanță.

#### Creați schema repository-ului și utilizatorul

Deschideți clientul PostgreSQL (pgAdmin, psql sau similar) și executați următoarele comenzi SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Înlocuiți următorii substituenți:**

- `<digna_repo_schema>` — numele dorit pentru schemă (de ex. `dignarepo`)
- `<digna_repo_user>` — numele de utilizator dorit (de ex. `digna_user`)
- `<digna_repo_password>` — o parolă sigură pentru acest utilizator

**Exemplu:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Practică recomandată"

    Folosiți parole puternice și complexe pentru utilizatorii bazei de date. Evitați credențialele ușor de ghicit.

---

### Pasul 2: Extrageți pachetul de instalare digna

1. Găsiți fișierul ZIP de instalare digna care v-a fost furnizat
2. Extrageți-l în locația de instalare dorită
3. După extragere, ar trebui să vedeți următoarele elemente:
   - `dashboard/` — interfața web a dashboard-ului
   - `digna` — executabilul principal (backend + CLI combinate)

!!! info "Fișierele de configurare și de licență nu se află în pachet"

    Nici `config.toml`, nici `dashboard/dashboard_config.toml` nu sunt livrate cu instalarea — le
    creați pe amândouă dumneavoastră, în [Configurarea backend-ului](#backend-configuration) și
    [Configurarea dashboard-ului](#dashboard-configuration). Nici `license.toml` nu este livrat;
    digna îl furnizează separat, așa cum descrie Pasul 3.

### Pasul 3: Instalați fișierul de licență

!!! warning "Important"

    Fișierul de licență **nu** este inclus în pachetul de instalare și va fi furnizat separat de digna.

1. Găsiți fișierul `license.toml` care v-a fost furnizat
2. Copiați-l în directorul rădăcină al instalării digna (unde se află `config.toml` și executabilul `digna`)

**De ce este important:**
Fișierul de licență conține informațiile dumneavoastră de client, data de expirare a licenței și semnătura digitală. **Nu modificați acest fișier** — orice modificare îl invalidează.

**Structura directorului după configurare:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Configurarea backend-ului {: #backend-configuration }

### Pasul 1: Creați și editați fișierul de configurare

Fișierul `config_template.toml` este furnizat în directorul de instalare digna. Trebuie doar să-l redenumiți în `config.toml`.

**Locație:** `digna_installation/config.toml`

Deschideți `config.toml` într-un editor de text și configurați fiecare secțiune de mai jos.

#### Secțiunea [app]

Această secțiune configurează setările aplicației backend digna:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametru | Valoare | Observații |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | URL-ul frontend-ului | Dacă dashboard-ul se află pe alt server, includeți URL-ul acestuia |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Necesar pentru CORS cu credențiale |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Permite toate metodele HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Permite toate antetele |

#### Secțiunea [repo]

Această secțiune configurează conexiunea la baza de date PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parametru | Valoare | Observații |
|---|---|---|
| `digna_REPO_HOST` | `localhost` sau IP | Numele de gazdă/IP-ul serverului PostgreSQL |
| `digna_REPO_PORT` | `5432` (implicit) | Portul PostgreSQL |
| `digna_REPO_DB` | `postgres` | Numele bazei de date |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema creată anterior |
| `digna_REPO_USER` | `digna_user` | Utilizatorul creat la configurarea PostgreSQL |
| `digna_REPO_PASSWORD` | Parola dumneavoastră | Parola setată la crearea schemei |

#### Secțiunea [base]

Această secțiune conține setările de securitate și pentru cookie-uri:

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

| Parametru | Valoare | Observații |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Trebuie să corespundă domeniului frontend-ului |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (producție) | Folosiți `true` pentru conexiuni HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Întotdeauna activat, pentru securitate |
| `digna_COOKIE_SAME_SITE` | `lax` | Previne atacurile CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 de ore) | Durata sesiunii, în secunde |
| `digna_MAX_WORKERS` | Numărul de nuclee CPU - 1 | Numărul de sarcini de inspecție paralele |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Întârzierea maximă, în secunde, pe care planificatorul o poate adăuga înainte de a porni o sarcină scadentă |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Ora din zi (format de 24 de ore `HH:MM`) la care începe curățarea zilnică |

#### Secțiunea [encryption]

Această secțiune conține cheia folosită pentru a cripta valorile sensibile stocate în repository. Este **obligatorie** — `config check` raportează secțiunea `[encryption]` ca FAILED dacă lipsește cheia.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametru | Valoare | Observații |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Cheie codificată Base64 | Criptează valorile sensibile stocate în repository-ul digna |

!!! warning "Protejați config.toml"

    Această cheie este o valoare fixă, identică în toate instalările digna, și tocmai ea decriptează
    valorile sensibile din repository-ul dumneavoastră. Restricționați `config.toml` la contul care
    rulează digna, țineți fișierul în afara controlului versiunilor și a unităților partajate și
    excludeți-l din orice copie de siguranță păstrată mai puțin sigur decât repository-ul însuși.

#### Secțiunea [logging]

Această secțiune configurează comportamentul de logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametru | Valoare | Observații |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` sau `DEBUG` | `INFO` pentru producție, `DEBUG` pentru depanare |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Numărul de copii zilnice ale logurilor păstrate |

---

### Pasul 2: Validați configurația

Înainte de a inițializa repository-ul, verificați dacă `config.toml` este complet și corect alcătuit. În directorul de instalare digna, rulați:

```bash
digna config check
```

Fiecare secțiune este validată separat, astfel încât o singură greșeală nu ascunde starea celorlalte:

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

Corectați tot ce este raportat ca FAILED și rulați comanda din nou înainte de a continua. Lista completă a opțiunilor se află în [referința CLI](../../../cli/Command_Line_Interface_202606.md).

### Pasul 3: Inițializați repository-ul

1. Deschideți Command Prompt
2. Accesați directorul de instalare digna (unde se află `config.toml` și executabilul `digna`)
3. Rulați testul de conexiune:

```bash
digna repo check
```

Ar trebui să vedeți o confirmare că conexiunea este stabilită (repository-ul în sine nu a fost încă inițializat).

### Pasul 4: Instalați schema repository-ului

În același director, rulați:

```bash
digna repo install
```

Această comandă instalează tabelele și schema necesare în baza de date PostgreSQL.

### Pasul 5: Creați un utilizator administrator

Utilizatorul administrator este creat direct în schema repository-ului, astfel încât serverul nu trebuie să ruleze încă. În directorul de instalare digna, rulați:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Exemplu:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Aceasta creează un utilizator cu privilegii administrative complete.

!!! tip "Practică recomandată"

    Folosiți o parolă puternică, cu o combinație de majuscule, minuscule, cifre și caractere speciale.

### Pasul 6: Porniți serverul digna

În directorul de instalare digna, porniți serverul cu:

```bash
digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — numele de gazdă/IP-ul serverului
- `--port` — portul serverului

Ar trebui să vedeți mesajele de pornire care confirmă că serverul rulează:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "Serverul ocupă terminalul"

    `serve` rulează în prim-plan și continuă până când îl opriți cu ++ctrl+c++. Lăsați-l să ruleze cât timp finalizați configurarea; pentru a-l porni automat la pornirea sistemului, consultați [Rularea digna ca serviciu Windows](#running-digna-as-a-windows-service).

---

## Configurarea dashboard-ului {: #dashboard-configuration }

### Pasul 1: Implementați dashboard-ul pe web server

Dashboard-ul digna își citește propria configurație din `dashboard/dashboard_config.toml`. Acest fișier nu este livrat cu instalarea — îl creați în directorul `dashboard/`, alături de fișierele dashboard-ului.

Conținutul său este descris în [Single Sign-On](../../../sso/overview.md), unde este de altfel și nevoie de fișier: acesta conține opțiunile de autentificare oferite de dashboard și, pentru implementările cu mai multe instanțe, conexiunea la backend.

Alegeți web serverul și urmați pașii de implementare corespunzători.

#### Implementarea pe IIS

1. **Deschideți IIS Manager**
   - Apăsați `Win + R`, tastați `inetmgr`, apăsați Enter

2. **Creați un site web nou**
   - În panoul din stânga, faceți clic dreapta pe **Sites**
   - Selectați **Add Website...**

3. **Configurați site-ul web**
   - **Site Name**: introduceți un nume (de ex. "dignaDashboard")
   - **Physical Path**: faceți clic pe Browse și selectați folderul `dashboard`
   - **Binding**: setați adresa IP și portul (implicit portul 80 pentru HTTP, 443 pentru HTTPS)

4. **Porniți site-ul web**
   - Faceți clic pe **OK** pentru a crea site-ul
   - Faceți clic dreapta pe noul site și selectați **Start**

5. **Testați instalarea**
   - Deschideți browserul
   - Accesați `http://localhost` (sau URL-ul configurat)
   - Ar trebui să vedeți pagina de autentificare a dashboard-ului digna

#### Implementarea pe Apache Tomcat

1. **Copiați dashboard-ul în Tomcat**
   - Copiați folderul `dashboard` în directorul `webapps` al Tomcat
   - Redenumiți-l, dacă este necesar (de ex. în `digna`)
   - Exemplu: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verificați implementarea**
   - Reîmprospătați sau reîncărcați pagina de administrare Tomcat (http://localhost:8080)
   - Ar trebui să vedeți "digna" (sau numele ales) în lista aplicațiilor implementate

3. **Accesați dashboard-ul**
   - Deschideți browserul
   - Accesați `http://localhost:8080/digna`
   - Ar trebui să vedeți pagina de autentificare a dashboard-ului digna

---

## Rularea digna ca serviciu Windows {: #running-digna-as-a-windows-service }

### De ce să folosiți un serviciu Windows?

Rularea backend-ului digna ca serviciu Windows asigură că acesta:
- Pornește automat la pornirea serverului
- Rulează în fundal, fără un Command Prompt deschis
- Repornește automat dacă se blochează
- Poate fi gestionat prin Windows Services

### Comenzile `windows`

Serviciul este gestionat chiar de executabilul `digna`, prin subcomenzile `digna windows`.
Nu există fișiere batch de rulat.

| Comandă | Scop |
|---|---|
| `digna windows install` | Înregistrează digna ca serviciu Windows |
| `digna windows start` | Pornește serviciul înregistrat |
| `digna windows stop` | Oprește serviciul aflat în execuție |
| `digna windows uninstall` | Anulează înregistrarea serviciului |

!!! warning "Sunt necesare drepturi de administrator"

    Toate cele patru comenzi trebuie rulate dintr-un Command Prompt deschis ca Administrator.

Fiecare comandă acceptă `--name` pentru a adresa un serviciu înregistrat sub un nume diferit de cel
implicit. Lista completă a opțiunilor se află în [referința CLI](../../../cli/Command_Line_Interface_202606.md).

### Instalarea serviciului

1. **Deschideți Command Prompt ca Administrator**
   - Faceți clic dreapta pe Command Prompt
   - Selectați "Run as Administrator"

2. **Accesați directorul de instalare digna**
   ```bash
   cd C:\path\to\digna
   ```

3. **Înregistrați serviciul**
   ```bash
   digna windows install
   ```

!!! important "Specificați adresa și portul, dacă valorile implicite nu vă convin"

    `install` consemnează adresa și portul în înregistrarea serviciului, iar serviciul se leagă
    exact la ce a fost consemnat. Valorile implicite sunt `127.0.0.1` și `8000`, care acceptă conexiuni
    doar de pe mașina însăși. Un dashboard aflat pe altă gazdă nu le poate accesa, așa că indicați
    adresa pe care backend-ul trebuie să asculte:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Aceste valori nu sunt citite din `config.toml`. Pentru a le modifica ulterior, dezinstalați serviciul
    și instalați-l din nou cu noile valori.

Serviciul este înregistrat cu **pornire automată**, așa că va porni odată cu Windows. Nu pornește
imediat — consultați secțiunea următoare.

#### Opțiuni de instalare

| Opțiune | Implicit | Scop |
|---|---|---|
| `--name` | `digna` | Numele sub care se înregistrează serviciul |
| `--display-name` | `digna` | Numele afișat în services.msc |
| `--description` | `digna data quality backend` | Descrierea afișată în services.msc |
| `--address` | `127.0.0.1` | Adresa la care serviciul își leagă API-ul |
| `--port` | `8000` | Portul la care serviciul își leagă API-ul |
| `--working-dir` | directorul executabilului `digna` | Directorul care conține `config.toml` și `license.toml`, pe care serviciul îl folosește ca director de lucru |
| `--start-type` | `auto` | `auto` pornește odată cu Windows, `manual` pornește doar la cerere, `disabled` înregistrează serviciul, dar refuză să-l pornească |
| `--account` | `LocalSystem` | Contul sub care rulează, de ex. `DOMAIN\user` sau `.\user` |
| `--password` | | Parola pentru `--account` |

!!! tip "Rularea sub un cont de domeniu"

    `LocalSystem` nu are identitate de rețea, așa că autentificarea Windows față de SQL Server și orice
    acces la o partajare de rețea vor eșua. Instalați cu `--account` și `--password` acolo unde
    serviciul trebuie să acceseze resurse ca un anumit utilizator.

### Pornirea și oprirea serviciului

#### Pentru a porni serviciul

```bash
digna windows start
```

#### Pentru a opri serviciul

```bash
digna windows stop
```

!!! tip "Sfat"

    Opriți întotdeauna serviciul înainte de a actualiza fișierele aplicației.

### Mutarea serviciului într-un director nou

Dacă trebuie să mutați instalarea digna:

1. **Opriți serviciul curent și anulați-i înregistrarea**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Mutați fișierele aplicației**
   - Mutați întregul folder de instalare digna în noua locație

3. **Înregistrați din nou serviciul din noua locație**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Repetați toate valorile `--address`, `--port` sau `--account` pe care le-ați folosit prima dată — înregistrarea
   anterioară nu mai există.

4. **Porniți serviciul**
   ```bash
   digna windows start
   ```

### Dezinstalarea serviciului

1. **Opriți serviciul aflat în execuție**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Anulați înregistrarea serviciului**
   ```bash
   digna windows uninstall
   ```

Serverul digna nu mai este acum înregistrat ca serviciu Windows.

---

## Actualizarea la o versiune nouă {: #upgrading-to-a-new-release }

### Înainte de actualizare

**Verificați mai întâi toate conexiunile la baze de date**

Începând cu Release 2026.06, digna accesează fiecare tehnologie sursă prin **ODBC**. Versiunile anterioare
ofereau alegerea între un driver specific fiecărei tehnologii și ODBC, selectată prin comutatorul **Use ODBC**.
Echipa digna a decis să se bazeze exclusiv pe ODBC, deoarece o singură interfață standard vă oferă
mai mult decât un set de drivere făcute la comandă:

- **Autentificare** — autentificarea face parte din ODBC, așa că o conexiune poate folosi tot ce acceptă
  driverul său: parole, token-uri și PAT-uri, Kerberos și Active Directory, MFA și autentificare unică din browser,
  identități în cloud, certificate de client și TLS. Metodele noi vin odată cu o actualizare a driverului,
  fără a aștepta o versiune digna.
- **Drivere întreținute de producătorii bazelor de date** — driverul propriu al producătorului urmărește noile versiuni
  de server și corecțiile de securitate, iar dumneavoastră îl puteți actualiza după propriul calendar, independent de digna.
- **Un singur mod de a configura totul** — fiecare tehnologie este o listă de proprietăți cheie/valoare, cu
  aceeași interfață, aceeași criptare a valorilor sensibile și aceeași depanare,
  în locul unui set diferit de câmpuri pentru fiecare sursă.
- **Reglare și acoperire** — opțiunile driverului, precum timpii de expirare, setările TLS, proxy-urile și dimensiunile
  de citire, sunt disponibile pentru fiecare sursă, iar orice tehnologie cu un driver ODBC conform poate fi
  conectată, inclusiv cele pentru care digna nu publică un ghid dedicat.

În practică, aceasta înseamnă că comutatorul **Use ODBC** și câmpurile separate pentru gazdă, port, bază de date, utilizator și
parolă nu mai există. **Fiecare conexiune care nu folosește deja ODBC trebuie trecută
pe ODBC** — nu există conversie automată, așa că planificați acest lucru înainte de actualizare:

1. Parcurgeți fiecare conexiune la baze de date definită în instalarea dumneavoastră și notați-le pe cele care nu
   folosesc încă ODBC — fiecare dintre ele va trebui reconfigurată.
2. Instalați driverul ODBC corespunzător pe gazda digna — conexiunile sunt deschise de pe serverul
   care rulează backend-ul digna, nu din browser. Consultați
   [Instalarea driverului ODBC pe gazda digna](../../../databases/overview.md#install-the-driver).
3. Pregătiți proprietățile ODBC pentru fiecare conexiune afectată.
   [Ghidurile pe tehnologii](../../../databases/overview.md#technology-guides) prezintă, pentru fiecare sursă,
   un set de proprietăți verificat.

După actualizare, treceți fiecare conexiune afectată pe ODBC și testați-o din dashboard —
consultați [Crearea unei conexiuni la baza de date](../../../databases/overview.md#create-a-database-connection)
și [Testarea unei conexiuni](../../../databases/overview.md#testing-a-connection).

!!! warning "Conexiuni Databricks Legacy"

    Conectorul Databricks Legacy a fost eliminat în această versiune. Migrați aceste conexiuni
    către conectorul [Databricks](../../../databases/databricks_connector_guide.md).

**Crearea unei copii de siguranță a repository-ului digna este obligatorie**

Înainte de a actualiza digna, faceți o copie de siguranță a repository-ului (PostgreSQL) pentru a vă proteja împotriva pierderii de date.
O copie de siguranță vă permite recuperarea dacă actualizarea întâmpină probleme neașteptate.

### Procesul de actualizare

#### Pasul 1: Opriți vechiul serviciu și anulați-i înregistrarea

Dacă digna rulează ca serviciu Windows, opriți-l cu **fișierele batch ale instalării
curente** — comenzile `digna windows` aparțin noii versiuni și nu sunt încă
disponibile:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

Apoi anulați înregistrarea serviciului, tot cu vechiul fișier batch. Înregistrarea indică vechiul
executabil și scripturile acestuia, pe care această actualizare le înlocuiește pe amândouă, așa că nu poate fi refolosită:

```bash
uninstall_service.bat
```

!!! warning "Anulați înregistrarea înainte de a redenumi ceva"

    `uninstall_service.bat` se află în folderul `bin` pe care urmează să-l redenumiți și este singurul
    lucru care poate elimina înregistrarea pe care a creat-o. Rulați-l cât timp vechea instalare se află încă
    la locul ei. Dacă folderul a fost deja redenumit, readuceți-i numele inițial, anulați înregistrarea, apoi continuați.

    Notați contul sub care rula serviciul, precum și adresa și portul pe care servea — veți
    avea nevoie de ele la Pasul 9.

#### Pasul 2: Faceți o copie de siguranță a instalării curente

În directorul de instalare digna, redenumiți folderele instalării curente, astfel încât noua versiune să poată fi implementată alături de ele:

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

!!! info "dignabackend și dignacli nu mai sunt folosite"

    Începând cu Release 2026.06, `dignabackend` și `dignacli` sunt înlocuite de executabilul unic `digna`, care reunește backend-ul și CLI-ul. Păstrați `dignabackend_old` și `dignacli_old` doar până când ați verificat actualizarea — apoi puteți șterge ambele foldere. Păstrați `dashboard_old` până când v-ați restaurat din el fișierele de configurare (consultați Pasul 4). Și folderul `bin` dispare: fișierele sale batch controlau vechiul serviciu, iar versiunea 2026.06 nu le mai livrează, așa că, odată ce înregistrarea serviciului a fost anulată la Pasul 1, ele nu fac decât să inducă în eroare.

#### Pasul 3: Extrageți și implementați noua versiune

1. Extrageți noul fișier ZIP de instalare digna
2. Copiați noul executabil `digna` și folderul `dashboard` în directorul de instalare


!!! warning "Important"

    Nici `config.toml`, nici `dashboard/dashboard_config.toml` nu sunt incluse vreodată în
    ZIP-ul de instalare — echipa digna nu livrează niciodată aceste fișiere. Configurația existentă
    rămâne, prin urmare, neatinsă de actualizare, iar copiile din folderele `*_old` redenumite sunt
    singurele pe care le aveți.

#### Pasul 4: Restaurați fișierele de configurare

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "Release 2026.06 modifică config.toml"

    Trei setări sunt noi și obligatorii, iar trei nu mai sunt folosite. Un `config.toml` preluat dintr-o versiune anterioară nu conține setările noi, iar digna nu va porni cât timp acestea lipsesc. Adăugați următoarele în `config.toml` existent:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Adăugați cele două chei `[base]` în secțiunea `[base]` existentă și adăugați `[encryption]` ca secțiune nouă. Apoi eliminați setările care nu mai sunt folosite: **`digna_FERNET_KEY`** din `[base]`, precum și **`digna_APP_HOST`** și **`digna_APP_PORT`** din `[app]` — serverul își preia acum adresa și portul din `digna serve`.

    Ce face fiecare setare este descris în [Configurarea backend-ului](#backend-configuration).

!!! warning "Autentificare unică: formatul [oidc_clients] s-a schimbat"

    Release 2026.06 înlocuiește matricea de tabele cu câte un tabel pentru fiecare furnizor, denumit după
    cheia furnizorului. `DIGNA_OIDC_KEY` dispare — cheia face acum parte din antetul secțiunii.

    Înainte:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    După:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Repetați secțiunea pentru fiecare furnizor și păstrați fiecare cheie identică cu `key` din
    `dashboard_config.toml`. `digna config check` raportează `oidc_clients` ca FAILED cât timp
    forma veche este încă prezentă. Sunt afectate doar instalările care folosesc autentificarea unică.

#### Pasul 5: Reîncărcați web serverul

Dashboard-ul este un set de fișiere statice, așa că web serverul — și browserul — pot servi în continuare
versiunea anterioară. Reîncărcați sau reporniți web serverul care găzduiește folderul `dashboard`,
apoi reîncărcați pagina forțat (++ctrl+f5++).

#### Pasul 6: Validați configurația

Confirmați că `config.toml` actualizat este complet înainte de a atinge repository-ul:

```bash
digna config check
```

Fiecare secțiune trebuie să raporteze OK. Corectați tot ce este raportat ca FAILED și rulați comanda din nou înainte de a continua.

#### Pasul 7: Înlocuiți fișierul de licență

Fiecare versiune este licențiată separat. Copiați fișierul `license.toml` furnizat de echipa digna pentru
această versiune în directorul de instalare, înlocuindu-l pe cel vechi:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Nu păstrați licența anterioară"

    Un `license.toml` emis pentru o versiune anterioară nu o acoperă pe aceasta, iar fiecare comandă
    care verifică licența — `user`, `inspection`, `repo` — se oprește înainte de a atinge
    repository-ul atunci când verificarea eșuează. Verificați-o înainte de a merge mai departe:

    ```bash
    digna license check
    ```

#### Pasul 8: Actualizați schema repository-ului

Accesați directorul de instalare digna și rulați:

```bash
digna repo upgrade
```

Aceasta actualizează schema PostgreSQL la cea mai recentă versiune, păstrând toate datele existente.

#### Pasul 9: Înregistrați și porniți serviciul

Vechea înregistrare a fost eliminată la Pasul 1, așa că serviciul este înregistrat din nou — de data aceasta cu
executabilul `digna`, care nu are fișiere batch:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Dați opțiunilor `--address` și `--port` valorile pe care servea vechiul serviciu, cu excepția cazului în care doriți noile
valori implicite `127.0.0.1` și `8000`; acestea sunt consemnate în înregistrare și nu mai sunt citite
din `config.toml`. Adăugați `--account` și `--password` dacă vechiul serviciu rula sub un cont
de domeniu. Consultați
[Rularea digna ca serviciu Windows](#running-digna-as-a-windows-service) pentru lista completă
a opțiunilor.

Dacă rulați manual, reporniți serverul:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Dacă folosiți IIS sau Tomcat, reporniți web serverul respectiv.

#### Pasul 10: Verificați actualizarea

1. Accesați dashboard-ul digna
2. Verificați că interfața se încarcă corect
3. Verificați logurile serverului pentru eventuale erori
4. Treceți pe ODBC fiecare conexiune care nu îl folosea încă, apoi testați toate conexiunile
   — consultați [Testarea unei conexiuni](../../../databases/overview.md#testing-a-connection)


