---
title: Ghid de instalare pe Windows – digna Release 2026.11 | Documentația digna
description: Ghid pas cu pas pentru instalarea digna Release 2026.11 pe Windows — cerințe de sistem, configurarea PostgreSQL, configurarea web serverului, configurarea backend-ului și a dashboard-ului, rularea digna ca serviciu Windows și actualizarea de la Release 2026.06.
keywords: digna instalare windows, ghid implementare digna, configurare backend digna, instalare dashboard digna, configurare postgresql, serviciu windows digna, ghid actualizare digna
image: /assets/logo_square.png
---

# Ghid de instalare pe Windows pentru digna Release 2026.11

**Release:** 2026.11

**Ultima actualizare:** 7 noiembrie 2026


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

### Noutăți în Release 2026.11

Această versiune adaugă digna Data Reconciliation, digna Agentic împreună cu digna MCP Server și digna Engine, care poate profila datele în interiorul digna și poate verifica integritatea referențială între tehnologii de baze de date diferite. Consultați [notele de lansare](../../../changelog/Release_202611.md) pentru detalii complete.

Pentru instalare, versiunea aduce un nou mecanism de migrare a repository-ului, o secțiune opțională `[duckdb]` în `config.toml` pentru digna Engine și un nou fișier de licență. [Secțiunea despre actualizare](#upgrading-to-a-new-release) le tratează pe fiecare dintre ele.

### Căutați macOS sau Linux?

Acest ghid acoperă Windows. Pentru alte platforme, consultați [Ghidul de instalare macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) sau [Ghidul de instalare Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Conexiunile la baze de date care folosesc digna Engine ca locație de profilare sunt profilate
    chiar pe gazda digna. Planificați memorie și spațiu pe disc suplimentare pentru ele; consultați
    [secțiunea \[duckdb\]](#duckdb-section).

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

Această secțiune configurează partajarea resurselor între origini (CORS) dintre dashboard și backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parametru | Valoare | Observații |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URL-urile dashboard-ului | URL-urile de pe care este servit dashboard-ul. Cererile browserului de la orice altă origine sunt respinse |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Obligatoriu, pentru ca browserul să trimită cookie-ul de sesiune cu fiecare cerere |

!!! info "Secțiunea [app] este opțională"

    Începând cu Release 2026.11, ambele chei, chiar și întreaga secțiune `[app]`, pot fi omise.
    Aceasta este configurarea potrivită atunci când un reverse proxy servește dashboard-ul și
    backend-ul sub aceeași origine: browserul nu face atunci cereri între origini, iar implicit
    niciuna nu este permisă.

#### Secțiunea [repo]

Această secțiune configurează conexiunea la baza de date PostgreSQL:

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

| Parametru | Valoare | Observații |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` sau IP | Numele de gazdă/IP-ul serverului PostgreSQL |
| `DIGNA_REPO_PORT` | `5432` (implicit) | Portul PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Numele bazei de date |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema creată anterior |
| `DIGNA_REPO_USER` | `digna_user` | Utilizatorul creat la configurarea PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Parola dumneavoastră | Parola setată la crearea schemei |
| `DIGNA_REPO_SSLMODE` | `prefer` (implicit) | Opțional. Modul SSL PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` sau `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (implicit) | Opțional. Numărul de conexiuni pe care digna le menține deschise către repository |

#### Secțiunea [base]

Această secțiune conține setările de securitate, pentru cookie-uri și pentru inspecții:

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

| Parametru | Valoare | Observații |
|---|---|---|
| `DIGNA_FERNET_KEY` | Valoarea afișată mai sus | Cheia criptării folosite de versiunile anterioare. Trebuie să fie prezentă; păstrați valoarea afișată |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Gazda prin care este accesat dashboard-ul. `""` nu setează niciun domeniu, ceea ce este corect în spatele unui proxy care servește dashboard-ul și backend-ul sub aceeași origine |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Trebuie să fie `true` ori de câte ori digna este servit prin HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Ține cookie-ul de sesiune departe de scripturi |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 de ore) | Durata sesiunii, în secunde |
| `DIGNA_MAX_WORKERS` | Numărul de nuclee CPU - 1 | Numărul de inspecții care pot rula în același timp |
| `DIGNA_FRONTEND_BASEURL` | URL-ul dashboard-ului | Obligatoriu. Este folosit pentru linkurile din mesajele de notificare, deci trebuie să fie un URL pe care destinatarii îl pot deschide |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (implicit) | Opțional. Numărul de secunde în care o singură interogare asupra unei baze de date sursă poate rula înainte de a fi întreruptă; `0` dezactivează limita de timp |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (implicit) | Opțional. Numărul de secunde de așteptare pentru conectarea la o bază de date sursă; `0` așteaptă la nesfârșit |

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
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parametru | Valoare | Observații |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` sau `DEBUG` | `INFO` pentru producție, `DEBUG` pentru depanare. Sunt acceptate și `TRACE`, `WARN` și `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (implicit) | Opțional. Directorul pentru fișierele de log cu rotație, relativ la directorul de lucru |
| `DIGNA_LOGGING_MAX_FILES` | `30` (implicit) | Opțional. Numărul de fișiere de log rotite care se păstrează |

!!! warning "Păstrați directorul de loguri când rulați ca serviciu"

    Un serviciu Windows nu are consolă, așa că fișierele de log sunt singura evidență a ceea ce face
    serviciul. Nu setați `DIGNA_LOGGING_DIR` la un șir gol, deoarece acesta dezactivează fișierele de log.

#### Secțiunea [duckdb] (opțională) {: #duckdb-section }

Nou în Release 2026.11. Această secțiune stabilește resursele **digna Engine**, care profilează
datele în interiorul digna pentru conexiunile la baze de date a căror locație de profilare este
**digna Engine** și rulează verificări de integritate referențială între surse de date aflate pe
conexiuni la baze de date diferite. Consultați
[Locația de profilare](../../../platform/profiling/profiling_location.md).

Secțiunea este opțională. Fără ea se aplică valorile implicite de mai jos.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parametru | Valoare | Observații |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (implicit) | Memoria, în MB, pe care o poate folosi o singură rulare digna Engine. Pot fi active simultan până la `DIGNA_MAX_WORKERS` rulări |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Implicit: directorul temporar al contului care rulează digna (`%TEMP%`) | Directorul pentru fișierele temporare atunci când datele nu încap în memorie |

!!! tip "Dimensionarea digna Engine"

    Planificați pe gazda digna până la `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` de
    memorie, pe lângă cea folosită de digna însuși, precum și suficient spațiu liber pe disc în
    directorul temporar pentru cea mai mare dată inspectată a surselor de date care folosesc
    digna Engine. Direcționați `DIGNA_DUCKDB_TEMP_DIRECTORY` către un disc cu acest spațiu, în care
    contul care rulează digna poate scrie:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Aveți nevoie de această secțiune doar dacă cel puțin o conexiune la baze de date folosește
    digna Engine sau dacă o verificare de integritate referențială compară surse de date de pe
    conexiuni diferite.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Corectați tot ce este raportat ca FAILED și rulați comanda din nou înainte de a continua. Un WARNING la **Unknown keys** enumeră cheile din `config.toml` pe care digna nu le citește; acestea nu au niciun efect, așa că eliminați-le sau corectați-le ortografia. Lista completă a opțiunilor se află în [referința CLI](../../../cli/Command_Line_Interface_202611.md).

### Pasul 3: Inițializați repository-ul

1. Deschideți Command Prompt
2. Accesați directorul de instalare digna (unde se află `config.toml` și executabilul `digna`)
3. Rulați testul de conexiune:

```bash
digna repo check
```

Pe o schemă nouă, comanda se conectează și apoi raportează că încă nu este instalat niciun repository:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

În acest moment, acesta este rezultatul așteptat: confirmă că digna ajunge la PostgreSQL și la schemă. O eroare de conexiune sau de autentificare indică, în schimb, o problemă în secțiunea `[repo]` sau în configurarea PostgreSQL.

### Pasul 4: Instalați schema repository-ului

În același director, rulați:

```bash
digna repo upgrade
```

Această comandă instalează tabelele necesare în schema repository-ului și se încheie cu:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instalează și actualizează"

    Începând cu Release 2026.11, `repo upgrade` instalează un repository nou și actualizează unul
    existent. `repo install` funcționează în continuare ca alt nume pentru aceeași comandă.

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
- `--address` — numele de gazdă/IP-ul serverului (implicit `127.0.0.1`)
- `--port` — portul serverului (implicit `8000`)

Când serverul a pornit, acesta afișează adresa pe care ascultă:

```text
Server running on http://127.0.0.1:8082
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
implicit. Lista completă a opțiunilor se află în [referința CLI](../../../cli/Command_Line_Interface_202611.md).

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

Această secțiune actualizează o instalare Release 2026.06 la Release 2026.11. Dacă instalarea
dumneavoastră este mai veche, citiți mai întâi
[Actualizarea de la o versiune mai veche decât 2026.06](#upgrading-from-a-release-before-2026-06).

### Înainte de actualizare

**Crearea unei copii de siguranță a repository-ului digna este obligatorie**

Înainte de a actualiza digna, faceți o copie de siguranță a repository-ului (PostgreSQL) pentru a vă proteja împotriva pierderii de date.
O copie de siguranță vă permite recuperarea dacă actualizarea întâmpină probleme neașteptate.

**Solicitarea fișierului de licență pentru Release 2026.11**

Release 2026.11 necesită un nou `license.toml`. Solicitați-l echipei digna înainte de a începe și
pregătiți-l pentru [Pasul 7](#step-7-replace-the-license-file).

### Actualizarea de la o versiune mai veche decât 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 a adus trei schimbări care se aplică în continuare atunci când actualizați o
instalare mai veche direct la 2026.11:

- **Doar ODBC.** digna accesează fiecare tehnologie sursă prin ODBC. Fiecare conexiune la baze de
  date care nu folosește încă ODBC trebuie trecută pe ODBC după actualizare; nu există conversie
  automată. Instalați în prealabil driverele ODBC pe gazda digna, consultați
  [Instalarea driverului ODBC pe gazda digna](../../../databases/overview.md#install-the-driver),
  și pregătiți proprietățile fiecărei conexiuni din
  [ghidurile pe tehnologii](../../../databases/overview.md#technology-guides). Conectorul
  Databricks Legacy nu mai există; mutați acele conexiuni pe conectorul
  [Databricks](../../../databases/databricks_connector_guide.md).
- **Un singur executabil.** `dignabackend` și `dignacli` sunt înlocuite de executabilul unic
  `digna`, care reunește backend-ul și CLI-ul.
- **config.toml.** Secțiunea `[encryption]` este obligatorie, iar `DIGNA_APP_HOST` și
  `DIGNA_APP_PORT` nu mai sunt citite: serverul își preia adresa și portul din `digna serve`.
  Comparați fișierul dumneavoastră cu [Configurarea backend-ului](#backend-configuration).

Pașii de mai jos indică unde o instalare mai veche necesită altceva. Actualizarea repository-ului
de la Pasul 8 aduce un repository din orice versiune anterioară direct la 2026.11.

### Procesul de actualizare

#### Pasul 1: Opriți serviciul digna {: #step-1-stop-the-digna-service }

Deschideți un Command Prompt ca Administrator și opriți serviciul cu executabilul `digna` al
instalării curente:

```bash
cd C:\path\to\digna
digna windows stop
```

Serviciul rămâne înregistrat. Noul executabil îl înlocuiește pe cel vechi în același director, așa
că înregistrarea indică în continuare fișierul corect.

Dacă digna rulează în prim-plan, apăsați ++ctrl+c++ în fereastra sa de Command Prompt.

!!! warning "Actualizarea de la o versiune mai veche decât 2026.06"

    Versiunile mai vechi decât 2026.06 înregistrau serviciul cu fișiere batch. Opriți serviciul și
    anulați-i înregistrarea cu fișierele batch ale instalării curente, **înainte** de a redenumi
    ceva la Pasul 2:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    Notați contul sub care rula serviciul, precum și adresa și portul pe care servea. Veți
    înregistra serviciul din nou la Pasul 9.

#### Pasul 2: Faceți o copie de siguranță a instalării curente {: #step-2-backup-current-installation }

În directorul de instalare digna, redenumiți executabilul și folderul dashboard al instalării
curente, astfel încât noua versiune să poată fi implementată alături de ele:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Păstrați `digna_old.exe` până când ați verificat actualizarea, iar `dashboard_old` până când v-ați
restaurat din el fișierele de configurare (consultați Pasul 4). După aceea le puteți șterge pe amândouă.

!!! info "Actualizarea de la o versiune mai veche decât 2026.06"

    Redenumiți folderele `dignabackend` și `dignacli` în locul executabilului:
    `ren dignabackend dignabackend_old` și `ren dignacli dignacli_old`. Release 2026.11 nu folosește niciunul dintre aceste foldere și nici folderul `bin` cu fișiere batch.

#### Pasul 3: Extrageți și implementați noua versiune {: #step-3-extract-and-deploy-new-version }

1. Extrageți noul fișier ZIP de instalare digna
2. Copiați noul executabil `digna` și folderul `dashboard` în directorul de instalare

!!! warning "Important"

    Nici `config.toml`, nici `dashboard/dashboard_config.toml` nu sunt incluse vreodată în
    ZIP-ul de instalare — echipa digna nu livrează niciodată aceste fișiere. Configurația existentă
    rămâne, prin urmare, neatinsă de actualizare, iar copiile din folderele `*_old` redenumite sunt
    singurele pe care le aveți.

#### Pasul 4: Restaurați fișierele de configurare {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

Release 2026.11 nu necesită nicio modificare a `config.toml`: un fișier care funcționează cu
Release 2026.06 funcționează în continuare. Două modificări sunt opționale:

- Adăugați o [secțiune `[duckdb]`](#duckdb-section) dacă conexiunile la baze de date vor folosi
  digna Engine, iar valorile implicite ale acestuia nu se potrivesc gazdei dumneavoastră.
- Omiteți secțiunea `[app]` dacă un reverse proxy servește dashboard-ul și backend-ul sub aceeași
  origine.

!!! warning "Setări pe care digna nu le citește"

    Versiunile anterioare ale acestui ghid prezentau unele setări pe care digna nu le citește.
    Acestea nu au niciun efect, iar `config check` le enumeră la **Unknown keys** în Pasul 6.
    Eliminați-le sau corectați-le:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` și
      `digna_LOGGING_BACKUP_COUNT` nu există. Eliminați-le.
    - Numele setărilor țin cont de majuscule și minuscule. digna citește `DIGNA_REPO_HOST`, nu
      `digna_REPO_HOST`. Scrieți fiecare nume cu majuscule, ca în
      [Configurarea backend-ului](#backend-configuration).

!!! warning "Autentificare unică: păstrați [[oidc_clients]]"

    digna citește furnizorii de autentificare unică sub forma unei liste de intrări
    `[[oidc_clients]]`, fiecare cu propriul `DIGNA_OIDC_KEY`. Dacă v-ați schimbat furnizorii în
    secțiuni `[oidc_clients.<key>]`, așa cum arăta o versiune anterioară a acestui ghid, readuceți-i
    la forma inițială. `config check` raportează `OIDC config(s)` ca FAILED cât timp acea formă
    este prezentă:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Repetați intrarea pentru fiecare furnizor și păstrați fiecare `DIGNA_OIDC_KEY` identic cu `key`
    din `dashboard_config.toml`. Sunt afectate doar instalările care folosesc autentificarea unică.

#### Pasul 5: Reîncărcați web serverul {: #step-5-reload-the-web-server }

Dashboard-ul este un set de fișiere statice, așa că web serverul — și browserul — pot servi în continuare
versiunea anterioară. Reîncărcați sau reporniți web serverul care găzduiește folderul `dashboard`,
apoi reîncărcați pagina forțat (++ctrl+f5++).

#### Pasul 6: Validați configurația {: #step-6-validate-the-configuration }

Confirmați că `config.toml` este complet înainte de a atinge repository-ul:

```bash
digna config check
```

Fiecare secțiune trebuie să raporteze OK. Corectați tot ce este raportat ca FAILED, eliminați
cheile enumerate la **Unknown keys** și rulați comanda din nou înainte de a continua.

#### Pasul 7: Înlocuiți fișierul de licență {: #step-7-replace-the-license-file }

În mod normal, un fișier de licență se păstrează de la o versiune la alta. Release 2026.11 este o
excepție: adaugă două module licențiate, digna Data Reconciliation și digna Agentic, iar o licență
emisă înainte de 2026.11 nu le conține. Copiați fișierul `license.toml` furnizat de echipa digna
pentru Release 2026.11 în directorul de instalare, înlocuindu-l pe cel vechi:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Nu păstrați licența anterioară"

    Cu licența anterioară, digna pornește în continuare, dar digna Data Reconciliation și digna
    MCP Server rămân dezactivate. Fiecare comandă care verifică licența — `user`,
    `inspection`, `repo` — se oprește înainte de a atinge repository-ul atunci când verificarea
    eșuează. Verificați noua licență înainte de a merge mai departe:

    ```bash
    digna license check
    ```

#### Pasul 8: Actualizați schema repository-ului {: #step-8-upgrade-the-repository-schema }

În directorul de instalare digna, rulați:

```bash
digna repo upgrade
```

Release 2026.11 gestionează schema repository-ului prin migrări versionate. Prima actualizare de
la o versiune anterioară aduce schema la ultima versiune a vechiului sistem, o înregistrează ca
punct de pornire și apoi aplică migrările din Release 2026.11. Se încheie cu:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Toate datele existente sunt păstrate. Pentru a vedea oricând starea repository-ului, rulați
`digna repo check`: comanda afișează cea mai recentă migrare aplicată și eventualele migrări în așteptare.

!!! warning "digna nu pornește cu un repository neactualizat"

    Începând cu Release 2026.11, serverul refuză să pornească atât timp cât repository-ul trebuie
    actualizat și semnalează acest lucru, de exemplu:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Rulați `repo upgrade` înainte de a porni serverul sau serviciul.

#### Pasul 9: Reporniți serviciile {: #step-9-restart-services }

Dacă digna rulează ca serviciu Windows, porniți-l din nou:

```bash
cd C:\path\to\digna
digna windows start
```

Dacă ați actualizat de la o versiune mai veche decât 2026.06 și ați anulat înregistrarea serviciului la
Pasul 1, înregistrați-l mai întâi din nou cu executabilul `digna`:

```bash
digna windows install --address <address> --port <port>
digna windows start
```

Dați opțiunilor `--address` și `--port` valorile pe care servea vechiul serviciu, cu excepția
cazului în care doriți valorile implicite `127.0.0.1` și `8000`. Adăugați `--account` și
`--password` dacă vechiul serviciu rula sub un cont de domeniu. Consultați
[Rularea digna ca serviciu Windows](#running-digna-as-a-windows-service) pentru lista completă
a opțiunilor.

Dacă rulați manual, reporniți serverul:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Dacă folosiți IIS sau Tomcat, reporniți web serverul respectiv.

#### Pasul 10: Verificați actualizarea {: #step-10-verify-the-upgrade }

1. Confirmați versiunea noului executabil:

    ```bash
    digna version
    ```

    Prima linie trebuie să fie `Release: 2026.11`.

2. Accesați dashboard-ul digna și verificați că interfața se încarcă corect.
3. Verificați fișierele din directorul `logs` al instalării pentru erori.
4. Testați conexiunile la baze de date — consultați
   [Testarea unei conexiuni](../../../databases/overview.md#testing-a-connection). După o
   actualizare de la o versiune mai veche decât 2026.06, treceți mai întâi pe ODBC fiecare conexiune
   care nu îl folosea încă.

Pentru a începe cu noile module, consultați [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Conectarea unui agent AI](../../../platform/agentic/connect_ai_agent.md) pentru digna MCP Server și
[Locația de profilare](../../../platform/profiling/profiling_location.md) pentru digna Engine.
