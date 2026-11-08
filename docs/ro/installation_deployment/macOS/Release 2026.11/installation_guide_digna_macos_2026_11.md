---
title: Ghid de instalare pe macOS – digna Release 2026.11 | Documentația digna
description: Ghid pas cu pas pentru instalarea digna Release 2026.11 pe macOS — cerințe de sistem, configurarea Homebrew și PostgreSQL, configurarea nginx sau Apache, configurarea backend-ului și a dashboard-ului, rularea digna ca serviciu în fundal și actualizarea de la Release 2026.06.
keywords: digna instalare macos, ghid implementare digna mac, configurare backend digna, instalare dashboard digna, postgresql homebrew, nginx macos, serviciu launchd digna, ghid actualizare digna
image: /assets/logo_square.png
---

# Ghid de instalare pe macOS pentru digna Release 2026.11

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
9. [Rularea digna ca serviciu în fundal](#running-digna-as-a-background-service)
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

### Căutați Windows sau Linux?

Acest ghid acoperă macOS. Pentru alte platforme, consultați [Ghidul de instalare Windows](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) sau [Ghidul de instalare Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Cerințe de sistem {: #system-requirements }

Înainte de a începe instalarea, asigurați-vă că sistemul dumneavoastră îndeplinește următoarele cerințe minime:

| Cerință | Specificație |
|---|---|
| **Sistem de operare** | macOS 13 (Ventura) sau mai nou |
| **Arhitectură** | Apple Silicon (arm64) sau Intel (x86_64) |
| **Memorie (configurație minimă)** | 16 GB RAM |
| **Spațiu pe disc** | 10 GB spațiu de stocare disponibil |
| **Bază de date** | PostgreSQL Server 12 sau o versiune superioară |
| **Web server** | nginx, Apache httpd sau echivalent |
| **Instrumente de linie de comandă** | Xcode Command Line Tools (necesare pentru Homebrew) |

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

### Verificarea arhitecturii

Mai multe căi din acest ghid diferă între Mac-urile cu Apple Silicon și cele cu Intel. Pentru a verifica ce aveți, deschideți **Terminal** și rulați:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew se instalează în `/opt/homebrew`.
- `x86_64` — Intel. Homebrew se instalează în `/usr/local`.

!!! tip "Sfat"

    În loc să fixeze una dintre căi, acest ghid folosește `$(brew --prefix)`, care se extinde la locația corectă pe ambele arhitecturi. Puteți copia comenzile exact așa cum sunt.

---

## Pregătirea înainte de instalare {: #pre-installation-setup }

Înainte de a instala digna, asigurați-vă că sunt pregătite trei cerințe preliminare esențiale:

1. **Homebrew** – managerul de pachete folosit pentru a instala componentele de mai jos
2. **Serverul PostgreSQL** – pentru stocarea metricilor calculate și a datelor de performanță
3. **Web serverul** – pentru găzduirea digna Dashboard

Dacă aceste componente nu sunt deja configurate, urmați secțiunile de mai jos pentru a le instala și configura.

### Instalarea Homebrew

Homebrew este managerul de pachete standard pentru macOS și este folosit în tot acest ghid pentru a instala PostgreSQL și nginx.

#### Pasul 1: Verificați dacă Homebrew este deja instalat

Deschideți **Terminal** (apăsați `Cmd + Space`, tastați `Terminal`, apăsați Enter) și rulați:

```bash
brew --version
```

Dacă se afișează un număr de versiune, treceți direct la secțiunea [Configurarea serverului PostgreSQL](#postgresql-server-setup).

#### Pasul 2: Instalați Homebrew

Dacă comanda nu a fost găsită, instalați Homebrew urmând instrucțiunile de pe [site-ul oficial Homebrew](https://brew.sh). Programul de instalare instalează și Xcode Command Line Tools, dacă acestea nu sunt deja prezente.

#### Pasul 3: Adăugați Homebrew în PATH

Pe Apple Silicon, programul de instalare afișează două comenzi pentru a adăuga Homebrew în mediul shell-ului. Rulați-le conform instrucțiunilor, apoi confirmați:

```bash
brew --prefix
```

Ar trebui să se afișeze `/opt/homebrew` pe Apple Silicon sau `/usr/local` pe Intel.

---

## Configurarea serverului PostgreSQL {: #postgresql-server-setup }

### Dacă aveți deja PostgreSQL

Dacă PostgreSQL este deja instalat și rulează pe mașina locală sau dacă folosiți un server PostgreSQL gestionat, la distanță, puteți trece direct la [secțiunea următoare](#web-server-configuration).

### Opțiuni de instalare

macOS oferă două moduri simple de a instala PostgreSQL. Alegeți **unul**:

- [Homebrew](#postgresql-homebrew) — instalare din linia de comandă, recomandată pentru implementările pe server
- [Postgres.app](#postgresql-app) — instalare grafică, comodă pentru evaluarea locală

### Instalarea PostgreSQL cu Homebrew {: #postgresql-homebrew }

#### Pasul 1: Instalați formula PostgreSQL

```bash
brew install postgresql@16
```

#### Pasul 2: Adăugați PostgreSQL în PATH

Formulele PostgreSQL cu versiune sunt *keg-only*, ceea ce înseamnă că Homebrew nu leagă automat comenzile lor în PATH. Adăugați-le dumneavoastră:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Notă"

    Aceasta presupune shell-ul implicit `zsh` folosit de macOS. Dacă folosiți `bash`, adăugați aceeași linie în `~/.bash_profile`.

#### Pasul 3: Porniți serviciul PostgreSQL

```bash
brew services start postgresql@16
```

Aceasta pornește imediat PostgreSQL și îl configurează să pornească din nou automat la autentificare.

#### Pasul 4: Verificați instalarea

```bash
psql --version
```

Dacă instalarea a reușit, ar trebui să vedeți versiunea PostgreSQL.

#### Pasul 5: Conectați-vă la server

```bash
psql postgres
```

!!! warning "Important — aici macOS diferă de Windows"

    Programul de instalare pentru Windows vă cere să creați un superutilizator `postgres` și o parolă. Homebrew nu face acest lucru. În schimb, creează un superutilizator denumit după **contul dumneavoastră macOS**, fără parolă, accesibil doar de pe mașina locală.

    Aceasta înseamnă că o instalare Homebrew proaspătă nu are un rol `postgres`. Folosiți numele propriului cont atunci când aveți nevoie de un superutilizator și creați un utilizator digna explicit, așa cum este descris în [Instalarea inițială](#initial-installation).

#### Pasul 6: Confirmați portul

Portul implicit PostgreSQL este `5432`. Pentru a confirma portul pe care ascultă serverul:

```bash
psql postgres -c "SHOW port;"
```

Notați valoarea — veți avea nevoie de ea la configurarea backend-ului digna.

### Instalarea PostgreSQL cu Postgres.app {: #postgresql-app }

Dacă preferați o instalare grafică:

1. Descărcați [Postgres.app](https://postgresapp.com) și trageți-o în folderul **Applications**
2. Deschideți aplicația și faceți clic pe **Initialize** pentru a crea un server nou
3. Urmați instrucțiunile aplicației pentru a adăuga instrumentele sale de linie de comandă în PATH
4. Verificați instalarea:

```bash
psql --version
```

Și Postgres.app creează un superutilizator denumit după contul dumneavoastră macOS.

---

## Configurarea web serverului {: #web-server-configuration }

digna necesită un web server pentru a găzdui dashboard-ul. Alegeți una dintre următoarele opțiuni:

- [nginx](#nginx-setup) — instalat prin Homebrew, recomandat
- [Apache httpd](#apache-setup) — inclus în macOS

Trebuie să instalați și să configurați **doar unul** dintre aceste servere.

Ambele secțiuni configurează două lucruri de care depinde dashboard-ul:

- **O rută de rezervă pentru aplicația single-page**, astfel încât reîmprospătarea unui URL al dashboard-ului să nu returneze 404
- **Un tip MIME pentru `.md`**, astfel încât fișierele Markdown să fie servite corect

### Configurarea nginx {: #nginx-setup }

#### Prezentare generală

nginx este un web server ușor și performant, foarte potrivit pentru servirea dashboard-ului static digna.

#### Instalare

```bash
brew install nginx
```

#### Pornirea nginx

```bash
brew services start nginx
```

#### Verificați instalarea

1. Deschideți browserul
2. Accesați `http://localhost:8080`
3. Ar trebui să vedeți pagina de bun venit nginx

!!! note "Notă — portul implicit este 8080, nu 80"

    Homebrew configurează nginx să asculte pe portul `8080`, astfel încât să poată rula fără privilegii de administrator. Pe macOS, legarea la portul `80` sau la orice alt port sub 1024 necesită root.

    Pentru a servi dashboard-ul pe portul 80, schimbați `listen 8080;` în `listen 80;` în configurația de mai jos și porniți nginx cu `sudo brew services start nginx`.

#### Configurarea unui site pentru dashboard

Configurația nginx din Homebrew include fiecare fișier din directorul său `servers`. Creați acolo un fișier de configurare dedicat pentru digna:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Lipiți următorul conținut, înlocuind `/path/to/digna/dashboard` cu calea reală către folderul `dashboard` extras:

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

!!! warning "Important"

    Fără directiva `try_files`, reîncărcarea oricărei pagini a dashboard-ului în afară de URL-ul rădăcină returnează 404. Acesta este echivalentul nginx al modulului URL Rewrite cerut de IIS pe Windows.

#### Aplicați configurația

Testați configurația pentru erori de sintaxă, apoi reîncărcați nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Configurarea Apache httpd {: #apache-setup }

#### Prezentare generală

macOS include Apache httpd, așa că nu este necesară nicio instalare. Este dezactivat implicit.

#### Pornirea Apache

```bash
sudo apachectl start
```

#### Verificați instalarea

1. Deschideți browserul
2. Accesați `http://localhost`
3. Ar trebui să vedeți mesajul "It works!"

#### Obligatoriu: activați mod_rewrite

Dashboard-ul necesită rescrierea URL-urilor. Deschideți configurația Apache:

```bash
sudo nano /etc/apache2/httpd.conf
```

Găsiți linia următoare și eliminați `#` de la început pentru a o decomenta:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Obligatoriu: permiteți suprascrierile .htaccess

În același fișier, găsiți blocul `<Directory "/Library/WebServer/Documents">` și modificați:

```apache
AllowOverride None
```

în:

```apache
AllowOverride All
```

#### Obligatoriu: tipul MIME pentru fișierele Markdown

Tot în `httpd.conf`, adăugați linia următoare, astfel încât fișierele Markdown să fie servite corect:

```apache
AddType text/markdown .md
```

!!! warning "Important"

    Fără această setare, fișierele `.md` s-ar putea să nu fie servite corect.

#### Aplicați configurația

Verificați configurația pentru erori de sintaxă, apoi reporniți Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Instalarea inițială {: #initial-installation }

### Pasul 1: Configurați repository-ul digna

Repository-ul digna stochează toate metricile calculate de digna. Acesta funcționează ca bază de date centrală pentru datele analitice și de performanță.

#### Creați schema repository-ului și utilizatorul

Deschideți clientul PostgreSQL (psql, pgAdmin sau similar) și executați următoarele comenzi SQL:

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

Pentru a le rula din Terminal într-un singur pas:

```bash
psql postgres
```

Apoi lipiți instrucțiunile la promptul `postgres=#` și tastați `\q` pentru a ieși.

!!! tip "Practică recomandată"

    Folosiți parole puternice și complexe pentru utilizatorii bazei de date. Evitați credențialele ușor de ghicit.

---

### Pasul 2: Extrageți pachetul de instalare digna

1. Găsiți fișierul ZIP de instalare digna care v-a fost furnizat
2. Extrageți-l în locația de instalare dorită — de exemplu `/opt/digna` sau `~/digna`
3. După extragere, ar trebui să vedeți următoarele elemente:
   - `dashboard/` — interfața web a dashboard-ului
   - `digna` — executabilul principal (backend + CLI combinate)

!!! info "Fișierele de configurare și de licență nu se află în pachet"

    Nici `config.toml`, nici `dashboard/dashboard_config.toml` nu sunt livrate cu instalarea — le
    creați pe amândouă dumneavoastră, în [Configurarea backend-ului](#backend-configuration) și
    [Configurarea dashboard-ului](#dashboard-configuration). Nici `license.toml` nu este livrat;
    digna îl furnizează separat, așa cum descrie Pasul 3.

Pentru extragerea din Terminal:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Faceți executabilul rulabil

În funcție de modul în care a fost transferată arhiva, bitul de execuție s-ar putea să nu se păstreze la extragere. Setați-l explicit:

```bash
cd /opt/digna
chmod +x digna
```

#### Dacă macOS blochează aplicația

Fișierele descărcate printr-un browser sau un client de e-mail sunt marcate cu un atribut de carantină. Dacă macOS raportează că aplicația *"nu poate fi deschisă deoarece dezvoltatorul nu poate fi verificat"*, eliminați atributul din directorul de instalare:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativ, deschideți **System Settings → Privacy & Security**, găsiți elementul blocat în partea de jos a paginii și faceți clic pe **Open Anyway**.

!!! note "Notă"

    Acest pas este necesar doar dacă macOS blochează efectiv executabilul. Pachetele transferate prin SSH sau din partajări interne de fișiere nu sunt de obicei puse în carantină.

### Pasul 3: Instalați fișierul de licență

!!! warning "Important"

    Fișierul de licență **nu** este inclus în pachetul de instalare și va fi furnizat separat de digna.

1. Găsiți fișierul `license.toml` care v-a fost furnizat
2. Copiați-l în directorul rădăcină al instalării digna (unde se află `config.toml` și executabilul `digna`)

**De ce este important:**
Fișierul de licență conține informațiile dumneavoastră de client, data de expirare a licenței și semnătura digitală. **Nu modificați acest fișier** — orice modificare îl invalidează.

**Structura directorului după configurare:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Configurarea backend-ului {: #backend-configuration }

### Pasul 1: Creați și editați fișierul de configurare

Fișierul `config_template.toml` este furnizat în directorul de instalare digna. Trebuie doar să-l redenumiți în `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Locație:** `/opt/digna/config.toml`

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

!!! note "Notă"

    Dacă serviți dashboard-ul din nginx-ul Homebrew pe portul său implicit, originea care trebuie permisă este `http://localhost:8080`.

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

!!! tip "Sfat"

    Pentru a afla numărul de nuclee CPU disponibile pe Mac, rulați `sysctl -n hw.ncpu`.

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
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parametru | Valoare | Observații |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (implicit) | Memoria, în MB, pe care o poate folosi o singură rulare digna Engine. Pot fi active simultan până la `DIGNA_MAX_WORKERS` rulări |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Implicit: directorul temporar al sistemului (`$TMPDIR` al contului care rulează digna) | Directorul pentru fișierele temporare atunci când datele nu încap în memorie |

!!! tip "Dimensionarea digna Engine"

    Planificați pe gazda digna până la `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` de
    memorie, pe lângă cea folosită de digna însuși, precum și suficient spațiu liber pe disc în
    directorul temporar pentru cea mai mare dată inspectată a surselor de date care folosesc
    digna Engine. Direcționați `DIGNA_DUCKDB_TEMP_DIRECTORY` către un disc cu acest spațiu, în care
    contul care rulează digna poate scrie:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Aveți nevoie de această secțiune doar dacă cel puțin o conexiune la baze de date folosește
    digna Engine sau dacă o verificare de integritate referențială compară surse de date de pe
    conexiuni diferite.

---

### Pasul 2: Validați configurația

Înainte de a inițializa repository-ul, verificați dacă `config.toml` este complet și corect alcătuit. În directorul de instalare digna, rulați:

```bash
./digna config check
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

1. Deschideți **Terminal**
2. Accesați directorul de instalare digna (unde se află `config.toml` și executabilul `digna`)
3. Rulați testul de conexiune:

```bash
cd /opt/digna
./digna repo check
```

Pe o schemă nouă, comanda se conectează și apoi raportează că încă nu este instalat niciun repository:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

În acest moment, acesta este rezultatul așteptat: confirmă că digna ajunge la PostgreSQL și la schemă. O eroare de conexiune sau de autentificare indică, în schimb, o problemă în secțiunea `[repo]` sau în configurarea PostgreSQL.

!!! note "Notă"

    Pe macOS, comenzile din directorul curent nu se află în PATH, așa că executabilul este apelat ca `./digna`, nu ca `digna`. Pentru a folosi peste tot forma scurtă, adăugați directorul de instalare în PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Pasul 4: Instalați schema repository-ului

În același director, rulați:

```bash
./digna repo upgrade
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
./digna user add <email> <password> "<display_name>" --admin
```

**Exemplu:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Aceasta creează un utilizator cu adresa de e-mail `admin@example.com` și privilegii administrative complete.

!!! tip "Sfat"

    Puneți parola între ghilimele simple. `zsh` tratează în mod special caractere precum `!`, `$` și `*`, iar o parolă fără ghilimele care le conține nu va fi transmisă așa cum a fost tastată.

!!! tip "Practică recomandată"

    Folosiți o parolă puternică, cu o combinație de majuscule, minuscule, cifre și caractere speciale.

### Pasul 6: Porniți serverul digna

În directorul de instalare digna, porniți serverul cu:

```bash
./digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — numele de gazdă/IP-ul serverului (implicit `127.0.0.1`)
- `--port` — portul serverului (implicit `8000`)

Când serverul a pornit, acesta afișează adresa pe care ascultă:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Sfat"

    La prima pornire a serverului, macOS vă poate întreba dacă doriți ca aplicația să accepte conexiuni de rețea de intrare. Faceți clic pe **Allow**; în caz contrar, dashboard-ul nu va putea accesa backend-ul.

!!! note "Serverul ocupă terminalul"

    `serve` rulează în prim-plan și continuă până când îl opriți cu ++ctrl+c++. Lăsați-l să ruleze cât timp finalizați configurarea; pentru a-l porni automat la pornirea sistemului, consultați [Rularea digna ca serviciu în fundal](#running-digna-as-a-background-service).

---

## Configurarea dashboard-ului {: #dashboard-configuration }

### Pasul 1: Implementați dashboard-ul pe web server

Dashboard-ul digna își citește propria configurație din `dashboard/dashboard_config.toml`. Acest fișier nu este livrat cu instalarea — îl creați în directorul `dashboard/`, alături de fișierele dashboard-ului.

Conținutul său este descris în [Single Sign-On](../../../sso/overview.md), unde este de altfel și nevoie de fișier: acesta conține opțiunile de autentificare oferite de dashboard și, pentru implementările cu mai multe instanțe, conexiunea la backend.

Alegeți web serverul și urmați pașii de implementare corespunzători.

#### Implementarea pe nginx

Dacă ați urmat secțiunea [Configurarea nginx](#nginx-setup), blocul server indică deja folderul `dashboard` și nu este necesară nicio copiere.

1. **Confirmați calea**
   - Deschideți `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Verificați că `root` indică folderul `dashboard` extras

2. **Asigurați-vă că folderul poate fi citit**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Reîncărcați nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Testați instalarea**
   - Deschideți browserul
   - Accesați `http://localhost:8080` (sau URL-ul configurat)
   - Ar trebui să vedeți pagina de autentificare a dashboard-ului digna

#### Implementarea pe Apache httpd

1. **Copiați dashboard-ul în document root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Adăugați regulile de rescriere**

   Creați un fișier `.htaccess` în folderul implementat, astfel încât rutele dashboard-ului să reziste la reîmprospătarea browserului:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Lipiți următorul conținut:

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

3. **Reporniți Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Accesați dashboard-ul**
   - Deschideți browserul
   - Accesați `http://localhost/digna`
   - Ar trebui să vedeți pagina de autentificare a dashboard-ului digna

---

## Rularea digna ca serviciu în fundal {: #running-digna-as-a-background-service }

### De ce să rulați digna ca serviciu?

Rularea backend-ului digna ca serviciu în fundal asigură că acesta:

- Pornește automat la pornirea mașinii
- Rulează în fundal, fără o fereastră Terminal deschisă
- Repornește automat dacă se blochează
- Poate fi gestionat prin `launchctl`, managerul de servicii din macOS

### Fișierele de gestionare a serviciului

Toate fișierele necesare se află în directorul de instalare digna, în: `bin/`

Sunt disponibile următoarele scripturi shell:

- `install_service.sh` — înregistrează digna în launchd
- `uninstall_service.sh` — anulează înregistrarea serviciului
- `start_service.sh` — pornește serviciul înregistrat
- `stop_service.sh` — oprește serviciul aflat în execuție

!!! warning "Sunt necesare drepturi de administrator"

    Toate scripturile trebuie executate cu `sudo`, deoarece înregistrarea unui serviciu care pornește la pornirea sistemului scrie în `/Library/LaunchDaemons`.

### Facerea scripturilor executabile

Este posibil ca extragerea să nu păstreze bitul de execuție. Înainte de prima utilizare:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Instalarea serviciului

1. **Deschideți Terminal**

2. **Accesați folderul bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Rulați scriptul de instalare**
   ```bash
   sudo ./install_service.sh
   ```

Serverul digna este acum înregistrat în launchd, cu **pornire automată** activată. Serviciul nu pornește imediat — consultați secțiunea următoare pentru a-l porni.

### Pornirea și oprirea serviciului

#### Pentru a porni serviciul

1. Deschideți Terminal
2. Accesați `/opt/digna/bin`
3. Rulați:
   ```bash
   sudo ./start_service.sh
   ```

#### Pentru a opri serviciul

1. Deschideți Terminal
2. Accesați `/opt/digna/bin`
3. Rulați:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Sfat"

    Opriți întotdeauna serviciul înainte de a actualiza fișierele aplicației.

### Verificarea serviciului

Pentru a confirma că serviciul este înregistrat și rulează:

```bash
sudo launchctl list | grep digna
```

O linie care începe cu un ID de proces indică faptul că serviciul rulează. Un `-` în prima coloană înseamnă că este înregistrat, dar oprit.

### Mutarea serviciului într-un director nou

launchd stochează calea absolută către executabil, așa că mutarea instalării necesită reînregistrarea serviciului:

1. **Dezinstalați serviciul curent**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Mutați fișierele aplicației**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Reinstalați serviciul**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Porniți serviciul**
   ```bash
   sudo ./start_service.sh
   ```

### Dezinstalarea serviciului

1. **Opriți serviciul aflat în execuție**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Dezinstalați serviciul**
   ```bash
   sudo ./uninstall_service.sh
   ```

Serverul digna nu mai este acum înregistrat în launchd.

---

## Actualizarea la o versiune nouă {: #upgrading-to-a-new-release }

Această secțiune descrie actualizarea unei instalări Release 2026.06 la Release 2026.11.

!!! warning "Actualizare de la o versiune anterioară 2026.06"

    Efectuați mai întâi pașii de actualizare la Release 2026.06: [Actualizarea la o versiune nouă](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release). Apoi continuați cu pașii de mai jos.

### Înainte de actualizare

**Crearea unei copii de siguranță a repository-ului digna este obligatorie**

Înainte de a actualiza digna, faceți o copie de siguranță a repository-ului (PostgreSQL) pentru a vă proteja împotriva pierderii de date.
O copie de siguranță vă permite recuperarea dacă actualizarea întâmpină probleme neașteptate.

Pentru a crea o copie de siguranță din Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Solicitarea fișierului de licență pentru Release 2026.11**

Release 2026.11 necesită un nou `license.toml`. Solicitați-l echipei digna înainte de a începe și
pregătiți-l pentru [Pasul 7](#step-7-replace-the-license-file).

### Procesul de actualizare

#### Pasul 1: Opriți serviciul digna {: #step-1-stop-the-digna-service }

Dacă digna rulează ca serviciu în fundal, opriți-l mai întâi:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Dacă digna rulează în prim-plan, apăsați ++ctrl+c++ în fereastra sa Terminal.

#### Pasul 2: Faceți o copie de siguranță a instalării curente {: #step-2-backup-current-installation }

În directorul de instalare digna, redenumiți executabilul și folderul dashboard al instalării
curente, astfel încât noua versiune să poată fi implementată alături de ele:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Păstrați `digna_old` până când ați verificat actualizarea, iar `dashboard_old` până când v-ați
restaurat din el fișierele de configurare (consultați Pasul 4). După aceea le puteți șterge pe amândouă.

#### Pasul 3: Extrageți și implementați noua versiune {: #step-3-extract-and-deploy-new-version }

1. Extrageți noul fișier ZIP de instalare digna
2. Copiați noul executabil `digna` și folderul `dashboard` în directorul de instalare
3. Restabiliți bitul de execuție și, dacă este necesar, eliminați atributul de carantină:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Important"

    Nici `config.toml`, nici `dashboard/dashboard_config.toml` nu sunt incluse vreodată în
    ZIP-ul de instalare — echipa digna nu livrează niciodată aceste fișiere. Configurația existentă
    rămâne, prin urmare, neatinsă de actualizare, iar copiile din folderele `*_old` redenumite sunt
    singurele pe care le aveți.

#### Pasul 4: Restaurați fișierele de configurare {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
apoi reîncărcați pagina forțat (++cmd+shift+r++).

#### Pasul 6: Validați configurația {: #step-6-validate-the-configuration }

Confirmați că `config.toml` este complet înainte de a atinge repository-ul:

```bash
./digna config check
```

Fiecare secțiune trebuie să raporteze OK. Corectați tot ce este raportat ca FAILED, eliminați
cheile enumerate la **Unknown keys** și rulați comanda din nou înainte de a continua.

#### Pasul 7: Înlocuiți fișierul de licență {: #step-7-replace-the-license-file }

Un fișier de licență emis pentru o versiune anterioară nu funcționează cu Release 2026.11. Copiați
fișierul `license.toml` furnizat de echipa digna pentru Release 2026.11 în directorul de instalare,
înlocuindu-l pe cel vechi:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Nu păstrați licența anterioară"

    Cu licența anterioară, fiecare comandă care verifică licența — `serve`, `user`,
    `inspection`, `repo` — eșuează, așa că digna nu pornește, iar repository-ul nu poate fi
    actualizat. Verificați noua licență înainte de a merge mai departe:

    ```bash
    ./digna license check
    ```

#### Pasul 8: Actualizați schema repository-ului {: #step-8-upgrade-the-repository-schema }

În directorul de instalare digna, rulați:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 gestionează schema repository-ului prin migrări versionate. Prima actualizare de
la o versiune anterioară aduce schema la ultima versiune a vechiului sistem, o înregistrează ca
punct de pornire și apoi aplică migrările din Release 2026.11. Se încheie cu:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Toate datele existente sunt păstrate. Pentru a vedea oricând starea repository-ului, rulați
`./digna repo check`: comanda afișează cea mai recentă migrare aplicată și eventualele migrări în așteptare.

!!! warning "digna nu pornește cu un repository neactualizat"

    Începând cu Release 2026.11, serverul refuză să pornească atât timp cât repository-ul trebuie
    actualizat și semnalează acest lucru, de exemplu:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Rulați `repo upgrade` înainte de a porni serverul sau serviciul.

#### Pasul 9: Reporniți serviciile {: #step-9-restart-services }

Dacă rulați ca serviciu în fundal:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Dacă rulați manual, reporniți serverul:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Dacă folosiți nginx sau Apache, reporniți web serverul respectiv:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Pasul 10: Verificați actualizarea {: #step-10-verify-the-upgrade }

1. Confirmați versiunea noului executabil:

    ```bash
    ./digna version
    ```

    Prima linie trebuie să fie `Release: 2026.11`.

2. Accesați dashboard-ul digna și verificați că interfața se încarcă corect.
3. Verificați ieșirea serverului și fișierele din directorul `logs` pentru erori.
4. Testați conexiunile la baze de date — consultați
   [Testarea unei conexiuni](../../../databases/overview.md#testing-a-connection).

Pentru a începe cu noile module, consultați [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Conectarea unui agent AI](../../../platform/agentic/connect_ai_agent.md) pentru digna MCP Server și
[Locația de profilare](../../../platform/profiling/profiling_location.md) pentru digna Engine.
